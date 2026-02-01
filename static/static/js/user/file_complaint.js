document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality
    const fileUpload = document.getElementById('fileUpload');
    const imageUpload = document.getElementById('imageUpload');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const removeFile = document.getElementById('removeFile');

    if (fileUpload) {
        fileUpload.addEventListener('click', () => imageUpload.click());
    }

    if (imageUpload) {
        imageUpload.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                fileName.textContent = file.name;
                filePreview.style.display = 'flex';
            }
        });
    }

    if (removeFile) {
        removeFile.addEventListener('click', () => {
            imageUpload.value = '';
            filePreview.style.display = 'none';
        });
    }

    // Category change handler
    const categorySelect = document.getElementById('category');
    const otherCategoryInput = document.getElementById('otherCategoryInput');
    const otherCategoryField = document.getElementById('otherCategory');

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            if (this.value === 'other') {
                otherCategoryInput.style.display = 'block';
                otherCategoryField.required = true;
            } else {
                otherCategoryInput.style.display = 'none';
                otherCategoryField.required = false;
            }
        });
    }
});
