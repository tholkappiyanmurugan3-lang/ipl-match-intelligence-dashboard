import json
import pandas as pd
import os

print("LOADING DATASET...")

folder = "all_json"
balls = []

# -----------------------------------
# LOAD ALL MATCH FILES
# -----------------------------------
for file in os.listdir(folder):
    if file.endswith(".json") and file != "README.txt":

        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:
            match = json.load(f)

            if "innings" in match:

                for inning in match["innings"]:
                    if "overs" in inning:

                        for over in inning["overs"]:
                            for ball in over.get("deliveries", []):

                                # -----------------------------------
                                # SAFE RUN DATA EXTRACTION
                                # -----------------------------------
                                runs = ball.get("runs", {})
                                batter_runs = runs.get("batter", 0)

                                # -----------------------------------
                                # WICKET DETECTION (CORRECT WAY)
                                # -----------------------------------
                                wicket_flag = 0
                                if "wickets" in ball or "wicket" in ball:
                                    wicket_flag = 1

                                balls.append({
                                    "batter": ball.get("batter"),
                                    "bowler": ball.get("bowler"),
                                    "runs": batter_runs,
                                    "over": over.get("over"),
                                    "is_wicket": wicket_flag
                                })

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------
df = pd.DataFrame(balls)

print("DATA LOADED SUCCESSFULLY")
print("Rows:", len(df))

# -----------------------------------
# TOP 5 BATTERS
# -----------------------------------
print("\nTOP 5 BATTERS")

top_batters = (
    df.groupby("batter")["runs"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_batters)

# -----------------------------------
# TOP 5 BOWLERS (BY WICKETS)
# -----------------------------------
print("\nTOP 5 BOWLERS (by wickets)")

top_bowlers = (
    df.groupby("bowler")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_bowlers)

# -----------------------------------
# PHASE ANALYSIS
# -----------------------------------
print("\nPHASE ANALYSIS")

df["over"] = pd.to_numeric(df["over"], errors="coerce")

def get_phase(over):
    if pd.isna(over):
        return "Unknown"
    elif over <= 5:
        return "Powerplay"
    elif over <= 14:
        return "Middle Overs"
    else:
        return "Death Overs"

df["phase"] = df["over"].apply(get_phase)

phase_analysis = df.groupby("phase")["runs"].mean()

print(phase_analysis)

print("\nANALYSIS COMPLETE SUCCESSFULLY")