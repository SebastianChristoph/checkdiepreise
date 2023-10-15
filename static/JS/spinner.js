document.addEventListener("DOMContentLoaded", function () {
  const spinner = document.querySelector("#spinner");
  const linkis = document.querySelectorAll(".linki");

  linkis.forEach((linki) => {
    linki.addEventListener("click", function () {
      console.log("ok");
      spinner.style.display = "block";
    });
  });
});
