# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:10:49 2026

@author: nelso
"""

from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

#function to predict match between two teams given their elo at a certain point
def predict_match(home, away):
    home_elo = get_elo(home)
    away_elo = get_elo(away)
    
    home_win = win_probability(home_elo, away_elo)
    away_win = 1 - home_win
    
    if home_win > away_win:
        return (home, home_win)
    else:
        return (away, away_win)

#predicting a match from upcoming group stage
team, probability = predict_match('Senegal', 'France')
print(f'Predicted winner: {team} with a {probability * 100:.1f}% chance')

#updating the history of each team
#history will show each teams elo rating at each game and then by year
history = defaultdict(list)

data_file['game'] = data_file.index + 1
data_file.apply(update_elo, axis=1)

x = pd.DataFrame(history['England'], columns=['year', 'game', 'elo'])
x = x.sort_values(['year', 'game'])

y = x.groupby('year').tail(1)
z = history['Brazil']

print(history)

#function to make historic plots of team elos
def plot_elo_history(team):
    df = pd.DataFrame(history[team], columns=['year', 'game', 'elo'])
    df = df.sort_values(['year', 'game'])
    yearly = df.groupby('year').tail(1)
    fig, ax = plt.subplots()
    ax.plot(yearly['year'], yearly['elo'], color = 'blue')
    ax.set_title(f'{team} ELO RATING OVER TIME', fontsize=5)
    ax.set_xlabel('YEAR')
    ax.set_ylabel('ELO RATING')
    ax.legend()
    plt.tight_layout()

plot_elo_history('Senegal')
