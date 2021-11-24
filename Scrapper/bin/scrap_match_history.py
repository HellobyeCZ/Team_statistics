import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import os



file_location = os.path.dirname(os.path.realpath(__file__))
file_location_lvl1 = os.path.dirname(file_location)
team_files_match = os.path.join(file_location_lvl1,"Teams")



os.chdir(team_files_match)

teams_list = os.listdir()

if ".DS_Store" in teams_list:
    teams_list.remove(".DS_Store")

for team in teams_list:

    print(f"Scrapping of {team} - in progress")
    os.chdir(f"{team_files_match}/{team}")

    url_list = pd.read_csv("url_list.csv")

    match_ids_all = pd.DataFrame(columns=["season","ID"])

    for l in url_list["ID_to_scrap"][0:-1]:

        url=f'https://www.ceskyflorbal.cz/druzstvo/{l}/zapasy'
        #Create a handle, page, to handle the contents of the website

        page = requests.get(url,timeout=1000)


        soup = BeautifulSoup(page.content, "html.parser")

        match_ids_list = re.findall('record_id=([0-9]+)&', str(soup))
        match_ids_unique = pd.unique(match_ids_list)
        season_scraped = re.findall("([0-9]{4}/[0-9]{4})", str(soup))

        match_iter = pd.DataFrame(columns=["season", "ID"])
        match_iter["ID"] = match_ids_unique
        match_iter["season"] = season_scraped[0]



        match_ids_all = match_ids_all.append(match_iter, ignore_index=True
        )


    match_ids_all.to_csv("match_ids_history.csv", index = None)
    print(f"Scrapping of {team} - DONE")


