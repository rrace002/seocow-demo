(function () {
  function buildBody(form) {
    var data = new FormData(form);
    var lines = [];
    data.forEach(function (value, key) { lines.push(key + ": " + value); });
    return lines.join("\n");
  }
  document.querySelectorAll("form.lead-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      var subject = "Red Rabbit Security inquiry";
      if (form.id === "assessment-form") subject = "Free security assessment request";
      if (form.id === "proposal-form") subject = "Proposal request";
      if (form.id === "contact-form") subject = "Contact request";
      var mailto = "mailto:info@redrabbitsec.com?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(buildBody(form));
      var success = form.parentElement.querySelector(".form-success");
      if (success) { success.hidden = false; success.style.display = "block"; }
      window.location.href = mailto;
    });
  });
})();
