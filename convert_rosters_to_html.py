import re
import os

def parse_roster_file(file_path):
    """Parse the roster file and return a dictionary of teams with their players."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split content into team sections
    team_sections = re.split(r'^=== (.+?) ===$', content, flags=re.MULTILINE)
    
    teams = {}
    current_team = None
    
    for i in range(1, len(team_sections), 2):
        if i + 1 >= len(team_sections):
            break
            
        team_name = team_sections[i].strip()
        team_content = team_sections[i + 1].strip()
        
        # Skip empty teams
        if "No players found" in team_content:
            teams[team_name] = []
            continue
            
        # Extract player data
        players = []
        player_lines = [line.strip() for line in team_content.split('\n') if line.strip()]
        
        # Find the header line to determine column positions
        header_line = next((line for line in player_lines if 'PLAYER' in line and 'G' in line), None)
        if not header_line:
            continue
            
        # Extract column positions
        columns = []
        for match in re.finditer(r'\S+', header_line):
            columns.append((match.start(), match.group()))
        
        # Process player data
        for line in player_lines:
            if '----' in line or 'PLAYER' in line:
                continue
                
            # Extract player data based on column positions
            player_data = {}
            for j in range(len(columns)):
                start = columns[j][0]
                end = columns[j + 1][0] if j + 1 < len(columns) else None
                value = line[start:end].strip() if end else line[start:].strip()
                
                # Clean up the value
                if j == 0:  # Player name
                    player_data['name'] = value
                else:
                    # Try to convert numeric values to float
                    try:
                        player_data[columns[j][1].lower()] = float(value)
                    except ValueError:
                        player_data[columns[j][1].lower()] = value
            
            if player_data:
                players.append(player_data)
        
        teams[team_name] = players
    
    return teams

def generate_html(teams, output_file):
    """Generate HTML from the parsed team data."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Road to 25K Rosters</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .team-section {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow: hidden;
        }
        .team-header {
            background-color: #2c3e50;
            color: white;
            padding: 15px 20px;
            margin: 0;
            font-size: 1.5em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .no-players {
            padding: 20px;
            text-align: center;
            color: #777;
            font-style: italic;
        }
        .stat-highlight {
            font-weight: bold;
            color: #2c3e50;
        }
        @media (max-width: 768px) {
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Road to 25K Rosters</h1>
"""

    # Add team sections
    for team_name, players in teams.items():
        html += f'<div class="team-section">\n'
        if not players:
            html += f'<h2 class="team-header">{team_name}</h2>\n'
            html += '<div class="no-players">No players found</div>\n'
        else:
            html += f'<h2 class="team-header">{team_name}</h2>\n'
            html += '<div class="table-container">\n'
            html += '<table>\n<thead>\n<tr>\n'
            # Add table headers
            if players:
                for key in players[0].keys():
                    if key == 'name':
                        html += f'<th>Player</th>\n'
                    else:
                        html += f'<th>{key.upper()}</th>\n'
            html += '</tr>\n</thead>\n<tbody>\n'
            # Add player rows
            for player in players:
                html += '<tr>\n'
                for key, value in player.items():
                    if key == 'name':
                        html += f'<td class="player-name">{value}</td>\n'
                    elif isinstance(value, (int, float)):
                        # Format numbers with 1 decimal place if needed
                        if key in ['fg%', '3p%']:
                            formatted_value = f'{value:.1f}%'
                        else:
                            formatted_value = f'{value:.1f}'.rstrip('0').rstrip('.')
                        
                        # Highlight key stats
                        if key in ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'fg%', '3p%']:
                            html += f'<td class="stat-highlight">{formatted_value}</td>\n'
                        else:
                            html += f'<td>{formatted_value}</td>\n'
                    else:
                        html += f'<td>{value}</td>\n'
                html += '</tr>\n'
            html += '</tbody>\n</table>\n</div>\n'  # Close table and table-container

        html += '</div>\n'  # Close team-section

    # Close HTML
    html += """
    </div>
</body>
</html>
"""

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    input_file = 'road_to_25k_rosters.txt'
    output_file = 'rosters.html'
    
    print(f"Parsing {input_file}...")
    teams = parse_roster_file(input_file)
    
    print(f"Generating {output_file}...")
    generate_html(teams, output_file)
    
    print(f"Done! HTML file generated: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
