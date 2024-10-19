// document.addEventListener('DOMContentLoaded', () => {
//     console.log("Script loaded");

    // Handle clicking on .clickableDiv elements
    document.querySelectorAll('.clickableDiv').forEach(function(div) {
        div.addEventListener('click', function() {
            // Get the text of the clicked div (e.g., "CBA", "CS", etc.)
            const selectedCollege = div.textContent.trim();
            
            // Redirect to the program.html page with the selected college as a query parameter
            window.location.href = `/college/program/${selectedCollege}/`;
        });
    });

    // Drag-and-drop functionality setup
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('input-file');

    if (dropArea && fileInput) {
        // Prevent default behavior for dragover and drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
            dropArea.addEventListener(event, e => e.preventDefault());
            dropArea.addEventListener(event, e => e.stopPropagation());
        });

        // Add visual feedback on dragover
        dropArea.addEventListener('dragover', () => {
            dropArea.classList.add('dragover');
        });

        // Remove feedback on dragleave
        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('dragover');
        });

        // Handle the file drop
        dropArea.addEventListener('drop', (event) => {
            dropArea.classList.remove('dragover');
            const files = event.dataTransfer.files;

            // Check if file is a CSV
            if (files.length && files[0].type === 'text/csv') {
                fileInput.files = files; // Programmatically set the input file
                alert('File dropped successfully!');
            } else {
                alert('Please upload a CSV file.');
            }
        });

        // Handle the input click
        fileInput.addEventListener('change', (event) => {
            const files = event.target.files;
            if (files.length) {
                alert(`File selected: ${files[0].name}`);
            }
        });
    } else {
        console.error("Drop area or file input not found in the DOM.");
    }
// });
