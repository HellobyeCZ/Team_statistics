from re import match
from typing import Text
from numpy.core.defchararray import index
from pandas.core.frame import DataFrame
import streamlit as st
from datetime import datetime, time
from pickle import FALSE
from urllib import parse
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os



file_location = os.path.dirname(os.path.realpath(__file__))
file_location_lvl1 = os.path.dirname(file_location)
file_location_lvl2 = os.path.dirname(file_location_lvl1)
team_files_match = os.path.join(file_location_lvl1,"Teams")
scrapper_dir = os.path.join(file_location_lvl2,"Scrapper")
scrapper_bin_dir = os.path.join(scrapper_dir,"bin")

st.set_page_config(page_title="Team Statistics")

teams_list = os.listdir(team_files_match)

teams_list.insert(0, "Homepage")

if ".DS_Store" in teams_list:
    teams_list.remove(".DS_Store")

st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Please select a team", teams_list)

def load_players(team):
    data = pd.read_csv(f"{team_files_match}/{team}/ALL_Players.csv")["0"]
    return data

if app_mode != "Homepage":
    stat_type = st.sidebar.selectbox("Please select type of statistics",["Team statistics",
                                                                        "Players statistics",
                                                                        "Individual statistics"
                                                                        ])
    ALL_Players = load_players(app_mode)                                                                    
    if stat_type == "Individual statistics":
        player_name = st.sidebar.selectbox("Select player:", ALL_Players)




#@st.cache(persist=True, allow_output_mutation=True)
def load_data(team):
    data1 = pd.read_csv(f"{team_files_match}/{team}/FINAL_match_statistics.csv")
    data2 = pd.read_csv(f"{team_files_match}/{team}/FINAL_opponent_goal_table.csv")
    data3 = pd.read_csv(f"{team_files_match}/{team}/FINAL_team_goal_table.csv")
    data4 = pd.read_csv(f"{team_files_match}/{team}/FINAL_team_pts_table.csv")
    data5 = pd.read_csv(f"{team_files_match}/{team}/pivot_opponent_GK_table.csv")
    data6 = pd.read_csv(f"{team_files_match}/{team}/pivot_team_GK_table.csv")
    data7 = pd.read_csv(f"{team_files_match}/{team}/pivot_team_pts_table.csv")
    data8 = pd.read_csv(f"{team_files_match}/{team}/FINAL_team_penalty_table.csv")
    data9 = pd.read_csv(f"{team_files_match}/{team}/ALL_Players.csv")

    updated = str("Last update: " + datetime.today().strftime("%d/%m/%Y"))
    return data1, data2, data3, data4, data5, data6, data7, data8, data9, updated

def load_homepage() -> None:
    """ The homepage is loaded using a combination of .write and .markdown.
    Due to some issues with emojis incorrectly loading in markdown st.write was
    used in some cases.
    When this issue is resolved, markdown will be used instead.
    """
    
    #st.image(r"/Users/jakubhruska/Desktop/Team_stats/img/fbc_penguins_praha.jpg",
    #         use_column_width=True)
    st.title("Team statistics")
    st.header("Current scraped teams:")
    st.write("FBC Penguins Praha")
    st.write("FBC Mobydick Praha")
    st.write("FBC Ressler boys")

    st.title("")

    st.title("")

    st.title("")
    
    st.text("All information scraped from ceskyflorbal.cz")
    

    if st.button('Update teams'):
            os.chdir(scrapper_bin_dir)
            print(scrapper_bin_dir)
            os.system("python3 scrap_match_current.py")
            os.system("python3 scrap_stats_current.py")
            os.system("python3 current_history_append.py")
            os.chdir(file_location)
            os.system("python3 Prepare_data.py")
            os.chdir(file_location)
            os.system("streamlit cache clear")
            st.success('Teams successfuly updated!')

            if st.button("Rerun the App"):
                st.experimental_rerun()
            

    st.title("")

    st.title("")

    st.title("")
    st.write("Created by Jakub Hruška")
    #st.markdown("> ")
       #for i in range(3):
    #    st.write(" ")
    #st.header("🎲 The Application")
    #st.write("This application is a Streamlit dashboard hosted on Heroku that can be used to explore "
    #         "the results from board game matches that I tracked over the last year.")
    #st.write("There are currently four pages available in the application:")
    #st.subheader("♟ General Statistics ♟")
    #st.markdown("* This gives a general overview of the data including frequency of games over time, "


