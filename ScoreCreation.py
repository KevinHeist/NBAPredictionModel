#Test
import numpy as np
import pandas as pd
import bs4 as bs
from ScrapingFunctions import *
import time
from TeamConverter import *

#scores generated from kaggle excel data set 
dfScoresH = pd.read_csv('newGames.csv', index_col=False)
#who plays when
dfGames = pd.read_csv('GameListDF.csv', index_col=False)

# Empty dataframe to populate with the scores and teams
ScoresComp = {'Date': [], 'Home_Team_Name': [], 'Vistor_Team_Name': [], 'Home_Points': [], 'Away_Points': []}
ScoresDF = pd.DataFrame(ScoresComp)

# Using the score outcome excel sheet found online, goes through our generated schedule and makes
# a dataframe that gives the scores of the generated schedule games.
# This is done by searching by date in the data file then searching for the team's game
# TeamConverter function is necessary because each of the files refer to teams in different ways 
# ie Philadelphia opposed to 76ers
i = range(len(dfGames['Home']))
k = 0
for j in i:
    if j % 100 == 0 and j != 0:
        k = k+1
        print('Another', 100*k,' done of', len(i))
    df = dfScoresH[dfScoresH['Date'].str.contains(dfGames['Year-Month-Day'][j])]
    df = df.loc[dfScoresH['Home_Team_Name'] == TeamConverter(dfGames['Home'][j])]
    ScoresDF = ScoresDF.append(df, ignore_index = True)

# Returns excel sheet with the score of each game in the order of the gameHistory starting at 2015-11-01
ScoresDF.to_csv("Scores.csv")
print(ScoresDF)