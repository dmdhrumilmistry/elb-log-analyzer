// import { Tabulator } from 'tabulator-tables';
const ipRequestCountTable = 'ip-requests-count-table';

let fileLoaded = false; // Flag to check if the file has already been loaded
let jsonData = null; // letiable to store JSON file data


function addEventListener() {
    document.getElementById('analyzed-file').addEventListener('change', function (event) {
        if (!fileLoaded) {
            fileLoaded = true; // Set the flag to true to indicate the file has been loaded

            let file = event.target.files[0];
            let reader = new FileReader();

            reader.onload = function (e) {
                let jsonContent = e.target.result;
                jsonData = JSON.parse(jsonContent);
                // Call a function or perform any actions with the loaded JSON data
                createDashboard(jsonData);
            };
            reader.readAsText(file);
        }
    });
}

function createIPRequestCountTable(jsonData) {
    // create list to store ip data
    let ipsData = [];

    for (let clientIP in jsonData) {
        if (clientIP === 'total') { continue; }

        // add data to list
        ipsData.push({
            ip: clientIP,
            total_requests: jsonData[clientIP].total,
            ports: jsonData[clientIP].ports,
            user_agents: jsonData[clientIP].user_agents
        })
    }

    // sort ip data list based on requests count
    ipsData.sort(function (a, b) {
        return b.total_requests - a.total_requests;
    });


    const IPtable = new Tabulator(`#${ipRequestCountTable}`, {
        data: ipsData,
        autoColumns: true, // Automatically generate columns
        layout: "fitColumns", // Adjust column widths to fit the table width
        height: "300px",
    });

}

function createDashboard(jsonData) {
    // Display the JSON data on the page
    createIPRequestCountTable(jsonData);
}

addEventListener();