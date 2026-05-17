import pandas as pd

# Load dataset
df = pd.read_csv("ipl_ball_by_ball.csv")

print("\nDATASET LOADED SUCCESSFULLY\n")

# -----------------------------------
# 1. Toss Win Analysis
# -----------------------------------

matches = df[["winner", "toss_winner"]].drop_duplicates()

matches["toss_match_win"] = matches["winner"] == matches["toss_winner"]

toss_win_percentage = (
    matches["toss_match_win"]
    .value_counts(normalize=True) * 100
)

print("TOSS WIN ANALYSIS")
print(toss_win_percentage)

# -----------------------------------
# 2. Top 5 Batters
# -----------------------------------

top_batters = (
    df.groupby("batter")["runs"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTOP 5 BATTERS")
print(top_batters)

# -----------------------------------
# 3. Top 5 Bowlers
# -----------------------------------

top_bowlers = (
    df.groupby("bowler")["wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTOP 5 BOWLERS")
print(top_bowlers)

# -----------------------------------
# 4. Phase Analysis
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

print("\nAVERAGE RUNS PER PHASE")
print(phase_runs)

print("\nANALYSIS COMPLETED SUCCESSFULLY!")