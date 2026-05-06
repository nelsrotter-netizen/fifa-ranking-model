**Alternative FIFA Ranking and Prediction Model
**

This repository presents an alternative model to determine FIFA rankings, then uses its capabilities to determine the history of team’s ELOs over time. The final capability is the prediction of matches between two teams at any given time. The dataset used is a complete history of every recorded FIFA sanctioned game since 1872. 
****It should be noted that I do not condone gambling and find sports betting to be a dangerous phenomenon in our current society. The point of this model is to see how easily one could find a way to game the system, especially considering that the current FIFA rankings are a significant determining factor in setting prediction markets. 

**Research Question: 
**Is there a better manner for ranking international teams apart from the traditional FIFA ranking system and is it more effective at predicting games than other AI modeling systems?

**Data Sources:
**This project sources data from a few different datasets:
  1. dataset compiling every FIFA sanctioned match since 1872. This dataset was pulled from Kaggle but could also be pulled by web-scraping from the FIFA website, where there is a catalogue of every game ever played. The primary concern with the dataset is that some of the teams recorded currently do not exist, with some well-known examples being East Germany and Yugoslavia. I considered removing those who were not currently recognized, but my own curiosity at seeing historical rankings of defunct countries was too great to take that step. Some interesting examples were teams like Catalonia and Yugoslavia that had some high-performing eras. 
  2. second dataset contains games from 2022 WC specifically. I had to go ahead and make a function to determine the winner of each game, which was compared to the predicted results from the updated ELO model.  
  3. third dataset has future games from the 2026 World Cup group stage. This was essential in order for the Odds API to be called to find market odds for each upcoming group stage game. 
  4. API from the Odds API, can be used for free to pull betting odds from any competitive sports game; odds pulled are from UK markets only

To use the Odds API:
1. Sign up for a free key at https://the-odds-api.com
2. Create a file called api_key.txt in the same folder as the scripts
3. Paste your API key into that file and save

**Scripts Used: 
**The repository consists of three separate scripts. 

Script 1: 
The first script initially reads the complete FIFA match dataset, altering the dates to be yearly and renaming some of the key column names to facilitate later analysis. It ensures that scores from matches are integers and then creates a new column called goal difference, a key feature of the newly developed ELO model. 

The first key function creates a new column to identify the winner for each game and applies it to the larger data_file, which then allows one to view which teams historically have the most wins. A further function defines the weight of games, weighing the World Cup highest, followed by elite regional tournaments, qualification matches, lesser regional tournaments, and finally all other friendly games. Another function determines the weight of goal difference to be used, capping the goal difference at 3, meaning a team with a +3 goal difference will have their match weighted double. 

The ELO function itself is derived from one similar to chess, with a base value of 1000 and a K_Base of 1, meaning every match is initially given a value of 1. This value is then multiplied by the various weighted factors earlier calculated, including match weight, goal difference, a time decay factor, and a win probability factor determined based on each team’s ELO before the match. After considering all of these factors, the code can be run and give the user a ranking list of every team to compete in a FIFA sanctioned match. 

The script then proceeds to develop a function to find a set of rankings at any given point in time, in this case in 2022. This developed ranking set will be used in the third script to see if the prediction model was well adapted in 2022 to predicting World Cup games. The same logic generally applies from the first update_elo function, except that it is flexible on the year input. 

Script 2:
The second script begins with a function predict_match, essentially just meaning that the team with the greater ELO at the match’s inception will win the match, with a probability given as to the validity of this result. A default dictionary function allows the user to view the collective history of every team at any given year or game. The plot_elo_history function then plots the history of any given team’s ELO over time, with the example of Senegal given in the script. 

