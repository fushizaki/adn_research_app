// fonction drag and drop + gestion de plusieurs fichiers avec preview et suppression
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
let selectedFiles = [];

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, highlight, false);
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
  dropZone.classList.add("border-black", "bg-gray-200");
}

function unhighlight(e) {
  dropZone.classList.remove("border-black", "bg-gray-200");
}

dropZone.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = Array.from(dt.files);
  addFilesToSelection(files);
}

fileInput.addEventListener("change", function () {
  const files = Array.from(this.files);
  addFilesToSelection(files);
});

function addFilesToSelection(newFiles) {
  selectedFiles = [...selectedFiles, ...newFiles];

  if (selectedFiles.length > 0) {
    dropZone.classList.add("border-green-500", "bg-green-50");
    displayPreview(selectedFiles);
  }
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  if (selectedFiles.length === 0) {
    dropZone.classList.remove("border-green-500", "bg-green-50");
  }
  displayPreview(selectedFiles);
}

function displayPreview(files) {
        const previewList = document.getElementById("previewFichier");
        previewList.innerHTML = files
            .map(
                (file, index) =>
                    `<li class="flex justify-between items-center mb-2 p-2 bg-gray-100 rounded">
          <span>${file.name}</span>
          <button type="button" onclick="removeFile(${index})" class="ml-2 text-red-600 hover:text-red-800 font-bold">✕</button>
        </li>`
            )
            .join("");
    }
