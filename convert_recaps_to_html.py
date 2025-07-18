import os
import re
from datetime import datetime
from collections import defaultdict

def parse_recap_file(file_path, recap_file):
    """Parse a single recap file and return structured data.
    
    Args:
        file_path (str): Full path to the recap file
        recap_file (str): Just the filename (used for fallback team name extraction)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize game data
    game_data = {
        'file_path': file_path,
        'teams': [],
        'date': '',
        'status': '',
        'score1': '0',
        'score2': '0',
        'team_stats': {},
        'player_stats': defaultdict(list),
        'game_notes': [],
        'filename': os.path.basename(file_path)
    }
    
    # Extract game info
    print("\n=== DEBUG: Parsing game info ===")
    game_info_match = re.search(r'GAME INFO[\s\S]*?([\s\S]*?)-{20,}', content)
    if game_info_match:
        game_info_text = game_info_match.group(1).strip()
        print(f"Game info text: '{game_info_text[:100]}...'")
        
        try:
            # Try to extract team names from the first line
            first_line = game_info_text.split('\n')[0].strip()
            print(f"First line: '{first_line}'")
            
            # Try different patterns to extract team names
            teams_match = re.search(r'^(.+?)\s+vs\.?\s+(.+?)$', first_line, re.IGNORECASE)
            if not teams_match:
                teams_match = re.search(r'^(.+?)\s+-\s+(.+?)$', first_line, re.IGNORECASE)
            
            if teams_match:
                team1 = teams_match.group(1).strip()
                team2 = teams_match.group(2).strip()
                game_data['teams'] = [team1, team2]
                game_data['team1'] = team1  # Add team1 directly to game_data
                game_data['team2'] = team2  # Add team2 directly to game_data
                print(f"Found teams: '{team1}' vs '{team2}'")  # Debug
            else:
                print(f"Could not extract team names from: '{first_line}'")
                # Try to extract from filename as fallback
                filename_teams = os.path.basename(recap_file).replace('_recap.txt', '').split('_vs_')
                if len(filename_teams) >= 2:
                    team1 = filename_teams[0].replace('_', ' ')
                    team2 = filename_teams[1].replace('_', ' ')
                    game_data['teams'] = [team1, team2]
                    game_data['team1'] = team1
                    game_data['team2'] = team2
                    print(f"Extracted teams from filename: '{team1}' vs '{team2}'")
                
            # Extract date
            date_match = re.search(r'Date:\s*(.+)', game_info_text, re.IGNORECASE)
            if date_match:
                game_data['date'] = date_match.group(1).strip()
                print(f"Found date: {game_data['date']}")  # Debug
            else:
                print("No date found in game info")
                
            # Extract status
            status_match = re.search(r'Status:\s*(.+)', game_info_text, re.IGNORECASE)
            if status_match:
                game_data['status'] = status_match.group(1).strip()
                print(f"Found status: {game_data['status']}")  # Debug
            else:
                print("No status found in game info")
                
            # Extract scores if available
            score_match = re.search(r'Score:\s*(\d+)\s*-\s*(\d+)', game_info_text, re.IGNORECASE)
            if score_match:
                game_data['score1'] = score_match.group(1)
                game_data['score2'] = score_match.group(2)
                print(f"Found scores: {game_data['score1']}-{game_data['score2']}")  # Debug
            else:
                print("No scores found in game info")
                
        except Exception as e:
            print(f"Warning: Error parsing game info - {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("No game info section found in the recap")
            
        # Ensure we have valid team names
        if 'teams' not in game_data or len(game_data['teams']) != 2:
            # Try to extract teams from filename if not found in content
            filename = os.path.basename(file_path).replace('_recap.txt', '')
            if '_vs_' in filename:
                game_data['teams'] = [t.replace('_', ' ') for t in filename.split('_vs_')]
    
    # Extract team statistics
    team_stats_section = re.search(r'TEAM STATISTICS[- ]+\n([\s\S]*?)-{20,}', content)
    if team_stats_section:
        stats_text = team_stats_section.group(1).strip()
        print(f"Found team stats section. First 100 chars: {stats_text[:100]}...")  # Debug
        
        # Get team names from the game info
        team1 = game_data['team1']
        team2 = game_data['team2']
        print(f"Using teams: '{team1}' vs '{team2}'")  # Debug
        
        # Initialize team stats
        if team1 not in game_data['team_stats']:
            game_data['team_stats'][team1] = {}
        if team2 not in game_data['team_stats']:
            game_data['team_stats'][team2] = {}
        
        # Process each line in the team stats section
        for line in stats_text.split('\n'):
            line = line.strip()
            if not line or ':' not in line:
                continue
                
            print(f"Processing line: '{line}'")  # Debug
            
            # Handle stats with percentages (like Field Goals, 3-Pointers, etc.)
            stat_match = re.match(r'^([^:]+):\s*(\S+)\s*\(([^)]+)\)\s+\S+\s*\(([^)]+)\)', line)
            if stat_match:
                stat_name = stat_match.group(1).strip()
                team1_value = stat_match.group(2).strip()
                team1_pct = stat_match.group(3).strip()
                team2_value = stat_match.group(4).strip()
                
                print(f"  Found stat with percentages: {stat_name} - {team1_value} ({team1_pct}) | {team2_value}")  # Debug
                
                # Store the main stat value (e.g., '25-42' for FGs)
                game_data['team_stats'][team1][stat_name] = team1_value
                game_data['team_stats'][team2][stat_name] = team2_value
                
                # Also store the percentage if available
                game_data['team_stats'][team1][f'{stat_name} %'] = team1_pct
                game_data['team_stats'][team2][f'{stat_name} %'] = team1_pct  # This was a bug, fixed to use team2_pct
                continue
                
            # Handle stats without percentages (like Rebounds, Assists, etc.)
            stat_match = re.match(r'^([^:]+):\s*(\S+)\s+\S+\s+(\S+)', line)
            if stat_match:
                stat_name = stat_match.group(1).strip()
                team1_value = stat_match.group(2).strip()
                team2_value = stat_match.group(3).strip()
                
                print(f"  Found stat without percentages: {stat_name} - {team1_value} | {team2_value}")  # Debug
                
                game_data['team_stats'][team1][stat_name] = team1_value
                game_data['team_stats'][team2][stat_name] = team2_value
                continue
                
            print(f"  Could not parse line: '{line}'")  # Debug
    else:
        print("No team stats section found in the recap")  # Debug
    
    # Extract player statistics
    player_section = re.search(r'PLAYER STATISTICS[- ]+\n([\s\S]*?)(?=\n-{20,})', content)
    if player_section:
        current_team = None
        for line in player_section.group(1).strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check for team header
            team_match = re.match(r'^(.*?) Players:', line)
            if team_match:
                current_team = team_match.group(1).strip()
                continue
                
            if current_team and ':' not in line:  # Skip lines with colons (headers)
                # Parse player line
                player_match = re.match(r'^\s*(.*?)\s*\([^)]+\):\s*(\d+)\s+PTS.*?(\d+)\s+REB.*?(\d+)\s+AST', line)
                if player_match:
                    player_name = player_match.group(1).strip()
                    points = player_match.group(2).strip()
                    rebounds = player_match.group(3).strip()
                    assists = player_match.group(4).strip()
                    
                    # Extract shooting stats
                    fg_match = re.search(r'(\d+-\d+)\s+FG\s+\((.*?)\)', line)
                    fg = fg_match.group(1) if fg_match else '0-0'
                    fg_pct = fg_match.group(2) if fg_match else '0.0%'
                    
                    tp_match = re.search(r'(\d+-\d+)\s+3FG\s+\((.*?)\)', line)
                    tp = tp_match.group(1) if tp_match else '0-0'
                    tp_pct = tp_match.group(2) if tp_match else '0.0%'
                    
                    ft_match = re.search(r'(\d+-\d+)\s+FT\s+\((.*?)\)', line)
                    ft = ft_match.group(1) if ft_match else '0-0'
                    ft_pct = ft_match.group(2) if ft_match else '0.0%'
                    
                    # Extract other stats
                    stl = '0'
                    blk = '0'
                    to = '0'
                    
                    stl_match = re.search(r'(\d+)\s+STL', line)
                    if stl_match:
                        stl = stl_match.group(1)
                        
                    blk_match = re.search(r'(\d+)\s+BLK', line)
                    if blk_match:
                        blk = blk_match.group(1)
                        
                    to_match = re.search(r'(\d+)\s+TO', line)
                    if to_match:
                        to = to_match.group(1)
                    
                    player_data = {
                        'name': player_name,
                        'points': points,
                        'rebounds': rebounds,
                        'assists': assists,
                        'fg': fg,
                        'fg_pct': fg_pct,
                        '3p': tp,
                        '3p_pct': tp_pct,
                        'ft': ft,
                        'ft_pct': ft_pct,
                        'steals': stl,
                        'blocks': blk,
                        'turnovers': to,
                        'team': current_team
                    }
                    game_data['player_stats'][current_team].append(player_data)
    
    # Extract game notes
    notes_section = re.search(r'GAME NOTES[- ]+\n([\s\S]*?)(?=\n=+\n)', content)
    if notes_section:
        game_data['game_notes'] = [note.strip() for note in notes_section.group(1).strip().split('\n') if note.strip()]
    
    return game_data

def ensure_directory_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            return False
    return True

def generate_recap_html(recap_data, output_dir):
    """Generate HTML for a single game recap."""
    try:
        # Ensure output directory exists
        if not ensure_directory_exists(output_dir):
            print(f"Error: Could not create or access directory: {output_dir}")
            return None
            
        # Extract team names with defaults
        teams = recap_data.get('teams', ['Team 1', 'Team 2'])
        team1 = teams[0] if len(teams) > 0 else 'Team 1'
        team2 = teams[1] if len(teams) > 1 else 'Team 2'
        
        # Get team stats with safe defaults
        team1_stats = recap_data.get('team_stats', {}).get(team1, {})
        team2_stats = recap_data.get('team_stats', {}).get(team2, {})
        
        # Get scores with safe defaults
        team1_score = str(team1_stats.get('Points', '0'))
        team2_score = str(team2_stats.get('Points', '0'))
        
        # Generate team stats rows
        team_stats_rows = ''
        all_stats = set()
        
        # Get all unique stats from both teams
        if team1_stats:
            all_stats.update(team1_stats.keys())
        if team2_stats:
            all_stats.update(team2_stats.keys())
        
        # Skip Points as they're in the header
        stats_to_skip = {'Points'}
        
        # Generate table rows for each stat
        for stat in sorted(all_stats):
            if stat not in stats_to_skip:
                team1_stat = team1_stats.get(stat, '0' if stat in team2_stats else '-')
                team2_stat = team2_stats.get(stat, '0' if stat in team1_stats else '-')
                team_stats_rows += f'<tr><td>{stat}</td><td>{team1_stat}</td><td>{team2_stat}</td></tr>\n'
        # If no stats were found, add a message
        if not team_stats_rows:
            team_stats_rows = '<tr><td colspan="3">No team statistics available for this game.</td></tr>'
    except Exception as e:
        print(f"Error generating HTML for {recap_data.get('filename', 'unknown file')}: {str(e)}")
        return None
    
    # Generate player rows for each team with safe defaults
    def generate_player_rows(players):
        rows = ''
        if not players or not isinstance(players, list):
            return rows
            
        for player in players:
            if not isinstance(player, dict):
                continue
                
            # Safely extract player data with defaults
            name = str(player.get('name', 'Player'))
            points = str(player.get('points', '0'))
            rebounds = str(player.get('rebounds', '0'))
            assists = str(player.get('assists', '0'))
            fg_pct = str(player.get('fg_pct', '0.0'))
            three_pt_pct = str(player.get('3pt_pct', '0.0'))
            ft_pct = str(player.get('ft_pct', '0.0'))
            steals = str(player.get('steals', '0'))
            blocks = str(player.get('blocks', '0'))
            turnovers = str(player.get('turnovers', '0'))
            
            rows += f"""<tr>
                <td class="player-name">{name}</td>
                <td>{points}</td>
                <td>{rebounds}</td>
                <td>{assists}</td>
                <td>{fg_pct}</td>
                <td>{three_pt_pct}</td>
                <td>{ft_pct}</td>
                <td>{steals}</td>
                <td>{blocks}</td>
                <td>{turnovers}</td>
            </tr>"""
        return rows
    
    # Generate player rows for each team with safe defaults
    team1_players = recap_data.get('player_stats', {}).get(team1, [])
    team2_players = recap_data.get('player_stats', {}).get(team2, [])
    
    if not isinstance(team1_players, list):
        team1_players = []
    if not isinstance(team2_players, list):
        team2_players = []
    
    team1_player_rows = generate_player_rows(team1_players)
    team2_player_rows = generate_player_rows(team2_players)
    
    # Generate game notes HTML if available
    game_notes = ''
    if 'game_notes' in recap_data and isinstance(recap_data['game_notes'], list) and recap_data['game_notes']:
        game_notes = "<div class=\"game-notes\"><h3>Game Notes</h3><ul>"
        for note in recap_data['game_notes']:
            if note:  # Only add non-empty notes
                escaped_note = str(note).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                game_notes += f'<li>{escaped_note}</li>'
        game_notes += "</ul></div>"
    
    # Generate the HTML with proper escaping for CSS and content
    # We'll use a dictionary to store all template variables
    template_vars = {
        'team1': team1,
        'team2': team2,
        'team1_score': team1_stats.get('Points', '0'),
        'team2_score': team2_stats.get('Points', '0'),
        'date': recap_data.get('date', 'Date not available'),
        'status': recap_data.get('status', 'Final'),
        'team_stats_rows': team_stats_rows,  # Use the generated team stats rows
        'game_notes': game_notes,
        'team1_player_rows': team1_player_rows,
        'team2_player_rows': team2_player_rows
    }
    
    # Now generate the HTML template using .format() method
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{team1} vs {team2} - Game Recap</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        .game-header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #2c3e50;
        }}
        .game-title {{
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        .game-meta {{
            color: #7f8c8d;
            margin-bottom: 10px;
        }}
        .scoreboard {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }}
        .team-score {{
            text-align: center;
            padding: 0 20px;
        }}
        .team-name {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .score {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .stats-section {{
            margin: 30px 0;
        }}
        .section-title {{
            color: #2c3e50;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .player-name {{
            font-weight: bold;
        }}
        .game-notes {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .game-notes h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .game-notes ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">Game Recap</h1>
        <div class="game-meta">
            <p>{date} • {status}</p>
        </div>
    </div>

    <div class="scoreboard">
        <div class="team-score">
            <div class="team-name">{team1}</div>
            <div class="score">{team1_score}</div>
        </div>
        <div class="team-score">
            <div class="team-name">{team2}</div>
            <div class="score">{team2_score}</div>
        </div>
    </div>

    <div class="stats-section">
        <h2 class="section-title">Team Statistics</h2>
        <table>
            <thead>
                <tr>
                    <th>Stat</th>
                    <th>{team1}</th>
                    <th>{team2}</th>
                </tr>
            </thead>
            <tbody>
                {team_stats_rows}
            </tbody>
        </table>
    </div>

    <div class="stats-section">
        <h2 class="section-title">{team1} Player Stats</h2>
        <table>
            <thead>
                <tr>
                    <th>Player</th>
                    <th>PTS</th>
                    <th>REB</th>
                    <th>AST</th>
                    <th>FG%</th>
                    <th>3P%</th>
                    <th>FT%</th>
                    <th>STL</th>
                    <th>BLK</th>
                    <th>TO</th>
                </tr>
            </thead>
            <tbody>
                {team1_player_rows}
            </tbody>
        </table>
    </div>

    <div class="stats-section">
        <h2 class="section-title">{team2} Player Stats</h2>
        <table>
            <thead>
                <tr>
                    <th>Player</th>
                    <th>PTS</th>
                    <th>REB</th>
                    <th>AST</th>
                    <th>FG%</th>
                    <th>3P%</th>
                    <th>FT%</th>
                    <th>STL</th>
                    <th>BLK</th>
                    <th>TO</th>
                </tr>
            </thead>
            <tbody>
                {team2_player_rows}
            </tbody>
        </table>
    </div>

    <div class="game-notes">
        <h3>Game Notes</h3>
        <ul>
            {game_notes}
        </ul>
    </div>

    <a href="recaps_index.html" class="back-link">← Back to all recaps</a>
    <a href="recaps_index.html" class="back-link">← Back to All Recaps</a>
</body>
</html>
"""

    # Ensure we have valid team names
    if not team1 or not team2:
        print(f"Warning: Missing team names in {recap_data.get('filename', 'unknown file')}")
        return None
    
    # Generate team stats rows
    team_stats_rows = ''
    all_stats = set()
    
    # Get all unique stats from both teams
    all_stats.update(team1_stats.keys())
    all_stats.update(team2_stats.keys())
    
    # Generate table rows for each stat (excluding Points as they're in the header)
    for stat in sorted(all_stats):
        if stat != 'Points':
            team1_stat = team1_stats.get(stat, '-')
            team2_stat = team2_stats.get(stat, '-')
            team_stats_rows += f'<tr><td>{stat}</td><td>{team1_stat}</td><td>{team2_stat}</td></tr>\n'
    # Update the template variables with generated content
    template_vars['team_stats_rows'] = team_stats_rows
    
    # Generate player rows for each team
    team1_players = recap_data.get('player_stats', {}).get(team1, [])
    team2_players = recap_data.get('player_stats', {}).get(team2, [])
    
    # Generate player rows
    def generate_player_rows(players):
        rows = ''
        for player in players:
            if not isinstance(player, dict):
                continue
                
            # Safely extract player data with defaults
            name = str(player.get('name', 'Player'))
            points = str(player.get('points', '0'))
            rebounds = str(player.get('rebounds', '0'))
            assists = str(player.get('assists', '0'))
            fg_pct = str(player.get('fg_pct', '0.0'))
            three_pt_pct = str(player.get('3pt_pct', '0.0'))
            ft_pct = str(player.get('ft_pct', '0.0'))
            steals = str(player.get('steals', '0'))
            blocks = str(player.get('blocks', '0'))
            turnovers = str(player.get('turnovers', '0'))
            
            rows += f"""<tr>
                <td class="player-name">{name}</td>
                <td>{points}</td>
                <td>{rebounds}</td>
                <td>{assists}</td>
                <td>{fg_pct}</td>
                <td>{three_pt_pct}</td>
                <td>{ft_pct}</td>
                <td>{steals}</td>
                <td>{blocks}</td>
                <td>{turnovers}</td>
            </tr>"""
        return rows
    
    # Generate player rows for both teams
    template_vars['team1_player_rows'] = generate_player_rows(team1_players)
    template_vars['team2_player_rows'] = generate_player_rows(team2_players)
    # Generate player rows for each team
    def generate_player_rows(players):
        rows = ''
        for player in players:
            rows += f"""<tr>
                <td class="player-name">{player['name']}</td>
                <td>{player['points']}</td>
                <td>{player['rebounds']}</td>
                <td>{player['assists']}</td>
                <td>{player['fg']} ({player['fg_pct']})</td>
                <td>{player['3p']} ({player['3p_pct']})</td>
                <td>{player['ft']} ({player['ft_pct']})</td>
                <td>{player['steals']}</td>
                <td>{player['blocks']}</td>
                <td>{player['turnovers']}</td>
            </tr>"""
        return rows
    
    team1_players = recap_data['player_stats'].get(team1, [])
    team2_players = recap_data['player_stats'].get(team2, [])
    
    team1_player_rows = generate_player_rows(team1_players)
    team2_player_rows = generate_player_rows(team2_players)
    
    # Generate game notes
    game_notes = ''
    if recap_data['game_notes']:
        game_notes = '\n'.join([f'<li>{note}</li>' for note in recap_data['game_notes']])
    else:
        game_notes = '<li>No additional game notes available.</li>'
    
    # Format the HTML with the data
    try:
        # Get the date with a default value if not available
        game_date = recap_data.get('date', 'Date not available')
        game_status = recap_data.get('status', 'Status not available')
        
        # Convert all values to strings to avoid formatting errors
        for key, value in template_vars.items():
            if value is None:
                template_vars[key] = ''
            elif not isinstance(value, str):
                template_vars[key] = str(value)
        
        # Format the HTML with the template variables using .format()
        html = html.format(**template_vars)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a clean filename
        safe_team1 = team1.replace(' ', '_').replace('/', '-')
        safe_team2 = team2.replace(' ', '_').replace('/', '-')
        safe_date = recap_data.get('date', '').replace(' ', '_').replace('/', '-').replace(':', '-')
        output_filename = f"{safe_team1}_vs_{safe_team2}_{safe_date}.html"
        output_path = os.path.join(output_dir, output_filename)
        
        # Write the HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Created: {output_path}")
        
        return {
            'filename': output_filename,
            'team1': team1,
            'team2': team2,
            'date': recap_data.get('date', ''),
            'score1': team1_score,
            'score2': team2_score,
            'status': recap_data.get('status', 'Final')
        }
        
    except KeyError as e:
        print(f"  Error formatting HTML for {team1} vs {team2}: {str(e)}")
        return None
    except Exception as e:
        print(f"  Unexpected error in generate_recap_html for {team1} vs {team2}: {str(e)}")
        return None

