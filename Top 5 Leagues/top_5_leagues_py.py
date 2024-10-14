# import libraries for data manipulation
import numpy as np
import pandas as pd

# import libraries for data visualization
import matplotlib.pyplot as plt
import seaborn as sns

#import libraries for statistical calculations
import scipy.stats as stats

import requests
from bs4 import BeautifulSoup

# to suppress warnings
import warnings
warnings.filterwarnings('ignore')

def generate_seasons_years(from_date, to_date):
    seasons_text = []
    for year in range(from_date, to_date):
        seasons_text.append(str(year) + "-" + str(year + 1))
    return seasons_text


def fill_data(global_dict, country, season, goals, empty_seasons_dictionary=None):
    if (country in global_dict.keys()):
        global_dict[country][season] += goals
        return   
    else:
        global_dict[country] = empty_seasons_dictionary.copy()
        fill_data(global_dict, country, season, goals)


def parse_and_fill(global_dict, url, season, empty_seasons_dictionary):
    # Step 1: Fetch the webpage content
    response = requests.get(url)

    # Step 2: Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 3: Locate the table containing the data (goal scorers, etc.)
    table = soup.find('table', class_='standard_tabelle')  # Look for the specific class used in the table

    # Step 4: Extract the data
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]  # Clean the text
        country = cols[3]
        goals = int(cols[5].rsplit(" ")[0])
        fill_data(global_dict, country, season, goals, empty_seasons_dictionary)
        
def get_urls(league, season):
    base_url = 'https://www.worldfootball.net/goalgetter/'
    urls = []
    if (league == "esp-primera-division" and season == "2016-2017"):
        urls.append(base_url + league + "-" + season + "_2/")
    elif (league == "esp-primera-division" and season == "1986-1987"):
        spain_leagues = ["esp-primera-division-1986-1987-playoff-1-6", "esp-primera-division-1986-1987-playoff-13-18", "esp-primera-division-1986-1987-playoff-7-12", "esp-primera-division-1986-1987-vorrunde"]
        for spain_league in spain_leagues:
            urls.append(base_url + spain_league + "/")  
    else:
        urls.append(base_url + league + "-" + season + "/")
    return urls


def create_empty_seasons_dictionary(seasons):
    seasons_dictionary = {} 
    for season in seasons:
        seasons_dictionary[season] = 0
    return seasons_dictionary
            
def extract_values_top_5_leagues(from_date, to_date):
    goals_per_nation_and_year = {}
    seasons = generate_seasons_years(int(from_date), int(to_date))
    empty_seasons_dictionary = create_empty_seasons_dictionary(seasons)
    leagues = ["eng-premier-league", "fra-ligue-1", "bundesliga", "ita-serie-a", "esp-primera-division"]
    
    for season in seasons:
        for league in leagues:
            urls = get_urls(league, season)
            for url in urls:
                parse_and_fill(goals_per_nation_and_year, url, season, empty_seasons_dictionary)
            
    return dict(sorted(goals_per_nation_and_year.items()))

final_dictionary = extract_values_top_5_leagues(1985,1988)
print(final_dictionary)
