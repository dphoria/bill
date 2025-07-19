document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("file") as HTMLInputElement | null;
  const indicator = document.getElementById("file-indicator");
  const form = document.querySelector("form") as HTMLFormElement;
  const loadingOverlay = document.getElementById("loading-overlay") as HTMLElement;

  if (fileInput && indicator) {
    fileInput.addEventListener("change", () => {
      if (fileInput.files && fileInput.files.length > 0) {
        indicator.textContent = `File selected: ${fileInput.files[0].name}`;
      } else {
        indicator.textContent = "";
      }
    });
  }

  if (form && loadingOverlay) {
    form.addEventListener("submit", () => {
      loadingOverlay.classList.remove("hidden");
    });
  }
});
