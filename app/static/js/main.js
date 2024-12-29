document.addEventListener("DOMContentLoaded", () => {
  const flashMessages = document.querySelectorAll(".flash");
  flashMessages.forEach((flash) => {
    setTimeout(() => flash.classList.add("show"), 100);
    setTimeout(() => flash.classList.remove("show"), 3100);
  });
});
