#Test
import numpy as np
import pandas as pd
import bs4 as bs
from ScrapingFunctions import *
import time

#2015-11-01

# df = pd.read_csv("GameListDF.csv")

dfGames = pd.read_csv("games.csv")
dfTeamsInfo = pd.read_csv("teams.csv")

#print(dfGames.head(5))

#row 25097

dfNewGames = dfGames[:][:25097]
i = range(25097)

# dfNewGames.to_csv("GameListOnline.csv")

tempTeamID = '1610612737'
IDList = dfTeamsInfo.loc[:,'TEAM_ID']
print(IDList)

# c = (dfTeamsInfo['TEAM_ID'] == 1610612737)

# print(tempidx)
# print(dfTeamsInfo.iloc['1610612737',:])

# for homeTeam in dfNewGames[i]['TEAM_ID_home']:
#     print(i)
#     tempidx = dfTeamsInfo.loc[0,'TEAM_ID']
#     dfNewGames['TEAM_ID_home'][i] = dfTeamsInfo[tempidx+4]
#     print(dfNewGames['TEAM_ID_home'][i])
#     i = i+1

# finalScores = np.zeros((len(df['Home'][:]),2))

# GameHistory = {'Home': ['Pistons', 'Pacers', 'Bucks'], 'Away': ['Nets', 'Knicks', 'Bulls'], 'Year-Month-Day': ['20230405']}
# finalScores = np.zeros((len(GameHistory['Home'][:]),2))
# i = range(len(GameHistory['Home']))
# for j in i[0:3]:
#     FindScore(GameHistory['Home'][j], GameHistory['Away'][j], GameHistory['Year-Month-Day'][j], finalScores, j)


# for j in i[0:8241]:
#     print(j)
#     if j%25 == 0 and j!=0:
#         print('sleeping')
#         time.sleep(80)
#     FindScore(df['Home'][j], df['Away'][j], df['Year-Month-Day'][j], finalScores, j)
#     finalScores.to_csv("GameListDF.csv")
# print('Finished')