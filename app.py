from flask import Flask, jsonify
from flask_cors import CORS
import json
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

print("LOADING DATASET...")

# -----------------------------------
# LOAD DATASET
# -----------------------------------
folder = "all_json"
balls = []

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

                                runs = ball.get("runs", {})

                                wicket_flag = 1 if ("wickets" in ball or "wicket" in ball) else 0

                                balls.append({
                                    "batter": ball.get("batter"),
                                    "bowler": ball.get("bowler"),
                                    "runs": runs.get("batter", 0),
                                    "over": over.get("over"),
                                    "is_wicket": wicket_flag
                                })

df = pd.DataFrame(balls)

print("DATA LOADED SUCCESSFULLY")
print("Rows:", len(df))

# -----------------------------------
# HOME ROUTE (FIX FOR NOT FOUND ERROR)
# -----------------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "IPL API is running 🚀",
        "available_routes": [
            "/top-batters",
            "/top-bowlers",
            "/phase-analysis"
        ]
    })

# -----------------------------------
# TOP BATTERS
# -----------------------------------
@app.route("/top-batters")
def top_batters():
    result = (
        df.groupby("batter")["runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .to_dict(orient="records")
    )
    return jsonify(result)

# -----------------------------------
# TOP BOWLERS
# -----------------------------------
@app.route("/top-bowlers")
def top_bowlers():
    result = (
        df.groupby("bowler")["is_wicket"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .to_dict(orient="records")
    )
    return jsonify(result)

# -----------------------------------
# PHASE ANALYSIS
# -----------------------------------
@app.route("/phase-analysis")
def phase_analysis():

    df["over"] = pd.to_numeric(df["over"], errors="coerce")

    def get_phase(over):
        if over <= 5:
            return "Powerplay"
        elif over <= 14:
            return "Middle Overs"
        else:
            return "Death Overs"

    df["phase"] = df["over"].apply(get_phase)

    result = (
        df.groupby("phase")["runs"]
        .mean()
        .reset_index()
        .to_dict(orient="records")
    )

    return jsonify(result)

# -----------------------------------
# RUN SERVER
# -----------------------------------


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)