# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:56:00 2026

@author: nelso
"""
import pandas as pd
import requests
from collections import defaultdict

#getting an API from Odds API, to be used to take odds from upcoming WC
def fetch_odds(api_key):
    return requests.get(
        "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds",
        params={"apiKey": api_key, "regions": "uk", "markets": "h2h", "oddsFormat": "decimal"}
    ).json()

#making a function to add market odds
def add_market_odds(predictions, api_key):
    odds_data = fetch_odds(api_key)
    #empty dataframe to be filled with odds
    market_odds = {}
    for match in odds_data:
        #setting two teams into the loop
        key = (match['home_team'], match['away_team'])
        home_probs, away_probs, draw_probs = [], [], []
        for bookmaker in match['bookmakers']:
            outcomes = bookmaker['markets'][0]['outcomes']
            for o in outcomes:
                #converting odds to probabilities, because they start as a whole number
                if o['name'] == match['home_team']:
                    home_probs.append(1 / o['price'])
                elif o['name'] == match['away_team']:
                    away_probs.append(1 / o['price'])
                else:
                    draw_probs.append(1 / o['price'])
        market_odds[key] = {
            #averaging across bookmakers to find implied probabilities
            'market_home_prob': sum(home_probs) / len(home_probs),
            'market_away_prob': sum(away_probs) / len(away_probs),
            'market_draw_prob': sum(draw_probs) / len(draw_probs),
        }
    
    predictions['market_home_prob'] = predictions.apply(
        lambda row: market_odds.get((row['home_team'], row['away_team']), {}).get('market_home_prob'), axis=1)
    predictions['market_away_prob'] = predictions.apply(
        lambda row: market_odds.get((row['home_team'], row['away_team']), {}).get('market_away_prob'), axis=1)
    predictions['market_draw_prob'] = predictions.apply(
        lambda row: market_odds.get((row['home_team'], row['away_team']), {}).get('market_draw_prob'), axis=1)
    
    return predictions

#reading a file containing every match from 2026 WC
group_stage_matches = pd.read_csv('2026_group_fixtures.csv')  

name_fixes = {
    'Bosnia and Herzegovina': 'Bosnia & Herzegovina', 
    'Cape_Verde': 'Cape Verde',
    'Curacao': 'Curaçao',
    'Czechia': 'Czech Republic',
    'Turkiye': 'Turkey',
    'United States': 'USA'}

#making a new Data Frame to house predictions
predictions = pd.DataFrame()
predictions[['home_team', 'away_team']] = group_stage_matches[['home_team', 'away_team']]
predictions['home_team'] = predictions['home_team'].replace(name_fixes)
predictions['away_team'] = predictions['away_team'].replace(name_fixes)
predictions[['ELO winner', 'ELO probability']] = pd.DataFrame(group_stage_matches.apply(lambda row: predict_match(row['home_team'], row['away_team']), axis=1).tolist())

with open('api_key.txt', 'r') as f:
    API_KEY = f.read().strip()

predictions = add_market_odds(predictions, api_key=API_KEY)

#defining a function to show who an AI model predicts would win
def market_winner(row):
    # determine market predicted winner
    if row['market_home_prob'] > row['market_away_prob'] and row['market_home_prob'] > row['market_draw_prob']:
        return row['home_team']
    elif row['market_away_prob'] > row['market_home_prob'] and row['market_away_prob'] > row['market_draw_prob']:
        return row['away_team']
    
predictions['market_winner'] = predictions.apply(market_winner, axis=1)

def corrections(row):    
    if row['ELO winner'] != row['market_winner']:
        return 'Mismatch'
    else:
        return 'Match'
    
predictions['comparison'] = predictions.apply(corrections, axis=1)

odds_data = fetch_odds(API_KEY)

names = []

for match in odds_data:
    print(match['home_team'], 'vs', match['away_team'])
    names.extend([match['home_team'], match['away_team']])

names = set(names)
p_names = set(predictions['home_team']).union(predictions['away_team'])

print(group_stage_matches[['home_team', 'away_team']].to_string())

lastWC_Fixtures = pd.read_csv('2022_WC_Fixtures.csv')
lastWC_Fixtures[['team1', 'team2']] = lastWC_Fixtures[['team1', 'team2']].apply(lambda x: x.str.capitalize())

def former_WC_winner(row):
    if row['number of goals team1'] > row['number of goals team2']:
        return row['team1']
    elif row['number of goals team1'] < row['number of goals team2']:
        return row['team2']
    else:
        return 'Draw'
    
lastWC_Fixtures['actual_winner'] = lastWC_Fixtures.apply(former_WC_winner, axis=1)

def predict_match_at(home, away, ratings):
    home_elo = ratings.get(home, INITIAL_ELO)
    away_elo = ratings.get(away, INITIAL_ELO)
    
    home_win = win_probability(home_elo, away_elo)
    away_win = 1 - home_win
    
    if home_win > away_win:
        return (home, home_win)
    else:
        return (away, away_win)
    
#converting ratings_at_2022 to a dictionary to be looked up
ratings_2022_dict = dict(zip(ratings_at_2022['team'], ratings_at_2022['elo']))
lastWC_Fixtures[['predicted_winner', 'predicted_probability']] = pd.DataFrame(
    lastWC_Fixtures.apply(lambda row: predict_match_at(row['team1'], row['team2'], ratings_2022_dict), axis=1).tolist()                      )
lastWC_Fixtures['correct'] = lastWC_Fixtures['predicted_winner'] == lastWC_Fixtures['actual_winner']
print(lastWC_Fixtures[['team1', 'team2', 'predicted_winner', 'actual_winner', 'correct']])
