from bs4 import BeautifulSoup as bs
import requests as rq
from ScrapingFunctions import *
import csv
from ScrapingStats import *
import pandas as pd
import time
from reader import feed

# Links to stats used
offEffURL = 'https://www.teamrankings.com/nba/stat/offensive-efficiency?date='
defEffURL = 'https://www.teamrankings.com/nba/stat/defensive-efficiency?date='
assToTOURL = 'https://www.teamrankings.com/nba/stat/assist--per--turnover-ratio?date='
effFGPercURL = 'https://www.teamrankings.com/nba/stat/effective-field-goal-pct?date='
opEffFGPercURL = 'https://www.teamrankings.com/nba/stat/opponent-effective-field-goal-pct?date='

# Link to to URL used for the score
baseScoreUrl = 'https://www.basketball-reference.com/boxscores/?'

# Bank of the URLs used for stats collection
URLBank = [offEffURL, defEffURL, assToTOURL, effFGPercURL, opEffFGPercURL]

# URL used to generate team schedule
url = 'https://www.teamrankings.com/nba/schedules/?date=' 

# Beginning of data collection ie 2023 would be begin at 2022-11-01 -> 2023 2023-03-31
# Generates dates for ease of url creation and getting the dates. GenerateDates(YearStart) ** default year is 2023
print('Dates being generated...')
DateMatrix = GenerateDates(2016)
#print(DateMatrix)
print('Date generation complete')

# Dataframe of the generated dates
DFDates = pd.DataFrame(DateMatrix)

# Used to see what teams play on what days
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

# Makes zero array of the correct length given the amount of teams
# Will be used for collecting the stats each day the team plays 
TeamStats = np.zeros((len(GameHistory['Home'][:]),20))

# Calls the game list dict 
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

# Saves team stats DF
DFStats = pd.DataFrame(TeamStats)
# Was done partially in jupiter so TeamStatsDF is not full, look for TeamStatsDFFinalRevising for full
#DFStats.to_csv("TeamStatsDF.csv")

# Stats Matrix Structure
# Home Team ( OffEff(L3/Home), DefEff(L3/Home), AsToTO(L3/Home), EffFg%(L3/Home), OpEff(L3/Home), then same thing for Away Team )