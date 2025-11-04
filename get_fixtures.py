import requests
import pandas as pd

# === Base URLs ===
BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"

# === Fetch data ===
bootstrap = requests.get(BOOTSTRAP_URL).json()
fixtures = pd.DataFrame(requests.get(FIXTURES_URL).json())

# --- Extract tables from bootstrap ---
teams = pd.DataFrame(bootstrap['teams'])
positions = pd.DataFrame(bootstrap['element_types'])
elements = pd.DataFrame(bootstrap['elements'])

# --- Maps ---
team_map = teams.set_index('id')['name'].to_dict()
pos_map = positions.set_index('id')['singular_name_short'].to_dict()

# === PLAYER DATA ===
elements['team_name'] = elements['team'].map(team_map)
elements['position'] = elements['element_type'].map(pos_map)
elements['price'] = elements['now_cost'] / 10

players = elements.copy()
players.columns = players.columns.str.lower()
players.to_csv("fpl_players_full.csv", index=False)
print(f"✅ Saved {len(players)} players with {len(players.columns)} columns.")

# === FIXTURE DATA ===
fixtures['team_h_name'] = fixtures['team_h'].map(team_map)
fixtures['team_a_name'] = fixtures['team_a'].map(team_map)

fixtures_clean = fixtures[[
    'id', 'event', 'kickoff_time',
    'team_h_name', 'team_a_name',
    'team_h_difficulty', 'team_a_difficulty',
    'finished', 'team_h_score', 'team_a_score'
]]

fixtures_clean.to_csv("fpl_fixtures.csv", index=False)
print(f"✅ Saved {len(fixtures_clean)} fixtures with columns: {list(fixtures_clean.columns)}")

# === Example: Upcoming fixtures (not finished) ===
upcoming = fixtures_clean[fixtures_clean['finished'] == False].sort_values(['event', 'kickoff_time'])
print("\nUpcoming fixtures:")
print(upcoming.head(10))
