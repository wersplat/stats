import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def parse_team_stats(lines: List[str], start_idx: int) -> Tuple[Optional[Dict], int]:
    """Parse team statistics from the recap."""
    if start_idx >= len(lines):
        return None, start_idx
        
    stats = {}
    i = start_idx
    
    # Skip empty lines and section headers
    while i < len(lines) and isinstance(lines[i], str) and not lines[i].strip():
        i += 1
    
    # Parse team stats
    while i < len(lines) and isinstance(lines[i], str) and lines[i].strip() and '----------------' not in lines[i]:
        line = lines[i].strip()
        if ':' in line:
            stat_name, values = line.split(':', 1)
            stat_name = stat_name.strip()
            values = [v.strip() for v in values.split() if v.strip()]
            if values:  # Only add if we have values
                stats[stat_name] = values
        i += 1
    
    return stats, i

def parse_player_stat_line(line: str) -> Optional[Dict]:
    """Parse a player stat line into a dictionary."""
    if not isinstance(line, str):
        return None
        
    # Example line: "  Player (Team): 18 PTS, 1 REB, 8 AST"
    # Or: "    6-15 FG (40.0%), 5-10 3FG (50.0%), 0-0 FT (0.0%)"
    
    # Check if it's a stat line with player name
    if ':' in line and '(' in line and ')' in line and ':' < line.index('('):
        try:
            # Extract player name and team
            player_part, stats_part = line.split(':', 1)
            player_team = player_part.strip()
            
            # Extract stats
            stats = {}
            for stat in stats_part.split(','):
                stat = stat.strip()
                if not stat:
                    continue
                if 'PTS' in stat:
                    stats['PTS'] = stat.split('PTS')[0].strip()
                elif 'REB' in stat:
                    stats['REB'] = stat.split('REB')[0].strip()
                elif 'AST' in stat:
                    stats['AST'] = stat.split('AST')[0].strip()
                elif 'STL' in stat:
                    stats['STL'] = stat.split('STL')[0].strip()
                elif 'BLK' in stat:
                    stats['BLK'] = stat.split('BLK')[0].strip()
                elif 'TO' in stat and 'TOTAL' not in stat:
                    stats['TO'] = stat.split('TO')[0].strip()
            
            return {'type': 'player', 'player_team': player_team, 'stats': stats}
        except Exception as e:
            print(f"Error parsing player stat line: {line}")
            print(f"Error: {str(e)}")
            return None
    
    # Check if it's a shooting line
    elif any(x in line for x in ['FG', '3FG', 'FT']):
        return {'type': 'shooting', 'line': line.strip()}
    
    return None

def create_team_stats_table(team_stats: Dict, team1_name: str, team2_name: str) -> str:
    """Create a markdown table for team statistics."""
    if not team_stats:
        return ""
    
    # Define the order of stats to display
    stat_order = [
        'Rebounds', 'Offensive Rebounds', 'Defensive Rebounds',
        'Assists', 'Steals', 'Blocks', 'Turnovers', 'Fouls', 'Points',
        'True Shooting %', 'Assist/TO Ratio'
    ]
    
    # Filter and order the stats
    ordered_stats = []
    for stat in stat_order:
        if stat in team_stats:
            ordered_stats.append((stat, team_stats[stat]))
    
    # Create the table
    table = ["### Team Statistics\n"]
    
    # Table header
    table.append(f"| Stat | {team1_name} | {team2_name} |")
    table.append("|------|-------------|-------------|")
    
    # Table rows
    for stat, values in ordered_stats:
        if len(values) == 2:  # Ensure we have both team's stats
            table.append(f"| {stat} | {values[0]} | {values[1]} |")
    
    return "\n".join(table) + "\n\n"

