import requests
import pandas as pd

# === FPL API endpoint ===
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
data = requests.get(url).json()

# === Extract main tables ===
elements = pd.DataFrame(data['elements'])          # players
teams = pd.DataFrame(data['teams'])                # teams
positions = pd.DataFrame(data['element_types'])    # positions (GKP, DEF, MID, FWD)

# === Add team and position names ===
team_map = teams.set_index('id')['name'].to_dict()
pos_map = positions.set_index('id')['singular_name_short'].to_dict()

elements['team_name'] = elements['team'].map(team_map)
elements['position'] = elements['element_type'].map(pos_map)

# === Clean column names ===
elements.columns = elements.columns.str.lower()

# === Add readable price ===
elements['price'] = elements['now_cost'] / 10

# === Order useful columns first (then keep all others for flexibility) ===
cols_first = [
    'id', 'web_name', 'team_name', 'position', 'price', 'selected_by_percent',
    'total_points', 'event_points', 'form', 'points_per_game', 'minutes',
    'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
    'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards',
    'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index',
    'expected_goals', 'expected_assists', 'expected_goal_involvements',
    'expected_goals_conceded'
]

# Make sure we don’t drop any columns that exist in the dataset
cols_all = [c for c in cols_first if c in elements.columns] + \
            [c for c in elements.columns if c not in cols_first]

players = elements[cols_all]

# === Save to file ===
players.to_csv("fpl_full_data.csv", index=False)

print(f"✅ Pulled {len(players)} players, {len(players.columns)} columns.")
print("Columns:", list(players.columns))
print(players.head(5))
