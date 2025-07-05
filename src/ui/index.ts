document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('file') as HTMLInputElement | null;
  const indicator = document.getElementById('file-indicator');

  if (fileInput && indicator) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files.length > 0) {
        indicator.textContent = `File selected: ${fileInput.files[0].name}`;
      } else {
        indicator.textContent = '';
      }
    });
  }
}); 