def create_shooting_table(shooting_lines: List[str]) -> str:
    """Create a markdown table for player shooting stats."""
    if not shooting_lines:
        return ""
    
    table = ["### Shooting Statistics\n"]
    table.append("| Player | FG | FG% | 3PT | 3P% | FT | FT% |")
    table.append("|--------|----|-----|-----|-----|----|-----|")
    
    for line in shooting_lines:
        if not line.strip():
            continue
            
        # Extract player name if available
        if ':' in line:
            player_name = line.split(':', 1)[0].strip()
            line = line.split(':', 1)[1].strip()
        else:
            player_name = ""
        
        # Initialize stats
        fg_made, fg_attempted, fg_pct = "0", "0", "0.0%"
        fg3_made, fg3_attempted, fg3_pct = "0", "0", "0.0%"
        ft_made, ft_attempted, ft_pct = "0", "0", "0.0%"
        
        # Parse FG stats
        if 'FG' in line:
            fg_part = line.split('FG')[0].strip()
            if '-' in fg_part:
                fg_made, fg_attempted = fg_part.split('-')
                fg_made = fg_made.strip()
                fg_attempted = fg_attempted.strip()
                
                # Find FG percentage
                fg_pct_match = re.search(r'FG\s*\(([\d.]+)%\)', line)
                if fg_pct_match:
                    fg_pct = f"{fg_pct_match.group(1)}%"
        
        # Parse 3PT stats
        if '3FG' in line:
            fg3_part = line.split('3FG')[0].strip().split()[-1]
            if '-' in fg3_part:
                fg3_made, fg3_attempted = fg3_part.split('-')
                fg3_made = fg3_made.strip()
                fg3_attempted = fg3_attempted.strip()
                
                # Find 3PT percentage
                fg3_pct_match = re.search(r'3FG\s*\(([\d.]+)%\)', line)
                if fg3_pct_match:
                    fg3_pct = f"{fg3_pct_match.group(1)}%"
        
        # Parse FT stats
        if 'FT' in line:
            ft_part = line.split('FT')[0].strip().split()[-1]
            if '-' in ft_part:
                ft_made, ft_attempted = ft_part.split('-')
                ft_made = ft_made.strip()
                ft_attempted = ft_attempted.strip()
                
                # Find FT percentage
                ft_pct_match = re.search(r'FT\s*\(([\d.]+)%\)', line)
                if ft_pct_match:
                    ft_pct = f"{ft_pct_match.group(1)}%"
        
        # Add row to table
        table.append(
            f"| {player_name} | "
            f"{fg_made}-{fg_attempted} | {fg_pct} | "
            f"{fg3_made}-{fg3_attempted} | {fg3_pct} | "
            f"{ft_made}-{ft_attempted} | {ft_pct} |"
        )
    
    return "\n".join(table) + "\n\n"

