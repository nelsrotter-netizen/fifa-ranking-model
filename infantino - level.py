# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:09:17 2026

@author: nelso
"""

from collections import defaultdict
import pandas as pd
import numpy as np

#reading the file and renaming columns
data_file = pd.read_csv('results.csv')
data_file = data_file.rename(columns={"date": "year"})
data_file = data_file.rename(columns={'tournament': 'match_type'})
data_file['year'] = pd.to_datetime(data_file['year']).dt.year

#dropping values that are NA
data_file = data_file.dropna(subset=['home_team', 'away_team', 'home_score', 'away_score'])

#ensuring that scores are integers
data_file['home_score'] = data_file['home_score'].astype(int)
data_file['away_score'] = data_file['away_score'].astype(int)

#adding a new column called goal difference
data_file['goal_difference'] = data_file['home_score'] - data_file['away_score']

#writing a function to get results of games
def track_winner(row):
    if row['home_score'] > row['away_score']:
        return row['home_team']
    elif row['home_score'] < row['away_score']:
        return row['away_team']
    else:
        return 'Draw'
    
data_file['winner'] = data_file.apply(track_winner, axis=1)


print('Most Wins All Time')
print(data_file['winner'].value_counts())

print('Most Prevalent Competitions')
print(data_file['match_type'].value_counts())

print('All Competitions')
print(data_file['match_type'].unique())

current_year = 2026

def time_weight(year):
    return np.exp(-(current_year - year) / 10)  # adjust 10 for speed

#defining the weight of the match, more important
#matches matter more with the creation of this feature
def match_weight(row):
    match_type = str(row['match_type']).lower()
    if match_type == 'fifa world cup':
        return 6
    elif match_type in ['afc asian cup', 'uefa euro', 'african cup of nations', 'copa américa']:
        return 4
    elif 'qualification' in match_type:
        return 3
    elif match_type == 'gold cup' or 'nations league' in match_type:
        return 2
    else:
        return 1

#larger margins give more points, capped at 3 goals
#in the style of a forfeit, which is written as 3-0
def goal_diff_weight(row):
    gd = abs(row['goal_difference'])
    return 1 + min(gd, 3) / 3

#applying the functions to create columns
data_file['goal_diff_weight'] = data_file.apply(goal_diff_weight, axis=1)
data_file['match_weight'] = data_file.apply(match_weight, axis=1)
data_file['time_weight'] = data_file['year'].apply(time_weight)

# Sort chronologically so Elo updates are in order
data_file = data_file.sort_values('year').reset_index(drop=True)

# selecting a base rating with a chess-like ELO system
K_BASE = 1
INITIAL_ELO = 1000

#empty distionary for elo_ratings
elo_ratings = {}
match_counts = defaultdict(int)

data_file = data_file.sort_values('year').reset_index(drop=True)

def get_elo(team):
    if not team in elo_ratings:
        elo_ratings[team] = INITIAL_ELO
    return elo_ratings[team]    

#expected score of for team A against team B
def win_probability(rating_A, rating_B):
    return 1 / (1 + 10 ** ((rating_B - rating_A) / 100))

#teams start with a smaller K until they play 20 games
def get_k(team, base_k):
    games = match_counts.get(team, 0)
    if games < 20:
        scale = 0.5 + (games / 20) * 0.5   
        return base_k * scale
    return base_k

history = defaultdict(list)

def update_elo(row): 
    home = row['home_team']
    away = row['away_team']
 
    home_elo = get_elo(home)
    away_elo = get_elo(away)
    
    exp_home = win_probability(home_elo, away_elo)
    exp_away = 1 - exp_home
    
    #defining actual scores, 1 for a win, 0.5 for a tie, 0 for a loss
    if row['winner'] == home:
        actual_home, actual_away = 1, 0
    elif row['winner'] == away: 
        actual_home, actual_away = 0, 1
    else:
        actual_home, actual_away = 0.5, 0.5
        
    base_k = K_BASE * row['match_weight'] * row['goal_diff_weight'] * row['time_weight']
    
    k_home = get_k(home, base_k)
    k_away = get_k(away, base_k)
      
    elo_ratings[home] = home_elo + k_home * (actual_home - exp_home)
    elo_ratings[away] = away_elo + k_away * (actual_away - exp_away) 
    
    match_counts[home] = match_counts.get(home, 0) + 1
    match_counts[away] = match_counts.get(away, 0) + 1
    game = row.name  # row index = game number
    year = row['year']
    history[home].append((year, game, elo_ratings[home]))
    history[away].append((year, game, elo_ratings[away]))
#running the elo updates
data_file.apply(update_elo, axis=1)

rankings  = pd.DataFrame(list(elo_ratings.items()), columns=['team', 'elo']).sort_values('elo', ascending=False).reset_index(drop=True)
rankings.index += 1

print('ALL RANKINGS')
print(rankings.to_string)
print('TOP 50 RANKINGS')
print(rankings.head(50).to_string())

#function to be called to find rankings at any given time
def build_elo_ratings(matches_df, before_date):
    local_elo = {}
    local_counts = defaultdict(int)

    def get_local_elo(team):
        if team not in local_elo:
            local_elo[team] = INITIAL_ELO
        return local_elo[team]

    def get_local_k(team, base_k):
        games = local_counts.get(team, 0)
        if games < 20:
            scale = 0.5 + (games / 20) * 0.5
            return base_k * scale
        return base_k

    for _, row in matches_df.iterrows():  # was 'filtered', should be 'matches_df'
        home, away = row['home_team'], row['away_team']
        home_elo = get_local_elo(home)
        away_elo = get_local_elo(away)
        exp_home = win_probability(home_elo, away_elo)
        exp_away = 1 - exp_home
        if row['winner'] == home:
            actual_home, actual_away = 1, 0
        elif row['winner'] == away:
            actual_home, actual_away = 0, 1
        else:
            actual_home, actual_away = 0.5, 0.5
        base_k = K_BASE * row['match_weight'] * row['goal_diff_weight'] * row['time_weight']
        k_home = get_local_k(home, base_k)
        k_away = get_local_k(away, base_k)
        local_elo[home] = home_elo + k_home * (actual_home - exp_home)
        local_elo[away] = away_elo + k_away * (actual_away - exp_away)
        local_counts[home] += 1
        local_counts[away] += 1

    rankings = (
        pd.DataFrame(list(local_elo.items()), columns=['team', 'elo'])
        .sort_values('elo', ascending=False)
        .reset_index(drop=True)
    )
    rankings.index += 1
    return rankings

new_match_history = pd.read_csv('results.csv')
new_match_history['date'] = pd.to_datetime(new_match_history['date'])
new_match_history = new_match_history.rename(columns={'tournament': 'match_type'})  # must be before apply
new_match_history = new_match_history.dropna(subset=['home_team', 'away_team', 'home_score', 'away_score'])
new_match_history['home_score'] = new_match_history['home_score'].astype(int)
new_match_history['away_score'] = new_match_history['away_score'].astype(int)
new_match_history['goal_difference'] = new_match_history['home_score'] - new_match_history['away_score']
new_match_history['winner'] = new_match_history.apply(track_winner, axis=1)
new_match_history['goal_diff_weight'] = new_match_history.apply(goal_diff_weight, axis=1)
new_match_history['match_weight'] = new_match_history.apply(match_weight, axis=1)  # needs match_type to exist
new_match_history['time_weight'] = new_match_history['date'].dt.year.apply(time_weight)

match_history_2022 = new_match_history[new_match_history['date'] < '2022-11-20'].sort_values('date')
ratings_at_2022 = build_elo_ratings(match_history_2022, before_date='2022-11-20')
print(ratings_at_2022.head(20))