// Add event listener to file input to show selected file name
const fileInput = document.querySelector('#id_file');
const fileLabel = document.querySelector('#file-label');
if (fileInput && fileLabel) {
  fileInput.addEventListener('change', () => {
    fileLabel.textContent = fileInput.files[0].name;
  });
}
