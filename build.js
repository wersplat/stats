const fs = require('fs');
const path = require('path');

// Read all recap files from the recaps directory
const recapsDir = path.join(__dirname, 'recaps');
const files = fs.readdirSync(recapsDir)
    .filter(file => file.endsWith('_recap.txt'));

console.log(`Found ${files.length} recap files.`);

// Process each file to extract metadata
const recapsData = files.map(file => {
    try {
        // Extract teams and timestamp from filename
        const fileName = file.replace('_recap.txt', '');
        const lastUnderscore = fileName.lastIndexOf('_');
        
        if (lastUnderscore === -1) {
            console.warn(`Skipping file with invalid format (no timestamp): ${file}`);
            return null;
        }
        
        const baseName = fileName.substring(0, lastUnderscore);
        const gameId = fileName.substring(lastUnderscore + 1);
        const timestamp = parseInt(gameId);
        
        if (isNaN(timestamp) || timestamp.toString() !== gameId) {
            console.warn(`Skipping file with invalid timestamp: ${file}`);
            return null;
        }
        
        // Split into teams
        const vsIndex = baseName.indexOf('_vs_');
        if (vsIndex === -1) {
            console.warn(`Skipping file with invalid team format: ${file}`);
            return null;
        }
        
        const team1 = baseName.substring(0, vsIndex);
        const team2 = baseName.substring(vsIndex + 4); // +4 to skip '_vs_'
        
        return {
            filename: file,
            team1: team1.replace(/_/g, ' '),
            team2: team2.replace(/_/g, ' '),
            id: gameId,
            timestamp: timestamp,
            date: new Date(timestamp * 1000).toISOString()
        };
    } catch (error) {
        console.error(`Error processing file ${file}:`, error);
        return null;
    }
}).filter(Boolean); // Remove any null entries from invalid files

// Sort by date (newest first)
recapsData.sort((a, b) => b.timestamp - a.timestamp);

// Update the index.html file with the recaps data
const indexPath = path.join(__dirname, 'index.html');
let indexContent = fs.readFileSync(indexPath, 'utf8');

// Replace the placeholder with the actual recaps data
indexContent = indexContent.replace(
    'const recapsData = [\n            // This will be populated by the build script\n        ];',
    `const recapsData = ${JSON.stringify(recapsData, null, 8)};`
);

fs.writeFileSync(indexPath, indexContent);
console.log('Build completed. Updated index.html with recaps data.');
