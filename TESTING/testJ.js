const fs = require('node:fs');
const path = require('path');

// Define the path to p.json
const jsonFilePath = path.join(__dirname, '..', 'json', 'p.json');

// Read the JSON file
fs.readFile(jsonFilePath, 'utf-8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
        return;
    }

    // Parse and use the JSON data
    const jsonData = JSON.parse(data);
    console.log(jsonData);
});