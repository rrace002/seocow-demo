(function () {
  function buildBody(form) {
    var data = new FormData(form);
    var lines = [];
    data.forEach(function (value, key) {
      lines.push(key + ": " + value);
    });
    return lines.join("\n");
  }

  document.querySelectorAll("form.lead-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;

      var subject = "SEO Cow inquiry";
      if (form.id === "audit-form") subject = "Free website audit request";
      if (form.id === "proposal-form") subject = "Proposal request";
      if (form.id === "contact-form") subject = "Contact request";

      var body = buildBody(form);
      var mailto =
        "mailto:info@seocow.com?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);

      var success = form.parentElement.querySelector(".form-success");
      if (success) {
        success.hidden = false;
        success.style.display = "block";
      }
      window.location.href = mailto;
    });
  });
})();
