Alternative FIFA Ranking and Prediction Model

This repository presents an alternative model to determine FIFA rankings, then uses its capabilities to determine the history of team’s ELOs over time. The final capability is the prediction of matches between two teams at any given time. The dataset used is a complete history of every recorded FIFA sanctioned game since 1872. 

Research Question: 
Is there a better manner for ranking international teams apart from the traditional FIFA ranking system and is it more effective at predicting games than other AI modeling systems?

Data Sources:
This project sources data from a few different datasets:
  1. dataset compiling every FIFA sanctioned match since 1872
  2. second dataset contains games from 2022 WC specifically
  3. third dataset has future games from the 2026 World Cup group stage
  4. API from the Odds API, can be used for free to pull betting odds from any competitive sports game; odds pulled are from UK markets only

Scripts Used: 
The repository consists of three separate scripts. 

Script 1: 
The first script initially reads the complete FIFA match dataset, altering the dates to be yearly and renaming some of the key column names to facilitate later analysis. It ensures that scores from matches are integers and then creates a new column called goal difference, a key feature of the newly developed ELO model. 

The first key function creates a new column to identify the winner for each game and applies it to the larger data_file, which then allows one to view which teams historically have the most wins. A further function defines the weight of games, weighing the World Cup highest, followed by elite regional tournaments, qualification matches, lesser regional tournaments, and finally all other friendly games. Another function determines the weight of goal difference to be used, capping the goal difference at 3, meaning a team with a +3 goal difference will have their match weighted double. 

The ELO function itself is derived from one similar to chess, with a base value of 1000 and a K_Base of 1, meaning every match is initially given a value of 1. This value is then multiplied by the various weighted factors earlier calculated, including match weight, goal difference, a time decay factor, and a win probability factor determined based on each team’s ELO before the match. After considering all of these factors, the code can be run and give the user a ranking list of every team to compete in a FIFA sanctioned match. 

Script 2:
The second script begins with a function predict_match, essentially just meaning that the team with the greater ELO at the match’s inception will win the match, with a probability given as to the validity of this result. A default dictionary function allows the user to view the collective history of every team at any given year or game. The plot_elo_history function then plots the history of any given team’s ELO over time, with the example of Senegal given in the script. 

Script 3: 
The final script demonstrates the predictive capacity of the ELO ranking model. The script imports a dataset with every group stage game from both the 2022 and upcoming 2026 World Cups, then making predictions on the outcomes from each game. For the 2022 WC, the predictions are compared to the actual results, whereas the 2026 WC is compared to AI predicted betting odds for each group stage game. 

Notes: 
The first script is intended to bring about a more accurate version of the FIFA rankings system. The FIFA rankings are used not only as a measure of the strength of teams competing in international soccer, but have several practical functions as well. They determine what teams are chosen in World Cup and regional competition groups, the status of play-in games for the World Cup, and are consistently used as a key metric in prediction and betting markets. Despite their issues, they are consistently important and hold weight in international competition. 

The first script uses a model similar to that of chess ELO systems, building on a base ELO and calculating the weight of match to then be added or subtracted from the team’s ELO at any given point in time. The original FIFA model uses a similar system, with the key differences being a lack of goal difference weight, adjusted time weight, and match type functions. The first portion is important because it determines whether the match was tight and there was little to separate the teams or whether it was a decisive victory and one team was clearly the better side. The match type function that FIFA currently uses assigns more weight to European and South American competition, which often solidifies high achieving sides in those confederations in the higher echelons of the ranking system. The updated model weighs European, South America, Asian, and African competition equally to determine which teams are most in form regardless of confederation. This is exemplified by teams like Iran, Japan, and Senegal appearing in the top 15 ranked teams in the world, a point which was emphasized recently when Japan beat England in London in a pre-2026 World Cup friendly game with both teams at full strength. 

The predict match function is one that can be adjusted by the user to account for the probability of draws, which can be achieved by setting a difference in ELO threshold that must be reached for one team to be deemed as having an advantage. In this model, however, the goal is to find games where betting markets are picking a favorite that is at odds with the updated model, a point at which current ranking systems are overvaluing the strengths of a given side. 

The API that is used in the third script, called using the add_market_odds function, is a compilation of various UK betting odds aggregated amongst themselves to determine generally which team is favored. This API, of course, could be called in another country like the United States or France, but I used the example of the UK because betting markets are particularly strong in the soccer-crazed nation. 