def create_markdown_table(team_name: str, players: List[Dict]) -> str:
    """Create a markdown table for a team's players."""
    if not players:
        return ""
    
    # Table header
    headers = ['Player', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']
    table = [f"### {team_name} Players\n"]
    
    # Table header row
    table.append("|" + "|".join(headers) + "|")
    table.append("|" + "|".join(["---"] * len(headers)) + "|")
    
    # Player rows
    for player in players:
        if player['type'] == 'player':
            row = [player['player_team']]
            for stat in headers[1:]:  # Skip 'Player' column
                row.append(player['stats'].get(stat, '0'))
            table.append("|" + "|".join(row) + "|")
    
    return "\n".join(table) + "\n"

def extract_team_names(lines: List[str]) -> Tuple[str, str]:
    """Extract team names from the game info section."""
    for line in lines:
        if isinstance(line, str) and ' vs ' in line and 'GAME INFO' not in line and '--------------------' not in line:
            parts = line.split(' vs ')
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
    return "Team 1", "Team 2"

def convert_to_markdown(input_file: str) -> Tuple[bool, str]:
    """Convert a single recap file to markdown format with tables for stats."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines() if line.strip()]
        
        # Extract team names
        team1_name, team2_name = extract_team_names(lines)
        
        # Create markdown content
        md_content = [f"# {os.path.basename(input_file).replace('_recap.txt', '')}\n"]
        
        current_section = []
        current_team = None
        players = []
        team_stats = {}
        in_team_stats = False
        in_player_stats = False
        shooting_lines = []
        game_notes = []
        
        i = 0
        while i < len(lines):
            if not isinstance(lines[i], str):
                i += 1
                continue
                
            line = lines[i].strip()
            
            # Check for team stats section
            if 'TEAM STATISTICS' in line:
                in_team_stats = True
                team_stats, new_i = parse_team_stats(lines, i + 1)
                if new_i > i:  # Ensure we make progress
                    i = new_i
                else:
                    i += 1
                continue
                
            # Check for player stats section
            if 'PLAYER STATISTICS' in line:
                in_player_stats = True
                in_team_stats = False
                i += 1
                continue
                
            # Check for game notes section
            if 'GAME NOTES' in line:
                game_notes = [l for l in lines[i:] if isinstance(l, str) and l.strip()]
                break
            
            # Process player stats if in player stats section
            if in_player_stats and line and '----------------' not in line:
                if 'Players:' in line:
                    # If we have players collected, create a table for them
                    if players:
                        md_content.append(create_markdown_table(current_team, players))
                        if shooting_lines:
                            md_content.append(create_shooting_table(shooting_lines))
                            shooting_lines = []
                        players = []
                    current_team = line.replace('Players:', '').strip()
                else:
                    # Parse player stats
                    player_data = parse_player_stat_line(lines[i])
                    if player_data:
                        if player_data['type'] == 'shooting':
                            # Combine with previous player's stats if available
                            if players and players[-1]['type'] == 'player':
                                players[-1]['shooting'] = player_data['line']
                                shooting_lines.append(f"{players[-1]['player_team']}: {player_data['line']}")
                            else:
                                shooting_lines.append(player_data['line'])
                        else:
                            players.append(player_data)
                i += 1
                continue
                
            # Add non-empty lines to current section
            if line:
                current_section.append(lines[i])
            
            # If we hit a section break, add the current section to markdown
            if not line and current_section:
                # Add team stats table if we just finished the team stats section
                if in_team_stats and team_stats:
                    md_content.append(create_team_stats_table(team_stats, team1_name, team2_name))
                    in_team_stats = False
                
                # Add the current section
                md_content.append("\n".join(current_section) + "\n")
                current_section = []
            
            i += 1
        
        # Add any remaining players
        if players and current_team:
            md_content.append(create_markdown_table(current_team, players))
            if shooting_lines:
                md_content.append(create_shooting_table(shooting_lines))
        
        # Add any remaining section
        if current_section:
            md_content.append("\n".join(current_section) + "\n")
        
        # Add game notes if any
        if game_notes:
            md_content.append("\n".join(game_notes) + "\n")
        
        # Create output filename
        output_file = input_file.replace('.txt', '.md')
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write("\n".join(md_content).strip() + "\n")
            
        return True, output_file
    except Exception as e:
        return False, str(e)

def process_recaps():
    """Process all recap files in the recaps directory."""
    recaps_dir = os.path.join(os.path.dirname(__file__), 'recaps')
    target_teams = [
        'Breakout Gaming', 'High Octane', 'On Site', 
        'Liquid Pro-Am', 'State Mafia', 'Bodega Cats'
    ]
    
    # Create a pattern to match any of the target teams
    pattern = '|'.join(re.escape(team) for team in target_teams)
    
    # Find all recap files
    recaps = []
    for root, _, files in os.walk(recaps_dir):
        for file in files:
            if file.endswith('_recap.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(pattern, content, re.IGNORECASE):
                            recaps.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
    
    # Convert each recap
    success_count = 0
    for recap in recaps:
        success, result = convert_to_markdown(recap)
        if success:
            print(f"Converted: {os.path.basename(result)}")
            success_count += 1
        else:
            print(f"Failed to convert {os.path.basename(recap)}: {result}")
    
    print(f"\nConversion complete. Successfully converted {success_count}/{len(recaps)} files.")

if __name__ == "__main__":
    process_recaps()
