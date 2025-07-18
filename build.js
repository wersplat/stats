const fs = require('fs');
const path = require('path');

// Get list of all recap files from the recaps directory
const recaps = fs.readdirSync('recaps')
    .filter(file => file.endsWith('_recap.txt'));

// Read the worker file
let workerContent = fs.readFileSync('_worker.js', 'utf8');

// Update the RECAP_FILES array in the worker file
workerContent = workerContent.replace(
    'const RECAP_FILES = [\n    // This will be replaced by the build script\n];',
    `const RECAP_FILES = ${JSON.stringify(recaps, null, 4)};`
);

// Write the updated worker file
fs.writeFileSync('_worker.js', workerContent);

console.log('Build completed. Found', recaps.length, 'recap files.');
