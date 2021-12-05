import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import os



file_location_smc = os.path.dirname(os.path.realpath(__file__))
file_location_smc_lvl1 = os.path.dirname(file_location_smc)
team_files_match = os.path.join(file_location_smc_lvl1,"Teams")



os.chdir(team_files_match)

teams_list = os.listdir()

if ".DS_Store" in teams_list:
    teams_list.remove(".DS_Store")

for team in teams_list:

    print(f"Scrapping of {team} - in progress")
    os.chdir(f"{team_files_match}/{team}")

    url_list = pd.read_csv("url_list.csv")

    match_ids_all = pd.DataFrame(columns=["season","ID"])

    last_id = url_list["ID_to_scrap"].iloc[-1]

    url=f'https://www.ceskyflorbal.cz/druzstvo/{last_id}/zapasy'
    #Create a handle, page, to handle the contents of the website

    page = requests.get(url,timeout=1000)


    soup = BeautifulSoup(page.content, "html.parser")

    soup_table = soup.find_all("div", class_="matches")

    match_ids_list = re.findall('record_id=([0-9]+)&', str(soup_table))
    match_ids_unique = pd.unique(match_ids_list)
    season_scraped = re.findall("([0-9]{4}/[0-9]{4})", str(soup))

    match_iter = pd.DataFrame(columns=["season", "ID"])
    match_iter["ID"] = match_ids_unique
    match_iter["season"] = season_scraped[0]



    match_ids_all = match_ids_all.append(match_iter, ignore_index=True
    )


    match_ids_all.to_csv("match_ids_current.csv", index = None)
    print(f"Scrapping of {team} - DONE\n")

os.chdir(file_location_smc)