def load_team(which):

    if stat_type == "Individual statistics":

        st.title(f"{player_name}'s statistics")

    else:

        st.title(f"{app_mode} statistics")
        st.markdown("The dashboard will visualize the team statistics")

    match_statistics, opponent_goal_table, team_goal_table, team_pts_table, pivot_opponent_GK_table, pivot_team_GK_table, pivot_team_pts_table, FINAL_team_penalty_table, ALL_Players, updated = load_data(which)
    
    if stat_type == "Players statistics":


        st.header("Players")
        select = st.selectbox('Select what you want to visualise:',pivot_team_pts_table.columns[1:], index = 4)
        state_data = pivot_team_pts_table[["Player",select]].sort_values(select,ascending=False).head(40)


        state_total_graph = px.bar(
                state_data, 
                x='Player',
                y=select,
                template="plotly_dark")
            
        st.plotly_chart(state_total_graph)

        st.header("Goalkeepers")
        select = st.selectbox('Select what you want to visualise:',pivot_team_GK_table.columns[1:], index = 1)
        state_data = pivot_team_GK_table[["GK",select]].sort_values(select,ascending=False).head(20)
        
        state_total_graph = px.bar(
                state_data, 
                x='GK',
                y=select,
                template="plotly_dark")
            
        st.plotly_chart(state_total_graph)

        # st.header("Specials")
        # st.subheader("Hattricks")
        # state_total_graph = px.bar(
        #         hattricks, 
        #         x='Hraci',
        #         y="Hattrick",
        #         template="plotly_dark")
            
        # st.plotly_chart(state_total_graph)

        st.subheader("Statistics per match")

        col1, col2 = st.columns([4,1])

        with col1:
            select = st.selectbox('Select what you want to visualise:',[
                "Points",
                "Goals",
                "Assists"
            ])

        with col2:
            st.write("Click to filter")
            filter_indicator = st.checkbox("Filter")

        if select == "Points":
            data_match = team_pts_table[["Player", "PTS", "Team_against", "Date", "League"]]
            data_col = "PTS"
        elif select == "Goals":
            data_match = team_pts_table[["Player", "G", "Team_against", "Date", "League"]]
            data_col = "G"
        elif select == "Assists":
            data_match = team_pts_table[["Player", "A", "Team_against", "Date", "League"]]
            data_col = "A"


        data_match = data_match.rename(columns={'Team_against': 'Soupeř'})

        if filter_indicator:
            col1, col2 = st.columns(2)
            with col1:
                select_column = st.selectbox(
                    "Select what you want to filter:", data_match.columns[[0,2]])

            with col2:
                select_value = st.selectbox(
                    "Select value:", data_match[select_column].unique()
                )
            
            data_match = data_match[data_match[select_column]==select_value]
        
        st.dataframe(data_match.sort_values(data_match.columns[1], ascending=False))


        col1, col2 = st.columns([4,1])

        with col1:
            st.subheader("Statistics per season/team")
        with col2:
            st.write("Click to filter")
            filter_indicator_group = st.checkbox("Filter", key="32")

        col1, col2, col3 = st.columns(3)

        with col1:
            select_group = st.selectbox('Select what you want to visualise:',[
                "Points",
                "Goals",
                "Assists"
            ], key="1")

        with col2:
                Sum_or_mean = st.selectbox(
                    "Select value:", [
                        "Sum",
                        "Mean"
                    ]
                )
    

        if select_group == "Points":
            data_match_group = team_pts_table[["Player", "PTS", "Team_against", "Date", "League", "Season"]]
            data_col = "PTS"
        elif select_group == "Goals":
            data_match_group = team_pts_table[["Player", "G", "Team_against", "Date", "League", "Season"]]
            data_col = "G"
        elif select_group == "Assists":
            data_match_group = team_pts_table[["Player", "A", "Team_against", "Date", "League", "Season"]]
            data_col = "A"

        data_match_group = data_match_group.rename(columns={'Team_against': 'Soupeř'})

        with col3:
                select_column_group = st.selectbox(
                    "Select what you want to filter:", data_match_group.columns[[2,4,5]])


        
        
        if Sum_or_mean == "Sum":
            data_match_group = data_match_group.groupby([select_column_group, "Player"]).sum().sort_values(data_col, ascending=False).reset_index()
        elif Sum_or_mean == "Mean":
            data_match_group = data_match_group.groupby([select_column_group, "Player"]).mean().sort_values(data_col, ascending=False).reset_index()

        if filter_indicator_group:
            col1, col2 = st.columns(2)
            with col1:
                select_value1 = st.selectbox(
                    "Select value:", data_match_group.columns[[0,1]],
                    key="56"
                )
            with col2:
                select_value2 = st.selectbox(
                    "Select value:", data_match_group[select_value1].unique(),
                    key= "94"
                )
            data_match_group = data_match_group[data_match_group[select_value1]==select_value2]

        st.dataframe(data_match_group)


        st.subheader("Goals per minutes")

        goal_minutes = team_goal_table

        col1, col2 = st.columns([4,2])
        
        with col1:
            select_value_minutes = st.selectbox(
                    "Select name:", goal_minutes["Goal"].unique(),
                    key= "92"
                )
        with col2:
            select_value_groupby = st.selectbox(
                "Minute/period:", goal_minutes.columns[[8,2]]
            )

        if select_value_groupby == "Minute":
            goal_minutes = goal_minutes[goal_minutes["Goal"]==select_value_minutes].iloc[:,[5,8]]
        elif select_value_groupby == "Period":
            goal_minutes = goal_minutes[goal_minutes["Goal"]==select_value_minutes].iloc[:,[5,2]]
        
        goal_minutes = goal_minutes.groupby(select_value_groupby).count().reset_index()

        goal_minutes_graph = px.bar(
            goal_minutes, 
            x = select_value_groupby,
            y = "Goal",
            template = "plotly_dark"
            )
        
        st.plotly_chart(goal_minutes_graph)

        st.markdown(updated)
        
    elif stat_type == "Team statistics":
        st.header("Team statistics")
        # st.subheader("History")

        # historie["BV/Z"] = historie["BV"]/historie["Z"]
        # historie["BO/Z"] = historie["BO"]/historie["Z"]
        # historie["B/Z"] = historie["B"]/historie["Z"]
        # select_history = st.selectbox(
        #     "Select what you want to filter:", historie.columns[3:])

        # historie_plot = px.bar(
        #     historie, 
        #     x ='Sezóna',
        #     y = select_history,
        #     hover_name="Soutěž",
        #     template = "plotly_dark"
        #     )
        
        
        # st.plotly_chart(historie_plot)


        goal_scored = team_goal_table
        goal_conceded = opponent_goal_table
        all_matches = match_statistics

        
            

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Goals scored", len(goal_scored))
        with col2:
            st.metric("Goals conceded", len(goal_conceded))
        with col3:
            st.metric("Ratio", round(len(goal_scored)/len(goal_conceded),2))
        with col4:
            st.metric("Penalties", round(sum(FINAL_team_penalty_table.TM),2))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Matches played", len(all_matches))
        with col2:
            st.metric("Wins", len(all_matches[all_matches['Outcome'] == 'Win']))
        with col3:
            st.metric("Loses", len(all_matches[all_matches['Outcome'] == 'Lose']))
        with col4:
            st.metric("Prob. of win", f"{int(round(len(all_matches[all_matches['Outcome'] == 'Win'])/len(all_matches['Outcome']),2)*100)}%")

        st.subheader("")
        st.subheader("")

        with st.expander("Goals scored per minutes/period"):

            st.subheader("Goals scored per minutes/period")

            col1, col2= st.columns(2)

            
            with col1:
                select_goal_scored_groupby = st.selectbox(
                    "Minute/period:", goal_scored.columns[[8,2]],
                    key="214"
                )

            with col2:
                st.write("Apply filter")
                goal_scored_ind = st.checkbox("")


            if goal_scored_ind:
                
                goal_scored["Goals"] = 1

                select_goal_scored = st.selectbox(
                        "Select season:", goal_scored["Season"].unique(),
                        key= "93"
                    )
                

                if select_goal_scored_groupby == "Minute":
                    goal_scored = goal_scored[goal_scored["Season"]==select_goal_scored].iloc[:,[11,8]]
                elif select_goal_scored_groupby == "Period":
                    goal_scored = goal_scored[goal_scored["Season"]==select_goal_scored].iloc[:,[11,2]]
                
                goal_scored = goal_scored.groupby(select_goal_scored_groupby).count().reset_index()

                goal_scored_graph = px.bar(
                    goal_scored, 
                    x = select_goal_scored_groupby,
                    y = "Goals",
                    template = "plotly_dark"
                    )

                st.plotly_chart(goal_scored_graph)

            elif goal_scored_ind == False:
                
                goal_scored["Goals"] = 1

                if select_goal_scored_groupby == "Minute":
                    goal_scored = goal_scored.iloc[:,[11,8]]
                elif select_goal_scored_groupby == "Period":
                    goal_scored = goal_scored.iloc[:,[11,2]]


                
                goal_scored = goal_scored.groupby(select_goal_scored_groupby).count().reset_index()

                goal_scored_graph = px.bar(
                    goal_scored, 
                    x = select_goal_scored_groupby,
                    y = "Goals",
                    template = "plotly_dark"
                    )

                st.plotly_chart(goal_scored_graph)

        









        with st.expander("Goals conceded per minutes/period"):
            goal_conceded = opponent_goal_table
            st.subheader("Goals conceded per minutes/period")

            col1, col2 = st.columns(2)
            with col1:
                select_goal_conceded_groupby = st.selectbox(
                    "Minute/period:", goal_conceded.columns[[8,2]],
                    key="215"
                )

            with col2:
                st.write("Apply filter")
                goal_conceded_ind = st.checkbox("", key="asda")


            if goal_conceded_ind:
                
                goal_conceded["Goals"] = 1

                select_goal_conceded = st.selectbox(
                        "Select season:", goal_conceded["Season"].unique(),
                        key= "94"
                    )
                

                if select_goal_conceded_groupby == "Minute":
                    goal_conceded = goal_conceded[goal_conceded["Season"]==select_goal_conceded].iloc[:,[11,8]]
                elif select_goal_conceded_groupby == "Period":
                    goal_conceded = goal_conceded[goal_conceded["Season"]==select_goal_conceded].iloc[:,[11,2]]
                
                goal_conceded = goal_conceded.groupby(select_goal_conceded_groupby).count().reset_index()

                goal_conceded_graph = px.bar(
                    goal_conceded, 
                    x = select_goal_conceded_groupby,
                    y = "Goals",
                    template = "plotly_dark"
                    )

                st.plotly_chart(goal_conceded_graph)

            elif goal_conceded_ind == False:
                
                goal_conceded["Goals"] = 1

                if select_goal_conceded_groupby == "Minute":
                    goal_conceded = goal_conceded.iloc[:,[11,8]]
                elif select_goal_conceded_groupby == "Period":
                    goal_conceded = goal_conceded.iloc[:,[11,2]]


                
                goal_conceded = goal_conceded.groupby(select_goal_conceded_groupby).count().reset_index()

                goal_conceded_graph = px.bar(
                    goal_conceded, 
                    x = select_goal_conceded_groupby,
                    y = "Goals",
                    template = "plotly_dark"
                    )

                st.plotly_chart(goal_conceded_graph)

        st.subheader("")
        st.subheader("")
        st.subheader("Last 10 matches")
        st.dataframe(match_statistics[["Date", "Team", "Opponent", "Goal_team", "Goal_opponent", "Outcome", "Season", "League", "Place"]].tail(10).sort_index(ascending=False))

        

        st.subheader("")
        st.subheader("")
        st.subheader("Overview of Penalties")

        pivot_team_penalty_table = pd.pivot_table(FINAL_team_penalty_table,
            index=['Foul'],
            aggfunc={'TM': np.sum}
            ).sort_values("TM", ascending=False)

        Penalties_graph = px.bar(
                pivot_team_penalty_table, 
                x = pivot_team_penalty_table.index,
                y = "TM",
                template = "plotly_dark"
                )
        st.plotly_chart(Penalties_graph)

        pivot_team_penalty_table_player = pd.pivot_table(FINAL_team_penalty_table,
            index=['Player'],
            aggfunc={'TM': np.sum}
            ).sort_values("TM", ascending=False)

        Penalties_graph_player = px.bar(
                pivot_team_penalty_table_player, 
                x = pivot_team_penalty_table_player.index,
                y = "TM",
                template = "plotly_dark"
                )
        st.plotly_chart(Penalties_graph_player)

    elif stat_type == "Individual statistics":
        st.markdown("The site will visualize the player's statistics")

        player_team_pts_table = team_pts_table[team_pts_table["Player"]==player_name]
        player_penalty_table = FINAL_team_penalty_table[FINAL_team_penalty_table["Player"].str.replace('\\xa0', ' ')==player_name[:-1]]
        player_goal_table = team_goal_table[team_goal_table["Goal"].str.replace('\\xa0', ' ')==player_name[:-1]]
        player_goal_table["Gól"] = 1
        player_assist_table = team_goal_table[team_goal_table["Assist"].str.replace('\\xa0', ' ')==player_name[:-1]]
        player_assist_table["Asistence"] = 1

        try:
            pivot_player_team_pts_table = pd.pivot_table(player_team_pts_table,
                index=['Season'],
                aggfunc={'G': np.sum, 'A': np.sum, 'PTS': np.sum, "Id": len}
                ).sort_values("PTS", ascending=False).rename(columns={"Id":"Matches", "A": "Assists", "G": "Goals", "PTS": "Points"})
        except:
            pass

        #mott = match_statistics[match_statistics["MOTM_Team"]==player_name[:-1]]
        #motm = match_statistics[match_statistics["MOTM"]==player_name[:-1]]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Matches Played:", len(player_team_pts_table.index))
        with col2:
            st.metric("Goals:", sum(player_team_pts_table.G))
        with col3:
            st.metric("Assists:", sum(player_team_pts_table.A))
        with col4:
            st.metric("Points:", sum(player_team_pts_table.PTS))
            
        with st.expander("See more statistics"):
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Seasons Played:", len(np.unique(player_team_pts_table.Season)))
            with col2:
                st.metric("MAX Goals:", max(player_team_pts_table.G))
            with col3:
                st.metric("MAX Assists:", max(player_team_pts_table.A))
            with col4:
                st.metric("MAX Points:", max(player_team_pts_table.PTS))
            with col5:
                st.metric("Penalties (min):", sum(player_penalty_table["TM"].astype(int)))
            

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Hattricks:", sum(player_team_pts_table.Hattrick))
            with col2:
                st.metric("Mean Goals:", np.round(np.mean(player_team_pts_table.G),2))
            with col3:
                st.metric("Mean Assists:", np.round(np.mean(player_team_pts_table.A),2))
            with col4:
                st.metric("Mean Points:", np.round(np.mean(player_team_pts_table.PTS),2))
            with col5:
                st.metric("Goal participation:", f'{int(np.round(sum(player_team_pts_table.PTS)/sum(team_pts_table["G"]),2)*100)}%')

           
        with st.expander("See stats in seasons"):

            st.write("Most G/A/PTS in season")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Goals", max(pivot_player_team_pts_table["Goals"]), delta=pivot_player_team_pts_table[pivot_player_team_pts_table["Goals"] == max(pivot_player_team_pts_table["Goals"])].index[0], delta_color="off")
            with col2:
                st.metric("Assists", max(pivot_player_team_pts_table["Assists"]), delta=pivot_player_team_pts_table[pivot_player_team_pts_table["Assists"] == max(pivot_player_team_pts_table["Assists"])].index[0], delta_color="off")
            with col3:
                st.metric("Points", max(pivot_player_team_pts_table["Points"]), delta=pivot_player_team_pts_table[pivot_player_team_pts_table["Points"] == max(pivot_player_team_pts_table["Points"])].index[0], delta_color="off")


            #with col2:
                #st.metric("MOTT:", len(mott.index))

            #with col3:
                #st.metric("MOTM:", len(motm.index))

            

        player_team_pts_table["Góly"] = np.cumsum(player_team_pts_table["G"])
        player_team_pts_table["Asistence"] = np.cumsum(player_team_pts_table["A"])
        player_team_pts_table["Body"] = np.cumsum(player_team_pts_table["PTS"])
        player_team_pts_table = player_team_pts_table.reset_index()

        try:
            pivot_player_team_pts_table1 = pd.pivot_table(player_team_pts_table,
                index=['Player', 'Season'],
                aggfunc={'G': np.sum, 'A': np.sum, 'PTS': np.sum, "Id": len}
                ).sort_values("PTS", ascending=False).rename(columns={"Id":"Matches", "A": "Assists", "G": "Goals", "PTS": "Points"})
        except:
            pass

        try:
            player_penalty_graph = pd.pivot_table(player_penalty_table,
                index=['Foul'],
                aggfunc={'TM': np.sum}
                ).sort_values("TM", ascending=False)
        except:
            pass
        try:
            player_goal_graph = pd.pivot_table(player_goal_table,
                index=['Assist'],
                aggfunc={'Gól': np.sum}
                ).sort_values("Gól", ascending=False)
        except:
            pass
        try:
            player_assist_graph = pd.pivot_table(player_assist_table,
                index=['Goal'],
                aggfunc={'Asistence': np.sum}
                ).sort_values("Asistence", ascending=False)
        except:
            pass

        try:
            player_period_graph = pd.pivot_table(player_goal_table,
                index=['Period'],
                aggfunc={'Gól': np.sum}
                ).sort_values("Gól", ascending=False)
        except:
            pass

        try:        
            player_minute_graph = pd.pivot_table(player_goal_table,
                index=['Minute'],
                aggfunc={'Gól': np.sum}
                ).sort_values("Gól", ascending=False)
        except:
            pass 
        try:           
            player_period_graph_A = pd.pivot_table(player_assist_table,
                index=['Period'],
                aggfunc={'Asistence': np.sum}
                ).sort_values("Asistence", ascending=False)
        except:
            pass
        try:         
            player_minute_graph_A = pd.pivot_table(player_assist_table,
                index=['Minute'],
                aggfunc={'Asistence': np.sum}
                ).sort_values("Asistence", ascending=False)
        except:
            pass            

        st.subheader("Stats over time")
        try:
            st.line_chart(player_team_pts_table[["Góly","Asistence","Body"]])
        except:
            pass
        
        st.subheader("Stats in seasons")
        try:
            st.line_chart(pivot_player_team_pts_table.sort_index(ascending=True))
        except:
            pass

        with st.expander("Histogram of penalties"):
            st.subheader("Histogram of penalties")
            try:
                st.bar_chart(player_penalty_graph)
            except:
                pass
        
        with st.expander("Histogram of assists to/from players"):
            st.subheader("Histogram of getting assists from players")
            try:
                st.bar_chart(player_goal_graph)
            except:
                pass
            st.subheader("Histogram of assisting to other players")
            try:
                st.bar_chart(player_assist_graph)
            except:
                pass

        with st.expander("Histogram of scoring/assisting in minutes/period"):

            st.subheader("Histogram of scoring goals in periods")
            try:
                st.bar_chart(player_period_graph)
            except:
                pass
            st.subheader("Histogram of scoring goals in minutes")
            try:
                st.bar_chart(player_minute_graph)
            except:
                pass
            st.subheader("Histogram of assisting goals in periods")
            try:
                st.bar_chart(player_period_graph_A)
            except:
                pass
            st.subheader("Histogram of assisting goals in minutes")
            try:
                st.bar_chart(player_minute_graph_A)
            except:
                pass
        st.write("")


        with st.expander("See all stats in dataframe"):
            
            st.subheader("Match statistics")
            st.dataframe(player_team_pts_table.iloc[: , 2:].sort_index(ascending=False))
            st.subheader("Penalties")
            st.dataframe(player_penalty_table.iloc[: , 1:].sort_index(ascending=False))
            st.subheader("Goals")
            st.dataframe(player_goal_table.iloc[: , 1:].sort_index(ascending=False))
            st.subheader("Assists")
            st.dataframe(player_assist_table.iloc[: , 1:].sort_index(ascending=False))
            st.subheader("PTS/G/A over seasons")
            st.dataframe(pivot_player_team_pts_table1)
            
            #st.dataframe(mott)
            #st.markdown(repr(match_statistics["MOTM_Team"][0]))
            #st.markdown(repr(player_name[:-1]))

            
if app_mode == 'Homepage':
    load_homepage()
else:
    load_team(app_mode)




