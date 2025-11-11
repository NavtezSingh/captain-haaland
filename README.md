# CaptainHaaland

> **Maximise your Fantasy Premier League points every Gameweek with data-driven optimisation.**

CaptainHaaland (or FPL Optimiser) is a Python-based tool that *selects the optimal 15-man FPL squad* using *fixture-adjusted projected points* and Linear Programming. It considers *budget, positions, club limits, and upcoming fixtures* to create a squad built for maximum points.

## Features

* Pulls live FPL data (players, stats, fixtures) from the official FPL API.
* Computes projected points using:

  * Form & Points per Game
  * Expected Goals (xG) and Assists (xA)
  * Upcoming fixture difficulty
* Linear Programming optimisation ensures:

  * Total squad cost ≤ £100m
  * Squad composition rules (2 GKP, 5 DEF, 5 MID, 3 FWD)
  * Max 3 players per club
* Outputs the optimal 15-man squad and projected points.
* Fixture-aware: prioritises players with easier upcoming matches.

---

## Installation

```bash
# Clone the repo
git clone https://github.com/NavtezSingh/CaptainHaaland.git
cd CaptainHaaland

# Install required Python packages
pip install pandas pulp requests numpy
```

---

## Usage

1. *Download FPL player & fixture data:*

```python
# Example: pull latest data
python fetch_fpl_data.py
```

2. *Calculate projected points (fixture-adjusted):*

```python
python calculate_projected_points.py
```

3. *Run the optimiser to get your squad:*

```python
python optimize_squad.py
```

4. *Output:*

* 15-man squad with projected points, position, team, and cost.
* Can be extended to choose *optimal starting XI & bench order*.

---

## How It Works

1. *Data Collection* – fetches latest stats and fixtures from the FPL API.
2. *Projected Points Calculation* – computes expected points per player factoring in form, xG/xA, and fixture difficulty.
3. *Optimisation Engine* – uses Linear Programming (PuLP) to maximise squad points under FPL constraints.
4. *Output* – generates a squad with budget, positional, and team constraints satisfied.

---

## Some Planned Features

* Automatic weekly squad optimization with live FPL updates.
* Optimal starting XI and bench order per Gameweek.
* Transfer planning & suggestions.
* Machine Learning-based projected points predictions.

---

## Dependencies

* Python 3.8+
* pandas
* numpy
* requests
* pulp

---

## Notes

* Fixture difficulty is weighted so easier matches boost projected points.
* Can be rerun weekly to reflect transfers, form changes, and fixture shifts.
* Fully customisable weights for form, xG/xA, and fixture difficulty.

---

## Contribution

Pull requests, bug fixes, and feature suggestions are welcome!
