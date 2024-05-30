document.addEventListener('DOMContentLoaded', function() {
    let dropArea = document.getElementById('pdf-drop-area');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('hover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('hover'), false);
    });

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        let pdfInput = document.getElementById('pdfElem');
        const file = files[0];
        if (file && file.type === "application/pdf") {
            pdfInput.files = createFileList(file);
            updateUI(file);
        }
    }

    function createFileList(file) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        return dataTransfer.files;
    }

    function updateUI(file) {
        document.getElementById('labelForPdfElem').textContent = file.name; // Update label to show file name
    }

    document.getElementById('pdfElem').addEventListener('change', function() {
        if (this.files.length > 0) {
            const file = this.files[0];
            updateUI(file);
        }
    });

    document.getElementById('submitButton').addEventListener('click', function() {
        checkInputAndFile();
    });

    function checkInputAndFile() {
        var text = document.getElementById('chatInput').value;
        var file = document.getElementById('pdfElem').files[0];
        if (text && file) {
            window.location.href = '/validate'; // Redirect to the validate route on success
        } else {
            document.getElementById('result').innerText = 'Please provide both a text prompt and a file.';
        }
    }
});
