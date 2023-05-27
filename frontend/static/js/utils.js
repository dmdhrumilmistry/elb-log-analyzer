var fileLoaded = false; // Flag to check if the file has already been loaded
var jsonData = null; // Variable to store JSON file data


function addEventListener() {
    document.getElementById('analyzed-file').addEventListener('change', function (event) {
        if (!fileLoaded) {
            fileLoaded = true; // Set the flag to true to indicate the file has been loaded

            var file = event.target.files[0];
            var reader = new FileReader();

            reader.onload = function (e) {
                var jsonContent = e.target.result;
                jsonData = JSON.parse(jsonContent);
                // Call a function or perform any actions with the loaded JSON data
                createDashboard(jsonData);
            };
            reader.readAsText(file);
        }
    });
}

function createDashboard(jsonData) {
    // Display the JSON data on the page
    console.log(jsonData);
    var jsonDataContainer = document.getElementById('dashboard');
    jsonDataContainer.textContent = JSON.stringify(jsonData);
}
