import os
import pandas as pd
import requests
from bs4 import BeautifulSoup


file_location = os.path.dirname(os.path.realpath(__file__))
file_location_lvl1 = os.path.dirname(file_location)
team_files_match = os.path.join(file_location_lvl1,"Teams")



os.chdir(team_files_match)

teams_list = [input("Zadej tým: ")]

if ".DS_Store" in teams_list:
    teams_list.remove(".DS_Store")

for team in teams_list:
    os.chdir(f"{team_files_match}/{team}")

    match_id_list = pd.read_csv("match_ids_history.csv")


    match_statistics = pd.DataFrame(
        columns=[
            "Id",
            "Team",
            "Opponent",
            "Goal_team",
            "Goal_opponent",
            "Outcome",
            "Date_place",
            "visitors",
            "begin_end",
            "round_soutez",
            "casti_strely",
            "referee",
            "delegate",
            "MOTM_Team",
            "MOTM_Opponent",
            "MOTM",
            "Season"
        ]
    )

    team_goal_table = pd.DataFrame(
        columns=[
            "Id",
            "Period",
            "Time",
            "Type",
            "Goal",
            "Assist",
            "Season"
        ]
    )

    opponent_goal_table = pd.DataFrame(
        columns=[
            "Id",
            "Period",
            "Time",
            "Type",
            "Goal",
            "Assist",
            "Season"
        ]
    )

    team_penalty_table = pd.DataFrame(
        columns=[
            "Id",
            "Period",
            "Time",
            "Player",
            "TM",
            "Foul",
            "Season"
        ]
    )

    opponent_penalty_table = pd.DataFrame(
        columns=[
            "Id",
            "Period",
            "Time",
            "Player",
            "TM",
            "Foul",
            "Season"
        ]
    )


    team_GK_table = pd.DataFrame(
        columns=[
            "Id",
            "GK",
            "Shots",
            "Goals",
            "Touches",
            "Success%",
            "Minutes",
            "Season"
        ]
    )


    opponent_GK_table = pd.DataFrame(
        columns=[
            "Id",
            "GK",
            "Shots",
            "Goals",
            "Touches",
            "Success%",
            "Minutes",
            "Season"
        ]
    )


    team_pts_table = pd.DataFrame(
        columns=[
            "Id",
            "Player",
            "G",
            "A",
            "PTS",
            "Season",
            "Team_against",
            "Team_for"
        ]
    )


    opponent_pts_table = pd.DataFrame(
        columns=[
            "Id",
            "Player",
            "G",
            "A",
            "PTS",
            "Season",
            "Team_against",
            "Team_for"
        ]
    )

    for index, row in match_id_list.iterrows():
        

        url = f"https://fis.ceskyflorbal.cz/index.php?pageid=2519&onlycontent=1&record_id={row['ID']}&type=1"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="content")

        progress = len(match_id_list["ID"])-index
        print(f"Scraping - {team}\n...\n({progress} remaining) ({url})")





        l_goal_table = pd.DataFrame(
            columns=[
                "Id",
                "Period",
                "Time",
                "Type",
                "Goal",
                "Assist",
                "Season"
            ]
        )


        r_goal_table = pd.DataFrame(
            columns=[
                "Id",
                "Period",
                "Time",
                "Type",
                "Goal",
                "Assist",
                "Season"
            ]
        )


        l_penalty_table = pd.DataFrame(
            columns=[
                "Id",
                "Period",
                "Time",
                "Player",
                "TM",
                "Foul",
                "Season"
            ]
        )

        r_penalty_table = pd.DataFrame(
            columns=[
                "Id",
                "Period",
                "Time",
                "Player",
                "TM",
                "Foul",
                "Season"
            ]
        )


        l_GK_table = pd.DataFrame(
            columns=[
                "Id",
                "GK",
                "Shots",
                "Goals",
                "Touches",
                "Success%",
                "Minutes",
                "Season"
            ]
        )


        r_GK_table = pd.DataFrame(
            columns=[
                "Id",
                "GK",
                "Shots",
                "Goals",
                "Touches",
                "Success%",
                "Minutes",
                "Season"
            ]
        )


        l_pts_table = pd.DataFrame(
            columns=[
                "Id",
                "Player",
                "G",
                "A",
                "PTS",
                "Season",
                "Team_against",
                "Team_for"
            ]
        )


        r_pts_table = pd.DataFrame(
            columns=[
                "Id",
                "Player",
                "G",
                "A",
                "PTS",
                "Season",
                "Team_against",
                "Team_for"
            ]
        )





        match_summary = results.find_all("table", class_="match_summary")


        teams = match_summary[0].find_all("td", class_="stats_leftcol_TeamName")
        l_team = teams[0].text
        r_team = teams[1].text

        if l_team == team:
            team_preference = "Left"
        else:
            team_preference = "Right"

        goals = match_summary[0].find_all("td", class_="score")
        l_goal_summ = goals[0].text
        r_goal_summ = goals[1].text

        stats_centercol = match_summary[0].find_all("td", class_="stats_centercol")
        date_place = stats_centercol[0].text
        visitors = stats_centercol[1].text
        begin_end = stats_centercol[2].text
        round_soutez = stats_centercol[3].text
        casti_strely = stats_centercol[4].text
        referee = stats_centercol[5].text
        delegate = stats_centercol[6].text



        all_statstables = results.find_all("table", class_="statstable")



        statable_1a = all_statstables[0].find_all("tr")

        for stat in statable_1a[1:]:

            td = stat.find_all("td")
            l_period = td[1].text
            l_time = td[2].text
            l_type = td[3].text
            l_Goal = td[4].text
            l_Assist = td[5].text

            l_goal_table = l_goal_table.append(
                {
                    "Id": str(row["ID"]),
                    "Period":l_period,
                    "Time": l_time,
                    "Type": l_type,
                    "Goal": l_Goal,
                    "Assist": l_Assist,
                    "Season": row["season"]
                }, ignore_index=True
            )


        statable_1b = all_statstables[1].find_all("tr")

        for stat in statable_1b[1:]:

            td = stat.find_all("td")
            r_period = td[1].text
            r_time = td[2].text
            r_type = td[3].text
            r_Goal = td[4].text
            r_Assist = td[5].text

            r_goal_table = r_goal_table.append(
                {
                    "Id": str(row["ID"]),
                    "Period":r_period,
                    "Time": r_time,
                    "Type": r_type,
                    "Goal": r_Goal,
                    "Assist": r_Assist,
                    "Season": row["season"]
                }, ignore_index=True
            )



        statable_2a = all_statstables[2].find_all("tr")

        for stat in statable_2a[1:]:

            td = stat.find_all("td")

            try:
                l_period = td[1].text
                l_time = td[2].text
                l_player = td[3].text
                l_tm = td[4].text
                l_foul = td[5].text
            except:
                l_period = td[0].text
                l_time = td[0].text
                l_player = td[0].text
                l_tm = td[0].text
                l_foul = td[0].text

            l_penalty_table = l_penalty_table.append(
                {
                    "Id": str(row["ID"]),
                    "Period":l_period,
                    "Time": l_time,
                    "Player": l_player,
                    "TM": l_tm,
                    "Foul": l_foul,
                    "Season": row["season"]
                }, ignore_index=True
            )


        statable_2b = all_statstables[3].find_all("tr")

        for stat in statable_2b[1:]:

            td = stat.find_all("td")

            try:
                r_period = td[1].text
                r_time = td[2].text
                r_player = td[3].text
                r_tm = td[4].text
                r_foul = td[5].text
            except:
                r_period = td[0].text
                r_time = td[0].text
                r_player = td[0].text
                r_tm = td[0].text
                r_foul = td[0].text

            r_penalty_table = r_penalty_table.append(
                {
                    "Id": str(row["ID"]),
                    "Period":r_period,
                    "Time": r_time,
                    "Player": r_player,
                    "TM": r_tm,
                    "Foul": r_foul,
                    "Season": row["season"]
                }, ignore_index=True
            )



        statable_3a = all_statstables[4].find_all("tr")

        for stat in statable_3a[1:]:

            td = stat.find_all("td")
            l_GK = td[0].text
            l_shots = td[1].text
            l_goal = td[2].text
            l_touches = td[3].text
            l_success = td[4].text
            l_minutes = td[5].text

            l_GK_table = l_GK_table.append(
                {
                    "Id": str(row["ID"]),
                    "GK": l_GK,
                    "Shots": l_shots,
                    "Goals": l_goal,
                    "Touches": l_touches,
                    "Success%": l_success,
                    "Minutes": l_minutes,
                    "Season": row["season"]
                }, ignore_index=True
            )


        statable_3b = all_statstables[5].find_all("tr")

        for stat in statable_3b[1:]:

            td = stat.find_all("td")
            r_GK = td[0].text
            r_shots = td[1].text
            r_goal = td[2].text
            r_touches = td[3].text
            r_success = td[4].text
            r_minutes = td[5].text

            r_GK_table = r_GK_table.append(
                {
                    "Id": str(row["ID"]),
                    "GK": r_GK,
                    "Shots": r_shots,
                    "Goals": r_goal,
                    "Touches": r_touches,
                    "Success%": r_success,
                    "Minutes": r_minutes,
                    "Season": row["season"]
                }, ignore_index=True
            )



        statable_4a = all_statstables[6].find_all("tr")

        for stat in statable_4a[1:]:

            td = stat.find_all("td")
            l_player = td[0].text
            l_G = td[1].text
            l_A = td[2].text
            l_PTS = td[3].text

            l_pts_table = l_pts_table.append(
                {
                    "Id": str(row["ID"]),
                    "Player": l_player,
                    "G": l_G,
                    "A": l_A,
                    "PTS": l_PTS,
                    "Season": row["season"],
                    "Team_against": r_team,
                    "Team_for": l_team
                }, ignore_index=True
            )


        statable_4b = all_statstables[7].find_all("tr")

        for stat in statable_4b[1:]:

            td = stat.find_all("td")
            r_player = td[0].text
            r_G = td[1].text
            r_A = td[2].text
            r_PTS = td[3].text

            r_pts_table = r_pts_table.append(
                {
                    "Id": str(row["ID"]),
                    "Player": r_player,
                    "G": r_G,
                    "A": r_A,
                    "PTS": r_PTS,
                    "Season": row["season"],
                    "Team_against": l_team,
                    "Team_for": r_team
                }, ignore_index=True
            )



        l_temp_motm = l_pts_table[l_pts_table["PTS"]==max(l_pts_table["PTS"])]
        if len(l_temp_motm) != 1:
            l_temp_motm = l_temp_motm[l_temp_motm["G"]==max(l_temp_motm["G"])]
            if len(l_temp_motm) != 1:
                l_temp_motm = l_temp_motm[l_temp_motm["PTS"].astype(int)>=2]
        
        r_temp_motm = r_pts_table[r_pts_table["PTS"]==max(r_pts_table["PTS"])]
        if len(r_temp_motm) != 1:
            r_temp_motm = r_temp_motm[r_temp_motm["G"]==max(r_temp_motm["G"])]
            if len(r_temp_motm) != 1:
                r_temp_motm = r_temp_motm[r_temp_motm["PTS"].astype(int)>=2]


        both_pts_table = l_pts_table.append(
            r_pts_table
        )

        both_temp_motm = both_pts_table[both_pts_table["PTS"]==max(both_pts_table["PTS"])]
        if len(both_temp_motm) != 1:
            both_temp_motm = both_temp_motm[both_temp_motm["G"]==max(both_temp_motm["G"])]
            if len(both_temp_motm) != 1:
                both_temp_motm = both_temp_motm[both_temp_motm["PTS"].astype(int)>=2]



        if team_preference == "Left":

            if l_goal_summ>r_goal_summ:
                outcome = "Win"
            elif l_goal_summ<r_goal_summ:
                outcome = "Lose"
            else:
                outcome = "Draw"

            match_statistics = match_statistics.append(
                {
                    "Id": str(row["ID"]),
                    "Team": l_team,
                    "Opponent": r_team,
                    "Goal_team": l_goal_summ,
                    "Goal_opponent": r_goal_summ,
                    "Outcome": outcome,
                    "Date_place": date_place,
                    "visitors": visitors,
                    "begin_end": begin_end,
                    "round_soutez": round_soutez,
                    "casti_strely": casti_strely,
                    "referee": referee,
                    "delegate": delegate,
                    "MOTM_Team": l_temp_motm[["Player"]],
                    "MOTM_Opponent": r_temp_motm[["Player"]],
                    "MOTM": both_temp_motm[["Player"]],
                    "Season": row["season"]
                    }, ignore_index=True
            )



            team_goal_table = team_goal_table.append(l_goal_table)
            opponent_goal_table = opponent_goal_table.append(r_goal_table)
            team_penalty_table = team_penalty_table.append(l_penalty_table)
            opponent_penalty_table = opponent_penalty_table.append(r_penalty_table)
            team_GK_table = team_GK_table.append(l_GK_table)
            opponent_GK_table = opponent_GK_table.append(r_GK_table)
            team_pts_table = team_pts_table.append(l_pts_table)
            opponent_pts_table = opponent_pts_table.append(r_pts_table)
            


        

            





        if team_preference == "Right":

            if r_goal_summ>l_goal_summ:
                outcome = "Win"
            elif r_goal_summ<l_goal_summ:
                outcome = "Lose"
            else:
                outcome = "Draw"

            match_statistics = match_statistics.append(
                {
                    "Id": str(row["ID"]),
                    "Team": r_team,
                    "Opponent": l_team,
                    "Goal_team": r_goal_summ,
                    "Goal_opponent": l_goal_summ,
                    "Outcome": outcome,
                    "Date_place": date_place,
                    "visitors": visitors,
                    "begin_end": begin_end,
                    "round_soutez": round_soutez,
                    "casti_strely": casti_strely,
                    "referee": referee,
                    "delegate": delegate,
                    "MOTM_Team": r_temp_motm[["Player"]],
                    "MOTM_Opponent": l_temp_motm[["Player"]],
                    "MOTM": both_temp_motm[["Player"]],
                    "Season": row["season"]
                    }, ignore_index=True
                )


            team_goal_table = team_goal_table.append(r_goal_table)
            opponent_goal_table = opponent_goal_table.append(l_goal_table)
            team_penalty_table = team_penalty_table.append(r_penalty_table)
            opponent_penalty_table = opponent_penalty_table.append(l_penalty_table)
            team_GK_table = team_GK_table.append(r_GK_table)
            opponent_GK_table = opponent_GK_table.append(l_GK_table)
            team_pts_table = team_pts_table.append(r_pts_table)
            opponent_pts_table = opponent_pts_table.append(l_pts_table)


    os.chdir(team_files_match + f"/{team}/history")

    team_goal_table.to_csv("team_goal_table.csv")
    opponent_goal_table.to_csv("opponent_goal_table.csv")
    team_penalty_table.to_csv("team_penalty_table.csv")
    opponent_penalty_table.to_csv("opponent_penalty_table.csv")
    team_GK_table.to_csv("team_GK_table.csv")
    opponent_GK_table.to_csv("opponent_GK_table.csv")
    team_pts_table.to_csv("team_pts_table.csv")
    opponent_pts_table.to_csv("opponent_pts_table.csv")
    match_statistics.to_csv("match_statistics.csv")    

    print(f"\n\n{team} - scraping DONE\n\n")


