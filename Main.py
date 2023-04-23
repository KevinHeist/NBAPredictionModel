from bs4 import BeautifulSoup as bs
import requests as rq
from ScrapingFunctions import *
import csv
from ScrapingStats import *
import pandas as pd
import time
from reader import feed

offEffURL = 'https://www.teamrankings.com/nba/stat/offensive-efficiency?date='
defEffURL = 'https://www.teamrankings.com/nba/stat/defensive-efficiency?date='
assToTOURL = 'https://www.teamrankings.com/nba/stat/assist--per--turnover-ratio?date='
effFGPercURL = 'https://www.teamrankings.com/nba/stat/effective-field-goal-pct?date='
opEffFGPercURL = 'https://www.teamrankings.com/nba/stat/opponent-effective-field-goal-pct?date='

baseScoreUrl = 'https://www.basketball-reference.com/boxscores/?'

URLBank = [offEffURL, defEffURL, assToTOURL, effFGPercURL, opEffFGPercURL]

# Will go November 1st till April 1st
# 15-16 seasons onward include the power ranking ie: #3 Philadelphia
# Therefore must add something that will do another splicing method for the earlier years
# If there was not an nba game there is no output added to the dictionary -> no error
# Also if there is an invalid game ie 2/31/23 it will output nothing to the dictionary -> no error

url = 'https://www.teamrankings.com/nba/schedules/?date=' 

# Beginning of data collection ie 2023 would be begin at 2022-11-01 -> 2023 2023-03-31
# Generates dates for ease of url creation and getting the dates. GenerateDates(YearStart) ** default year is 2023
print('Dates being generated...')
DateMatrix = GenerateDates(2016)
#print(DateMatrix)
print('Date generation complete')

DFDates = pd.DataFrame(DateMatrix)
# # save the dataframe as a csv file
#DFDates.to_csv("DatesDF.csv")

GameHistory = {'Home': [], 'Away': [], 'Year-Month-Day': []}

# Function creating 
print('Using date matrix to find each game on each generated day')
ScrapingSched(url, GameHistory, DateMatrix)
print('***-----------------------***')
print('Complete Home/Away/Date dict')
print('***-----------------------***')

DFGames = pd.DataFrame(GameHistory)
# save the dataframe as a csv file
#DFGames.to_csv("GameListDF.csv")

#print(GameHistory) 

# How to print each particular element 
# print(GameHistory['Home'][2], GameHistory['Away'][2], GameHistory['Year-Month-Day'][2])

# Makes zero array of the correct length given the amount of teams 
TeamStats = np.zeros((len(GameHistory['Home'][:]),20))

dfGamesList = pd.read_csv('GameListDF.csv')
i = range(len(dfGamesList['Home']))

# Gathers the stats specified in the array for the selected teams
print('~~~~~ Scraping Stats for Specified Teams ~~~~~')
#8241 total
for j in i:
    print(j)
    if j%40 == 0 and j!=0:
        #sleep statement allows for greater times between requests
        print('sleeping')
        time.sleep(180)
    for URL in URLBank:
        StatScrape(dfGamesList['Home'][j], dfGamesList['Away'][j], j, TeamStats, URL, dfGamesList['Year-Month-Day'][j])
print('Finished')
print('===== Finished with Stat Collections =====')

DFStats = pd.DataFrame(TeamStats)
#DFStats.to_csv("TeamStatsDF.csv")

# Home Team ( OffEff(L3/Home), DefEff(L3/Home), AsToTO(L3/Home), EffFg%(L3/Home), OpEff(L3/Home), then same thing for Away Team )
#print(TeamStats)


# Gives the final scores from the dates in the dict format of Home/Away
print("------ Finding Scores for Specified Teams --------")

print('+++++ Final Scores Have Been Generated +++++')

 
# convert array into dataframe
#DFScores = pd.DataFrame(finalScores)
# save the dataframe as a csv file
#DFScores.to_csv("FinalScoresDF.csv")