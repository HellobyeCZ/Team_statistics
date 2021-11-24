import os
import pandas as pd
import numpy as np
import math


file_location = os.path.dirname(os.path.realpath(__file__))
file_location_lvl1 = os.path.dirname(file_location)
file_location_lvl2 = os.path.dirname(file_location_lvl1)
team_files_output = os.path.join(file_location_lvl1,"Teams")
team_files_source = os.path.join(file_location_lvl2,"Scrapper/Teams")


os.chdir(team_files_source)

teams_list = os.listdir()

if ".DS_Store" in teams_list:
    teams_list.remove(".DS_Store")

for team in teams_list:

    print(f"Preparing {team} - in progress")
    os.chdir(f"{team_files_source}/{team}/_final")

  

    FINAL_team_penalty_table = pd.read_csv("FINAL_team_penalty_table.csv", index_col=0)
    FINAL_opponent_penalty_table = pd.read_csv("FINAL_opponent_penalty_table.csv", index_col=0)
    FINAL_team_GK_table = pd.read_csv("FINAL_team_GK_table.csv", index_col=0)
    FINAL_opponent_GK_table = pd.read_csv("FINAL_opponent_GK_table.csv", index_col=0)
    FINAL_opponent_goal_table = pd.read_csv("FINAL_opponent_goal_table.csv", index_col=0)
    FINAL_team_goal_table = pd.read_csv("FINAL_team_goal_table.csv", index_col=0)
    FINAL_team_pts_table = pd.read_csv("FINAL_team_pts_table.csv", index_col=0)
    FINAL_opponent_pts_table = pd.read_csv("FINAL_opponent_pts_table.csv", index_col=0)
    FINAL_match_statistics = pd.read_csv("FINAL_match_statistics.csv", index_col=0)


    ### FINAL_TEAM_GK_TABLE
    FINAL_team_GK_table['GK'] = FINAL_team_GK_table['GK'].str.replace('\d+', '', regex=True)

    FINAL_team_GK_table["Min"] = FINAL_team_GK_table["Minutes"].str.replace(r'([0-9]{2}):[0-9]{2}', lambda m: m.group(1), regex=True)

    FINAL_team_GK_table = FINAL_team_GK_table.astype(
        {
            "Shots": int, 
            "Goals": int,
            "Touches": int,
            "Min": int
        }
    )

    pivot_team_GK_table = pd.pivot_table(FINAL_team_GK_table,
    index=['GK'],
    aggfunc={'Shots': np.sum, 'Goals': np.sum, 'Touches': np.sum, 'Id': len, 'Min': np.sum}
    ).sort_values("Id", ascending=False).rename(columns={'Id': 'Matches'})

    pivot_team_GK_table["Mean_Goals"] = np.where(pivot_team_GK_table['Matches']>= 5, round(pivot_team_GK_table['Goals']/pivot_team_GK_table['Matches'], ndigits=2), "-")
    pivot_team_GK_table["Goal_Minute"] = np.where(pivot_team_GK_table['Matches']>= 5, round(pivot_team_GK_table['Min']/pivot_team_GK_table['Goals'], ndigits=2), "-")


    ### FINAL_opponent_GK_table
    FINAL_opponent_GK_table['GK'] = FINAL_opponent_GK_table['GK'].str.replace('\d+', '', regex=True)

    FINAL_opponent_GK_table["Min"] = FINAL_opponent_GK_table["Minutes"].str.replace(r'([0-9]{2}):[0-9]{2}', lambda m: m.group(1), regex=True)

    FINAL_opponent_GK_table = FINAL_opponent_GK_table.astype(
        {
            "Shots": int, 
            "Goals": int,
            "Touches": int,
            "Min": int
        }
    )

    pivot_opponent_GK_table = pd.pivot_table(FINAL_opponent_GK_table,
    index=['GK'],
    aggfunc={'Shots': np.sum, 'Goals': np.sum, 'Touches': np.sum, 'Id': len, 'Min': np.sum}
    ).sort_values("Id", ascending=False).rename(columns={'Id': 'Matches'})

    pivot_opponent_GK_table["Mean_Goals"] = np.where(pivot_opponent_GK_table['Matches']>= 5, round(pivot_opponent_GK_table['Goals']/pivot_opponent_GK_table['Matches'], ndigits=2), "-")
    pivot_opponent_GK_table["Goal_Minute"] = np.where(pivot_opponent_GK_table['Matches']>= 5, round(pivot_opponent_GK_table['Min']/pivot_opponent_GK_table['Goals'], ndigits=2), "-")


    
    ### FINAL_team_goal_table

    FINAL_team_goal_table["Minute"] = FINAL_team_goal_table["Time"].str.replace(r'([0-9]{2}):[0-9]{2}(|\-)', lambda m: m.group(1), regex=True)
    FINAL_team_goal_table["Seconds"] = FINAL_team_goal_table["Time"].str.replace(r'[0-9]{2}:([0-9]{2})(|\-)', lambda m: m.group(1), regex=True)
    FINAL_team_goal_table["Period"] = FINAL_team_goal_table["Period"].str.replace(r'([0-9]{1})\..*', lambda m: m.group(1), regex=True)
    FINAL_team_goal_table['Minute'] = FINAL_team_goal_table['Minute'].str.replace('-', '0').astype(int)
    FINAL_team_goal_table['Seconds'] = FINAL_team_goal_table['Seconds'].str.replace('-', '0').astype(int)
    
    
    FINAL_team_goal_table["Seconds_all"] = FINAL_team_goal_table["Seconds"] + FINAL_team_goal_table["Minute"]*60

    FINAL_team_goal_table['Goal'] = FINAL_team_goal_table['Goal'].str.replace('\d+', '', regex=True)
    FINAL_team_goal_table['Assist'] = FINAL_team_goal_table['Assist'].str.replace('\d+', '', regex=True)

    ### FINAL_opponent_goal_table

    FINAL_opponent_goal_table["Minute"] = FINAL_opponent_goal_table["Time"].str.replace(r'([0-9]{2}):[0-9]{2}(|\-)', lambda m: m.group(1), regex=True)
    FINAL_opponent_goal_table["Seconds"] = FINAL_opponent_goal_table["Time"].str.replace(r'[0-9]{2}:([0-9]{2})(|\-)', lambda m: m.group(1), regex=True)
    FINAL_opponent_goal_table["Period"] = FINAL_opponent_goal_table["Period"].str.replace(r'([0-9]{1})\..*', lambda m: m.group(1), regex=True)
    FINAL_opponent_goal_table['Minute'] = FINAL_opponent_goal_table['Minute'].str.replace('-', '0').astype(int)
    FINAL_opponent_goal_table['Seconds'] = FINAL_opponent_goal_table['Seconds'].str.replace('-', '0').astype(int)
    
    
    FINAL_opponent_goal_table["Seconds_all"] = FINAL_opponent_goal_table["Seconds"] + FINAL_opponent_goal_table["Minute"]*60

    FINAL_opponent_goal_table['Goal'] = FINAL_opponent_goal_table['Goal'].str.replace('\d+', '', regex=True)
    FINAL_opponent_goal_table['Assist'] = FINAL_opponent_goal_table['Assist'].str.replace('\d+', '', regex=True)





    ### FINAL_team_pts_table

    FINAL_team_pts_table['Player'] = FINAL_team_pts_table['Player'].str.replace('\(O\)', '', regex=True)
    FINAL_team_pts_table['Player'] = FINAL_team_pts_table['Player'].str.replace('\(U\)', '', regex=True)
    FINAL_team_pts_table['Player'] = FINAL_team_pts_table['Player'].str.replace('\d+', '', regex=True)


    FINAL_team_pts_table["Hattrick"] = [math.floor(number/3) for number in FINAL_team_pts_table["G"]]





    pivot_team_pts_table = pd.pivot_table(FINAL_team_pts_table,
    index=['Player'],
    aggfunc={'G': np.sum, 'A': np.sum, 'PTS': np.sum, 'Id': len, 'Hattrick': np.sum}
    ).sort_values("Id", ascending=False).rename(columns={'Id': 'Matches'}).sort_values("PTS", ascending=False)


    pivot_team_pts_table["Mean_points"] = np.where(pivot_team_pts_table['Matches']>= 10, round(pivot_team_pts_table['PTS']/pivot_team_pts_table['Matches'], ndigits=2), "0")
    pivot_team_pts_table["Mean_goal"] = np.where(pivot_team_pts_table['Matches']>= 10, round(pivot_team_pts_table['G']/pivot_team_pts_table['Matches'], ndigits=2), "0")
    pivot_team_pts_table["Mean_assists"] = np.where(pivot_team_pts_table['Matches']>= 10, round(pivot_team_pts_table['A']/pivot_team_pts_table['Matches'], ndigits=2), "0")



    ### FINAL_opponent_pts_table

    FINAL_opponent_pts_table['Player'] = FINAL_opponent_pts_table['Player'].str.replace('\(O\)', '', regex=True)
    FINAL_opponent_pts_table['Player'] = FINAL_opponent_pts_table['Player'].str.replace('\(U\)', '', regex=True)
    FINAL_opponent_pts_table['Player'] = FINAL_opponent_pts_table['Player'].str.replace('\d+', '', regex=True)



    ###FINAL_match_statistics

    FINAL_match_statistics["Date"] = FINAL_match_statistics["Date_place"].str.replace(r'[a-zA-Z]+[\w].*([0-9]{2}\.[0-9]{2}\.[0-9]{4});.*', lambda m: m.group(1), regex=True)
    FINAL_match_statistics["Place"] = FINAL_match_statistics["Date_place"].str.replace(r'[a-zA-Z]+[\w].*[0-9]{2}\.[0-9]{2}\.[0-9]{4};(.*)', lambda m: m.group(1), regex=True)
    FINAL_match_statistics["Weekday"] = FINAL_match_statistics["Date_place"].str.replace(r'(.+[\w]).*[0-9]{2}\.[0-9]{2}\.[0-9]{4};.*', lambda m: m.group(1), regex=True)

    FINAL_match_statistics["ref1"] = FINAL_match_statistics["referee"].str.replace(r'rozhodčí:(.*),.*', lambda m: m.group(1), regex=True)
    FINAL_match_statistics["ref2"] = FINAL_match_statistics["referee"].str.replace(r'rozhodčí:.*,(.*)', lambda m: m.group(1), regex=True)
    
    FINAL_match_statistics["League"] = [value.split(";")[2] for value in FINAL_match_statistics["round_soutez"]]

    FINAL_match_statistics["MOTM"] = FINAL_match_statistics["MOTM"].str.replace(' \(U\)', '', regex=True)
    FINAL_match_statistics["MOTM"] = FINAL_match_statistics["MOTM"].str.replace(' \(O\)', '', regex=True)
    FINAL_match_statistics["MOTM"] = FINAL_match_statistics["MOTM"].str.replace('\d+', '', regex=True)
    FINAL_match_statistics["MOTM"] = FINAL_match_statistics["MOTM"].str.replace('Player\\n ', '', regex=True)
    FINAL_match_statistics["MOTM"] = FINAL_match_statistics["MOTM"].str.replace('\n ', '', regex=True)
    FINAL_match_statistics["MOTM_Team"] = FINAL_match_statistics["MOTM_Team"].str.replace(' \(U\)', '', regex=True)
    FINAL_match_statistics["MOTM_Team"] = FINAL_match_statistics["MOTM_Team"].str.replace(' \(O\)', '', regex=True)
    FINAL_match_statistics["MOTM_Team"] = FINAL_match_statistics["MOTM_Team"].str.replace('\d+', '', regex=True)
    FINAL_match_statistics["MOTM_Team"] = FINAL_match_statistics["MOTM_Team"].str.replace('Player\\n ', '', regex=True)
    FINAL_match_statistics["MOTM_Team"] = FINAL_match_statistics["MOTM_Team"].str.replace('\n ', '', regex=True)
    FINAL_match_statistics["MOTM_Opponent"] = FINAL_match_statistics["MOTM_Opponent"].str.replace(' \(U\)', '', regex=True)
    FINAL_match_statistics["MOTM_Opponent"] = FINAL_match_statistics["MOTM_Opponent"].str.replace(' \(O\)', '', regex=True)
    FINAL_match_statistics["MOTM_Opponent"] = FINAL_match_statistics["MOTM_Opponent"].str.replace('\d+', '', regex=True)
    FINAL_match_statistics["MOTM_Opponent"] = FINAL_match_statistics["MOTM_Opponent"].str.replace('Player\\n ', '', regex=True)
    FINAL_match_statistics["MOTM_Opponent"] = FINAL_match_statistics["MOTM_Opponent"].str.replace('\n ', '', regex=True)



    ###JOIN Dates and League
    FINAL_team_pts_table = pd.merge(FINAL_team_pts_table, FINAL_match_statistics[["Id","Date", "League"]], on="Id")



    ###FINAL_team_penalty_table
    FINAL_team_penalty_table['Player'] = FINAL_team_penalty_table['Player'].str.replace('\d+', '', regex=True)
    FINAL_team_penalty_table = FINAL_team_penalty_table[FINAL_team_penalty_table["Period"]!= "ŽÁDNÉ VYLOUČENÍ"]

    FINAL_team_penalty_table["TM"] = FINAL_team_penalty_table["TM"].replace({np.nan: 10})
    
    FINAL_team_penalty_table["TM"] = FINAL_team_penalty_table["TM"].astype(int)
    

    ###List all players
    ALL_Players = pd.DataFrame(np.unique(FINAL_team_pts_table["Player"]))

    os.chdir(f"{team_files_output}/{team}")

    pivot_team_GK_table.to_csv("pivot_team_GK_table.csv")
    pivot_opponent_GK_table.to_csv("pivot_opponent_GK_table.csv")
    FINAL_team_goal_table.to_csv("FINAL_team_goal_table.csv")
    FINAL_opponent_goal_table.to_csv("FINAL_opponent_goal_table.csv")
    FINAL_team_pts_table.to_csv("FINAL_team_pts_table.csv")
    pivot_team_pts_table.to_csv("pivot_team_pts_table.csv")
    FINAL_match_statistics.to_csv("FINAL_match_statistics.csv")
    FINAL_team_penalty_table.to_csv("FINAL_team_penalty_table.csv")
    ALL_Players.to_csv("ALL_Players.csv")


    print(f"Preparing {team} - DONE\n")

