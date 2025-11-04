import pandas as pd
import pulp

# === Load fixture-adjusted data ===
df = pd.read_csv("projected_points.csv")

# Filter out players with zero minutes or missing projections
df = df[df['minutes'] > 0]
df = df[df['projected_points'] > 0]

# === Linear Programming Model ===
model = pulp.LpProblem("FPL_Optimization", pulp.LpMaximize)

# Binary variable for each player
x = pulp.LpVariable.dicts("select", df.index, cat="Binary")

# Objective: maximize fixture-adjusted projected points
model += pulp.lpSum(df.loc[i, "projected_points"] * x[i] for i in df.index)

# Budget constraint
model += pulp.lpSum(df.loc[i, "price"] * x[i] for i in df.index) <= 100

# Squad size = 15
model += pulp.lpSum(x[i] for i in df.index) == 15

# Position limits
position_limits = {"GKP": 2, "DEF": 5, "MID": 5, "FWD": 3}
for pos, limit in position_limits.items():
    model += pulp.lpSum(x[i] for i in df.index if df.loc[i, "position"] == pos) == limit

# Team limit (≤ 3 players per team)
for team in df['team_name'].unique():
    model += pulp.lpSum(x[i] for i in df.index if df.loc[i, "team_name"] == team) <= 3

# === Solve ===
print("Solving optimization problem with fixture-adjusted projections...")
model.solve(pulp.PULP_CBC_CMD(msg=0))

# === Results ===
selected = df.loc[[i for i in df.index if pulp.value(x[i]) == 1]]
selected = selected[['web_name', 'team_name', 'position', 'price', 'projected_points']]
selected = selected.sort_values(by='position')

print("\n🏆 Optimal Squad (Fixture-Adjusted):")
print(selected.to_string(index=False))

print(f"\n💰 Total Cost: {selected['price'].sum():.1f}")
print(f"🔮 Total Projected Points: {selected['projected_points'].sum():.1f}")
