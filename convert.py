import json
import pandas as pd
import os

# Current project directory
base_dir = os.path.dirname(__file__)

# JSON folder path
folder_path = os.path.join(base_dir, "all_json")

# Store all ball-by-ball data
all_data = []

# Read all JSON files
for file in os.listdir(folder_path):

    if file.endswith(".json"):

        file_path = os.path.join(folder_path, file)

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

            info = data.get("info", {})
            innings = data.get("innings", [])

            winner = info.get("outcome", {}).get("winner", "No Result")
            toss_winner = info.get("toss", {}).get("winner", "Unknown")
            match_date = info.get("dates", [""])[0]

            # Process innings
            for inning in innings:

                team = inning.get("team", "")
                overs = inning.get("overs", [])

                # Process overs
                for over in overs:

                    over_num = over.get("over", 0)
                    deliveries = over.get("deliveries", [])

                    # Process deliveries
                    for delivery in deliveries:

                        batter = delivery.get("batter", "")
                        bowler = delivery.get("bowler", "")

                        runs = delivery.get("runs", {}).get("batter", 0)

                        wicket = 1 if "wickets" in delivery else 0

                        all_data.append({
                            "match_date": match_date,
                            "team": team,
                            "batter": batter,
                            "bowler": bowler,
                            "over": over_num,
                            "runs": runs,
                            "wicket": wicket,
                            "winner": winner,
                            "toss_winner": toss_winner
                        })

# Create DataFrame
df = pd.DataFrame(all_data)

# Save CSV
output_path = os.path.join(base_dir, "ipl_ball_by_ball.csv")

df.to_csv(output_path, index=False)

print("CSV CREATED SUCCESSFULLY!")
print("Total Records:", len(df))
print("Saved at:", output_path)