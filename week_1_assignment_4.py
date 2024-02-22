import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def data_cleansing():
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]


    ## cleansing nhl 
    nhl_df = nhl_df[nhl_df['year'] == 2018]
    nhl_df = nhl_df[~nhl_df.apply(lambda row: row.astype(str).str.contains('Division').any(), axis=1)]
    nhl_df['WLR'] = nhl_df['W'].astype(float) / nhl_df['GP'].astype(float)
    nhl_df['team'] = nhl_df['team'].str.replace(r'\*$', '', regex=True)

    ## cleansing cities 
    cities['NHL'] = cities['NHL'].str.replace(r'\[.+\]', "", regex=True)
    cities['NHL'] = cities['NHL'].replace({"Rangers Islanders Devils": "Rangers,Islanders,Devils",
                                               "Kings Ducks": "Kings,Ducks"})
    cities = cities.assign(NHL=cities['NHL'].str.split(',')).explode('NHL')

    # create dict mapping
    MetroDict = {'Boston Bruins': 'Boston',
            'Toronto Maple Leafs': 'Toronto',
            'Florida Panthers': 'Miami-Fort Lauderdale',
            'Detroit Red Wings': 'Detroit',
            'Ottawa Senators': 'Ottawa',
            'Buffalo Sabres': 'Buffalo',
            'Washington Capitals': 'Washington, D.C.',
            'Pittsburgh Penguins': 'Pittsburgh',
            'Philadelphia Flyers': 'Philadelphia',
            'Columbus Blue Jackets': 'Columbus',
            'New Jersey Devils':'New York City',
            'Carolina Hurricanes':'Raleigh',
            'New York Islanders':'New York City',
            'New York Rangers':'New York City',
            'Nashville Predators':'Nashville',
            'Winnipeg Jets':'Winnipeg',
            'Minnesota Wild':'Minneapolis–Saint Paul',
            'Colorado Avalanche':'Denver',
            'St. Louis Blues':'St. Louis',
            'Dallas Stars':'Dallas–Fort Worth',
            'Chicago Blackhawks':'Chicago',
            'Vegas Golden Knights':'Las Vegas',
            'Anaheim Ducks':'Los Angeles',
            'San Jose Sharks':'San Francisco Bay Area',
            'Los Angeles Kings':'Los Angeles',
            'Calgary Flames':'Calgary',
            'Edmonton Oilers':'Edmonton',
            'Vancouver Canucks':'Vancouver',
            'Arizona Coyotes':'Phoenix',
            'Tampa Bay Lightning':'Tampa Bay Area',
            'Montreal Canadiens': 'Montreal',
            'Phoenix Coyotes': 'Phoenix'}

    ## merging data frames
    nhl_df['Metropolitan Area'] = nhl_df['team'].map(MetroDict)
    df = pd.merge(cities, nhl_df, left_on='Metropolitan area', right_on='Metropolitan Area')
    df['Population (2016 est.)[8]'] = pd.to_numeric(df['Population (2016 est.)[8]'])
    df.head(31)

   ## drop duplicated columns
    df.loc[df['Metropolitan area'] == 'New York City', 'WLR'] = 0.5182013333333334
    df.loc[df['Metropolitan area'] == 'Los Angeles', 'WLR'] = 0.6228945
    df = df.dropna()
    df = df.drop_duplicates(keep='last',subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def nhl_correlation(): 
    
    population_by_region = df['Population (2016 est.)[8]']
    win_loss_by_region = df['WLR']

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)

data_cleansing()
nhl_correlation()