Script 3: 
The final script demonstrates the predictive capacity of the ELO ranking model. The script imports a dataset with every group stage game from both the 2022 and upcoming 2026 World Cups, then making predictions on the outcomes from each game. For the 2022 WC, the predictions are compared to the actual results, whereas the 2026 WC is compared to AI predicted betting odds for each group stage game. These odds are pulled from the Odds API, a free-to-use API that collects betting market odds from various countries. The call that I used comes from the United Kingdom but it can be updated to find markets in whatever country the user chooses. The final portion of the script calculates how accurate the model would have been at predicting 2022 World Cup games. 

Notes: 
The first script is intended to bring about a more accurate version of the FIFA rankings system. The FIFA rankings are used not only as a measure of the strength of teams competing in international soccer, but have several practical functions as well. They determine what teams are chosen in World Cup and regional competition groups, the status of play-in games for the World Cup, and are consistently used as a key metric in prediction and betting markets. Despite their issues, they are consistently important and hold weight in international competition. 

The first script uses a model similar to that of chess ELO systems, building on a base ELO and calculating the weight of match to then be added or subtracted from the team’s ELO at any given point in time. The original FIFA model uses a similar system, with the key differences being a lack of goal difference weight, adjusted time weight, and match type functions. The first portion is important because it determines whether the match was tight and there was little to separate the teams or whether it was a decisive victory and one team was clearly the better side. 

The match type function that FIFA currently uses assigns more weight to European and South American competition, which often solidifies high achieving sides in those confederations in the higher echelons of the ranking system. The updated model weighs European, South American, Asian, and African competition equally to determine which teams are most in form regardless of confederation. This is exemplified by teams like Iran, Japan, and Senegal appearing in the top 15 ranked teams in the world, a point which was emphasized recently when Japan beat England in London in a pre-2026 World Cup friendly game with both teams at full strength. 

Some of the concerns that could arise from the model are the values given in the time weight and k_base values. The time weight for this case is quite brutal, meaning that recent matches take strong precedence over long-term success. This is a debatable issue; some argue that federations that have historical success tend to stay consistent over time due to solid management. When teams are successful, it encourages growth in youth soccer programs and investment in sporting infrastructure that in turn create long-term success on the field. This is certainly something to consider, but I argue that team selection changes so quickly and with changing national team eligibility rules it is quite difficult to predict how teams will compete over time. Therefore, I tend to view a model that heavily considers team form to be more accurate. The k_base value matters when comparing my ranking system to that of the current FIFA rankings only because their scale is more pronounced, with top teams appearing in the 1400 to 1600 ELO range. 

One of the concerns that I had when developing the predict match function was how to account for draws, something that betting markets still are pretty poor at doing. The first thought was to create a threshold for how far away teams were in ELO standing to where we could assume one would have a winning advantage. However, this model would likely produce more draws than wins in higher level competition when teams are likely at the same ELO level and I found that a win based model more effectively pits teams against one another to find which was to have the  advantage if one had to make a prediction. This would be especially important when considering knockout games, where stakes are higher and teams cannot simply play for a draw. 

The API that is used in the third script, called using the add_market_odds function, is a compilation of various UK betting odds aggregated amongst themselves to determine generally which team is favored. This API could be called for another country like the United States or France, but I used the example of the UK because betting markets are particularly strong in the soccer-crazed nation. 

**Overall Findings**
The ELO model generally produces rankings that are less favorable to teams in Europe and South America than we can currently view in the current FIFA World Rankings. This is intentional and achieved by weighting Asian and African competitions equal to those in Europe and South America, while also weighing qualification matches equally between confederations. 

The predict match function correctly predicted 36 out of 49 games in the 2022 World Cup, meaning 73.5% all games that did not end in a draw, a figure that indicates it could likely be successful on a financial level. In the 2026 World Cup scheme, the general distinction that it makes is to choose certain underdog teams to compete heavily with traditional European and South American giants and teams like the United States that are consistently high-ranked in the current system but rarely ever win a knockout World Cup game. If I had to pick a team or two to watch in the upcoming World Cup, it would be Japan first, Senegal second. Both are consistently dominant in their confederational play and boast a variety of talented players. Several of their matches are mismatches as described in the predictions dataframe; this could be something to note. 
