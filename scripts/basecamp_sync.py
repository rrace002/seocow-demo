#!/usr/bin/env python3
"""Create Basecamp projects + go-live to-do lists from dashboard/data/projects.json.

Uses the official Basecamp 4 REST API (https://github.com/basecamp/bc-api).

Required env:
  BASECAMP_ACCOUNT_ID
  BASECAMP_ACCESS_TOKEN
  BASECAMP_USER_AGENT   e.g. "NearMeOS LaunchBase (you@example.com)"

Optional:
  BASECAMP_PROGRESS_JSON  path to exported dashboard progress JSON

Examples:
  python scripts/basecamp_sync.py --dry-run
  python scripts/basecamp_sync.py --only near-me-os,ahbi
  python scripts/basecamp_sync.py --mark-from-progress progress.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "dashboard" / "data" / "projects.json"


class BasecampClient:
    """Minimal Basecamp 4 client (https://github.com/basecamp/bc-api)."""

    def __init__(self, account_id: str, token: str, user_agent: str) -> None:
        # Paths have no /api/v1 prefix — account ID is the first path segment.
        self.base = f"https://3.basecampapi.com/{account_id}"
        self.token = token
        self.user_agent = user_agent

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base}{path}"
        data = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": self.user_agent,
            "Content-Type": "application/json; charset=utf-8",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{method} {path} failed ({exc.code}): {detail}") from exc


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def project_description(project: dict[str, Any]) -> str:
    lines = [
        f"Client: {project.get('client', '')}",
        f"Type: {project.get('type', '')}",
        f"Staging: {project.get('url', '')}",
    ]
    if project.get("pr"):
        lines.append(f"PR: {project['pr']}")
    if project.get("pages"):
        lines.append(f"Pages: ~{project['pages']}")
    if project.get("notes"):
        lines.append("")
        lines.append(project["notes"])
    lines.append("")
    lines.append("Synced from Near Me OS Launch Base.")
    return "\n".join(lines)


def create_launch_project(
    client: BasecampClient,
    project: dict[str, Any],
    checklist: list[dict[str, Any]],
    done_ids: set[str],
    dry_run: bool,
) -> None:
    name = f"Launch · {project['name']}"
    print(f"→ {name}")
    if dry_run:
        for item in checklist:
            mark = "x" if item["id"] in done_ids else " "
            print(f"   [{mark}] {item['group']}: {item['label']}")
        return

    created = client.request(
        "POST",
        "/projects.json",
        {
            "name": name,
            "description": project_description(project),
        },
    )
    project_id = created["id"]
    print(f"   project id={project_id}")

    # Basecamp creates default tools; todoset id lives on the project dock.
    project_detail = client.request("GET", f"/projects/{project_id}.json")
    todoset_id = None
    for dock in project_detail.get("dock", []):
        if dock.get("name") == "todoset" and dock.get("enabled"):
            todoset_id = dock.get("id")
            break
    if not todoset_id:
        raise RuntimeError(f"No todoset found for project {project_id}")

    groups: dict[str, list[dict[str, Any]]] = {}
    for item in checklist:
        groups.setdefault(item["group"], []).append(item)

    for group_name, items in groups.items():
        todolist = client.request(
            "POST",
            f"/todosets/{todoset_id}/todolists.json",
            {
                "name": group_name,
                "description": f"<div>Go-live checklist for {project['name']}</div>",
            },
        )
        todolist_id = todolist["id"]
        for item in items:
            todo = client.request(
                "POST",
                f"/todolists/{todolist_id}/todos.json",
                {"content": item["label"]},
            )
            if item["id"] in done_ids:
                client.request(
                    "POST",
                    f"/todos/{todo['id']}/completion.json",
                    {},
                )
        print(f"   todolist '{group_name}' ({len(items)} items)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--only",
        help="Comma-separated project ids to sync",
    )
    parser.add_argument(
        "--mark-from-progress",
        type=Path,
        help="Dashboard export JSON; marks completed to-dos when creating",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_json(args.data)
    checklist = data["checklistTemplate"]
    projects = data["projects"]

    only = None
    if args.only:
        only = {part.strip() for part in args.only.split(",") if part.strip()}
        projects = [p for p in projects if p["id"] in only]

    progress: dict[str, Any] = {}
    progress_path = args.mark_from_progress
    if not progress_path and os.environ.get("BASECAMP_PROGRESS_JSON"):
        progress_path = Path(os.environ["BASECAMP_PROGRESS_JSON"])
    if progress_path:
        exported = load_json(progress_path)
        progress = exported.get("progress", exported)

    if args.dry_run:
        client = None
    else:
        account = os.environ.get("BASECAMP_ACCOUNT_ID", "").strip()
        token = os.environ.get("BASECAMP_ACCESS_TOKEN", "").strip()
        ua = os.environ.get("BASECAMP_USER_AGENT", "").strip()
        missing = [
            name
            for name, val in [
                ("BASECAMP_ACCOUNT_ID", account),
                ("BASECAMP_ACCESS_TOKEN", token),
                ("BASECAMP_USER_AGENT", ua),
            ]
            if not val
        ]
        if missing:
            print("Missing env: " + ", ".join(missing), file=sys.stderr)
            print("Tip: open the dashboard Basecamp settings and Copy env snippet.", file=sys.stderr)
            return 2
        client = BasecampClient(account, token, ua)

    for project in projects:
        done_map = progress.get(project["id"], {}).get("done", {})
        done_ids = {key for key, val in done_map.items() if val}
        create_launch_project(
            client,  # type: ignore[arg-type]
            project,
            checklist,
            done_ids,
            dry_run=args.dry_run,
        )

    print(f"Done. {'Dry run only.' if args.dry_run else f'Synced {len(projects)} project(s).'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
