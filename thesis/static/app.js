document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('drop-area');
    const inputFile = document.getElementById('input-file');
    const uploadIcon = document.getElementById('upload-icon');
    let uploadedFile = null;

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.style.borderColor = '#000';
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.style.borderColor = '#ccc';
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.style.borderColor = '#ccc';
        const files = event.dataTransfer.files;
        if (files.length && files[0].type === 'text/csv') {
            uploadedFile = files[0];
            showMagicButton();
            displayCSVIcon(); // Show the CSV icon
        } else {
            alert('Please upload a CSV file.');
        }
    });

    inputFile.addEventListener('change', (event) => {
        const files = event.target.files;
        if (files.length && files[0].type === 'text/csv') {
            uploadedFile = files[0];
            displayCSVIcon(); // Show the CSV icon
            // Show Magic Button after file is uploaded
            showMagicButton();
        } else {
            alert('Please upload a CSV file.');
        }
    });

    function getCSRFToken() {
        const cookieValue = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : null;
    }

    function displayCSVIcon() {
        // Change the icon to a CSV icon
        uploadIcon.src = "/static/image/csv.png"; // Ensure the path matches your setup
        uploadIcon.alt = "CSV Icon";
    }

    function showMagicButton() {
        const magicButtonContainer = document.getElementById('magicButtonContainer');
        magicButtonContainer.innerHTML = '<button id="magicButton" class="magicbutton">Apply Prediction Model</button>';
        document.getElementById('magicButton').addEventListener('click', function() {
            applyModelAndDisplayResults()
            alert('Successfully applied the prediction model!');

        });
    }
    
    function applyModelAndDisplayResults() {
        return new Promise((resolve, reject) => {
            if (uploadedFile) {
                const formData = new FormData();
                formData.append('file', uploadedFile);
    
                fetch('/upload/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: formData,
                })
                .then(response => {
                    console.log('Response status:', response.status);
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        console.error('Server error:', data.error);
                        reject(data.error);
                    } else {
                        resolve(data);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    reject(error);
                });
            } else {
                alert('No file uploaded.');
                reject('No file uploaded.');
            }
        });
    }
    
    
});