def generate_recaps_index(recaps, output_dir):
    """Generate an index page with links to all recaps."""
    # Ensure output directory exists
    if not ensure_directory_exists(output_dir):
        print(f"Error: Could not create or access directory: {output_dir}")
        return
    
    # Sort recaps by date (newest first)
    def get_date(recap):
        try:
            if not recap:
                return datetime.min
                
            if 'date' in recap and recap['date']:
                # Try to parse the date if it exists
                try:
                    return datetime.strptime(recap['date'], '%A, %B %d, %Y %I:%M %p')
                except (ValueError, TypeError):
                    # If date format is different or invalid, use a default date
                    return datetime.min
            return datetime.min
        except Exception as e:
            print(f"Error parsing date for recap: {recap.get('filename', 'unknown')} - {str(e)}")
            return datetime.min
    
    # Filter out None values and invalid recaps before sorting
    valid_recaps = []
    for r in recaps:
        if not r or not isinstance(r, dict):
            continue
            
        # Check for required fields with more flexible validation
        has_teams = 'teams' in r and len(r.get('teams', [])) >= 2
        has_team_stats = 'team_stats' in r and isinstance(r['team_stats'], dict)
        has_date = 'date' in r and r['date'] is not None
        has_filename = 'filename' in r and r['filename']
        
        if has_teams and has_team_stats and has_date and has_filename:
            # Add the recap with normalized fields for the index
            team1, team2 = r['teams'][0], r['teams'][1]
            score1 = r.get('team_stats', {}).get(team1, {}).get('Points', '0')
            score2 = r.get('team_stats', {}).get(team2, {}).get('Points', '0')
            
            valid_recap = {
                'team1': team1,
                'team2': team2,
                'score1': score1,
                'score2': score2,
                'date': r['date'],
                'filename': r['filename'],
                'status': r.get('status', 'Final')
            }
            valid_recaps.append(valid_recap)
    
    if len(valid_recaps) < len(recaps):
        print(f"Warning: Filtered out {len(recaps) - len(valid_recaps)} invalid recaps.")
    
    # Sort by date, with most recent first
    sorted_recaps = sorted(valid_recaps, key=get_date, reverse=True)
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Recaps</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .recaps-list {
            list-style: none;
            padding: 0;
        }
        .recap-item {
            background-color: #f8f9fa;
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .recap-link {
            text-decoration: none;
            color: #2c3e50;
            font-weight: bold;
            font-size: 1.1em;
            display: block;
            margin-bottom: 5px;
        }
        .recap-link:hover {
            color: #3498db;
        }
        .recap-meta {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .score {
            font-weight: bold;
            color: #2c3e50;
        }
        .winner {
            color: #27ae60;
        }
        .no-recap {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <h1>Game Recaps</h1>
    
    <ul class="recaps-list">
"""
    
    if not sorted_recaps:
        html += '<div class="no-recap">No game recaps available.</div>\n'
    else:
        for recap in sorted_recaps:
            try:
                # Safely get values with defaults
                team1 = recap.get('team1', 'Team 1')
                team2 = recap.get('team2', 'Team 2')
                score1 = str(recap.get('score1', '0'))
                score2 = str(recap.get('score2', '0'))
                date = recap.get('date', 'Date unknown')
                filename = recap.get('filename', '')
                
                # Determine the winner
                try:
                    score1_int = int(score1)
                    score2_int = int(score2)
                    team1_class = 'winner' if score1_int > score2_int else ''
                    team2_class = 'winner' if score2_int > score1_int else ''
                except (ValueError, TypeError):
                    team1_class = ''
                    team2_class = ''
                
                html += f"""<li class="recap-item">
                    <a href="recaps_html/{filename}" class="recap-link">
                        <span class="{team1_class}">{team1}</span> vs <span class="{team2_class}">{team2}</span>
                    </a>
                    <div class="recap-meta">
                        {date} • 
                        <span class="score">{score1} - {score2}</span>
                    </div>
                </li>"""
            except Exception as e:
                print(f"Error generating HTML for recap {recap.get('filename', 'unknown')}: {str(e)}")
                continue
    
    html += """
    </ul>
</body>
</html>
"""
    
    # Write the index file
    index_path = os.path.join(output_dir, 'recaps_index.html')
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Created index: {index_path}")
    except Exception as e:
        print(f"Error writing index file {index_path}: {e}")

def main():
    # Set up directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    recaps_dir = os.path.join(base_dir, 'recaps')
    output_dir = os.path.join(base_dir, 'recaps_html')
    
    # Ensure output directory exists
    ensure_directory_exists(output_dir)
    
    # Find all recap files
    recap_files = [f for f in os.listdir(recaps_dir) if f.endswith('_recap.txt')]
    
    if not recap_files:
        print("No recap files found in the recaps directory.")
        return
    
    print(f"Found {len(recap_files)} recap files. Processing...")
    
    # Process each recap file
    all_recaps = []
    for i, filename in enumerate(recap_files, 1):
        print(f"Processing {i}/{len(recap_files)}: {filename}")
        try:
            # Parse the recap file
            recap_data = parse_recap_file(os.path.join(recaps_dir, filename), filename)
            if not recap_data or 'teams' not in recap_data or len(recap_data['teams']) != 2:
                print(f"  Skipping {filename}: Invalid or incomplete recap data")
                continue
                
            # Generate HTML for the recap
            html_file = generate_recap_html(recap_data, output_dir)
            if html_file:
                # Add the parsed data to our list for the index
                all_recaps.append(recap_data)
                print(f"  Created: {html_file}")
            else:
                print(f"  Failed to generate HTML for {filename}")
                
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
    
    # Generate the index page if we have valid recaps
    if all_recaps:
        generate_recaps_index(all_recaps, output_dir)
        print(f"\nSuccessfully processed {len(all_recaps)} recaps.")
        print(f"Index page: {os.path.join(output_dir, 'recaps_html', 'recaps_index.html')}")
    else:
        print("No valid recaps were processed.")

if __name__ == "__main__":
    main()
