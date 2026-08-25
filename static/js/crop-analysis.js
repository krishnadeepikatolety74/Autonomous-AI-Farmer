document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const imagePreview = document.getElementById("image-preview");
    const previewContainer = document.getElementById("preview-container");
    const dropZone = document.getElementById("drop-zone");
    const form = document.getElementById("crop-analysis-form");
    const loadingContainer = document.getElementById("analysis-loading");
    const resultsContainer = document.getElementById("analysis-results");

    if (!fileInput) return;

    // Handle file selection preview
    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                imagePreview.src = event.target.result;
                previewContainer.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle drag and drop visuals
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "var(--primary)";
            dropZone.style.background = "#EAF7EC";
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "rgba(111, 175, 123, 0.3)";
            dropZone.style.background = "#FAFDFB";
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            // Trigger change event to update preview
            const event = new Event('change');
            fileInput.dispatchEvent(event);
        }
    });

    // Form submit loading switch
    form.addEventListener("submit", () => {
        if (resultsContainer) {
            resultsContainer.style.display = "none";
        }
        form.style.display = "none";
        loadingContainer.style.display = "block";
    });
});
