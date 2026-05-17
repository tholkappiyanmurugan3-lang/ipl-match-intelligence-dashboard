import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("ipl_ball_by_ball.csv")

# -----------------------------------
# Toss Win Analysis
# -----------------------------------

matches = df[["winner", "toss_winner"]].drop_duplicates()

matches["toss_match_win"] = matches["winner"] == matches["toss_winner"]

toss_result = (
    matches["toss_match_win"]
    .value_counts()
)

plt.figure(figsize=(6,6))
plt.pie(
    toss_result,
    labels=["Lost Match", "Won Match"],
    autopct='%1.1f%%'
)

plt.title("Toss Winner vs Match Winner")
plt.savefig("toss_analysis.png")

# -----------------------------------
# Top Batters
# -----------------------------------

top_batters = (
    df.groupby("batter")["runs"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

plt.figure(figsize=(8,5))
top_batters.plot(kind="bar")

plt.title("Top 5 Batters")
plt.xlabel("Batters")
plt.ylabel("Runs")

plt.tight_layout()
plt.savefig("top_batters.png")

# -----------------------------------
# Top Bowlers
# -----------------------------------

top_bowlers = (
    df.groupby("bowler")["wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

plt.figure(figsize=(8,5))
top_bowlers.plot(kind="bar")

plt.title("Top 5 Bowlers")
plt.xlabel("Bowlers")
plt.ylabel("Wickets")

plt.tight_layout()
plt.savefig("top_bowlers.png")

# -----------------------------------
# Phase Analysis
# -----------------------------------

def get_phase(over):

    if over <= 5:
        return "Powerplay"

    elif over <= 14:
        return "Middle Overs"

    else:
        return "Death Overs"

df["phase"] = df["over"].apply(get_phase)

phase_runs = (
    df.groupby("phase")["runs"]
    .mean()
)

plt.figure(figsize=(7,5))
phase_runs.plot(kind="bar")

plt.title("Average Runs Per Phase")
plt.xlabel("Phase")
plt.ylabel("Average Runs")

plt.tight_layout()
plt.savefig("phase_analysis.png")

print("ALL CHARTS CREATED SUCCESSFULLY!")