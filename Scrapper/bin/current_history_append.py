import os
import pandas as pd


file_location = os.path.dirname(os.path.realpath(__file__))
file_location_lvl1 = os.path.dirname(file_location)
team_files_match = os.path.join(file_location_lvl1,"Teams")



os.chdir(team_files_match)

teams_list = os.listdir()

if ".DS_Store" in teams_list:
    teams_list.remove(".DS_Store")

for team in teams_list:

    print(f"Appending {team} - in progress")
    os.chdir(f"{team_files_match}/{team}/history")

    files_list = os.listdir()


    os.chdir(f"{team_files_match}/{team}")

    for file in files_list:

        history = pd.read_csv(f"history/{file}", index_col=0)
        current = pd.read_csv(f"current/{file}", index_col=0)

        final = history.append(current)

        final.to_csv(f"_final/FINAL_{file}")

    print(f"Appending {team} - DONE")

