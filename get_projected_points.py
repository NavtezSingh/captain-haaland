import pandas as pd
import requests
import numpy as np

# === Load players and fixtures (from your saved CSVs) ===
players = pd.read_csv("fpl_players_full.csv")
fixtures = pd.read_csv("fpl_fixtures.csv")

# === Keep only upcoming fixtures ===
fixtures = fixtures[fixtures['finished'] == False]

# --- Compute average fixture difficulty for each team (next 5 games) ---
fixture_difficulty = (
    fixtures
    .groupby('team_h_name')
    .apply(lambda x: x.head(5)['team_h_difficulty'].mean())
    .to_frame('avg_home_fdr')
    .join(
        fixtures.groupby('team_a_name')
        .apply(lambda x: x.head(5)['team_a_difficulty'].mean())
        .to_frame('avg_away_fdr'),
        how='outer'
    )
    .fillna(method='ffill')
)

fixture_difficulty['avg_fdr'] = fixture_difficulty[['avg_home_fdr', 'avg_away_fdr']].mean(axis=1)
fixture_difficulty = fixture_difficulty['avg_fdr'].to_dict()

# === Merge FDR with player data ===
players['fixture_difficulty'] = players['team_name'].map(fixture_difficulty)

# --- Normalize FDR (invert so lower FDR = easier fixtures) ---
players['fixture_factor'] = (6 - players['fixture_difficulty']) / 5

# --- Handle missing data ---
players = players.replace([np.inf, -np.inf], np.nan).fillna(0)

# === Calculate projected points ===
# Combines form, points per game, xG/xA (if available), and fixture ease
def project_points(row):
    base = 0
    if 'goals' in row and 'assists' in row:
        base = (float(row['goals']) + float(row['assists'])) * 2
    form = float(row.get('form', 0))
    ppg = float(row.get('points_per_game', 0))
    fdr = float(row.get('fixture_factor', 1))
    return (0.4 * form + 0.4 * ppg + 0.2 * base) * fdr

players['projected_points'] = players.apply(project_points, axis=1)

# Save results
players.to_csv("projected_points.csv", index=False)

print("✅ Calculated fixture-adjusted projected points for all players.")
print(players[['web_name', 'team_name', 'position', 'fixture_difficulty', 'projected_points']].head(10))
