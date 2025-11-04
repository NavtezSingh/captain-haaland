import pandas as pd
import pulp

# === Load player data ===
df = pd.read_csv("fpl_players_full.csv")

# Filter out players with zero minutes (not regulars)
df = df[df['minutes'] > 0]

# --- Add a simple projected_points column ---
# (We’ll make this smarter later using your model)
df['projected_points'] = (
    df['form'].astype(float) * 0.6 + df['points_per_game'].astype(float) * 0.4
)

# === Linear Programming Model ===
model = pulp.LpProblem("FPL_Optimization", pulp.LpMaximize)

# Binary decision variable for each player
x = pulp.LpVariable.dicts("select", df.index, cat="Binary")

# Objective function: maximize total projected points
model += pulp.lpSum(df.loc[i, "projected_points"] * x[i] for i in df.index)

# --- Constraints ---
# Budget ≤ 100
model += pulp.lpSum(df.loc[i, "price"] * x[i] for i in df.index) <= 100

# Total squad = 15 players
model += pulp.lpSum(x[i] for i in df.index) == 15

# Position limits
position_limits = {"GKP": 2, "DEF": 5, "MID": 5, "FWD": 3}
for pos, limit in position_limits.items():
    model += pulp.lpSum(x[i] for i in df.index if df.loc[i, "position"] == pos) == limit

# Max 3 players per team
for team in df['team_name'].unique():
    model += pulp.lpSum(x[i] for i in df.index if df.loc[i, "team_name"] == team) <= 3

# === Solve ===
print("Solving optimization problem...")
model.solve(pulp.PULP_CBC_CMD(msg=0))

# === Results ===
selected = df.loc[[i for i in df.index if pulp.value(x[i]) == 1]]
selected = selected[['web_name', 'team_name', 'position', 'price', 'projected_points', 'total_points', 'form']]
selected = selected.sort_values(by='position')

total_cost = selected['price'].sum()
total_proj = selected['projected_points'].sum()

print("\n🏆 Optimal Squad:")
print(selected.to_string(index=False))
print(f"\n💰 Total Cost: {total_cost:.1f} | 🔮 Projected Points: {total_proj:.1f}")
