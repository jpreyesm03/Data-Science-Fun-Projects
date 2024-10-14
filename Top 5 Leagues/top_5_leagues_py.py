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

def fill_dictionary(dict, url, season):
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
        if (season in dict.keys()):
            if (country in dict[season].keys()):
                dict[season][country] += goals
            else:
                dict[season][country] = goals    
        else:
            dict[season] = {country : goals}
            
def extract_values_top_5_leagues(from_date, to_date):
    goals_per_nation_and_year = {}
    seasons = generate_seasons_years(int(from_date), int(to_date))
    leagues = ["eng-premier-league", "fra-ligue-1", "bundesliga", "ita-serie-a", "esp-primera-division"]
    base_url = 'https://www.worldfootball.net/goalgetter/'
    for season in seasons:
        for league in leagues:
            if (league == "esp-primera-division" and season == "2016-2017"):
                url = base_url + league + "-" + season + "_2/"
            else:
                url = base_url + league + "-" + season + "/"
            fill_dictionary(goals_per_nation_and_year, url, season)
    return goals_per_nation_and_year

final_dictionary = extract_values_top_5_leagues(2010,2020)
print(final_dictionary)
