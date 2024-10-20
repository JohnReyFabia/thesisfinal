document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.program-link');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); 
            
            const programName = this.getAttribute('data-program-name');
            console.log('Program Name:', programName); 
            console.log('College Code:', collegeCode);

        
            fetch(`/college/${collegeCode}/${programName}/`)
                .then(response => response.json())
                .then(data => {
                    console.log('Data received:', data);
                    if (data.error) {
                        document.getElementById('program-details').innerHTML = `<p>${data.error}</p>`;
                    } else {
                        let yearList = '';
                        if (data.years && Array.isArray(data.years)) {
                            data.years.forEach(yearObj => {
                                yearList += `
                                <div>
                                    <p>Year: ${yearObj.year}, No. of Slots: ${yearObj.no_of_slots}</p>
                                </div>`;  
                            });
                        }


                        document.getElementById('program-details').innerHTML = `
                            <h3>${data.program_name}</h3>
                            ${yearList} 
                        `;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('program-details').innerHTML = '<p>Something went wrong!</p>';
                });
        });
    });
});
