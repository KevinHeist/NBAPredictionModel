from bs4 import BeautifulSoup as bs
import requests as rq
import numpy as np

#date = '2023-11-01'
statBank = []
offEffURL = 'https://www.teamrankings.com/nba/stat/offensive-efficiency?date='
defEffURL = 'https://www.teamrankings.com/nba/stat/defensive-efficiency?date='
assToTOURL = 'https://www.teamrankings.com/nba/stat/assist--per--turnover-ratio?date='
effFGPercURL = 'https://www.teamrankings.com/nba/stat/effective-field-goal-pct?date='
opEffFGPercURL = 'https://www.teamrankings.com/nba/stat/opponent-effective-field-goal-pct?date='

URLBank = [offEffURL, defEffURL, assToTOURL, effFGPercURL, opEffFGPercURL]
#urlDate = 'https://www.teamrankings.com/nba/stat/offensive-efficiency?date=2022-11-01'

#stat = '', url = '', date = '',  - > put back into parameters when working

def StatScrape(home = '', away = '', i = 0, TeamStats = [], url = '', date = ''):
    urlDate = url + str(date)
    page = rq.get(urlDate).text
    soup = bs(page,features="html.parser")
    
    # Takes the url info and puts it into a Python object (ListOfGames) --- works because there is only one table and this is the first
    table = soup.find('table')

    #stats after the team name: year / last 3 / last 1 / home / away
    inner = [item.text for item in soup.find_all('td')]
    # Last 3 then home/away do home team stats first then away
    # if it is a string or percentage it must be int()
    tempidx = inner.index(home)
    print(inner)
    # if statements including '--' are to combat there being empty stats on certain days given it being 
    # early in the season

    # inner[tempidx+2] = Last 3 games stat
    # inner[tempidx+4] = stats at home for the home team
    # inner[tempidx+5] = stats while away for the away team
    if inner[tempidx+4] == '--':
            inner[tempidx+4] = inner[tempidx+1]
    if inner[tempidx+2] == '--':
            inner[tempidx+4] = inner[tempidx+2]
    if url == URLBank[0]:
        TeamStats[i][0] = inner[tempidx+2]
        TeamStats[i][1] = inner[tempidx+4]
        tempidx = inner.index(away)
        if inner[tempidx+5] == '--':
            inner[tempidx+5] = inner[tempidx+1]
        TeamStats[i][10] = inner[tempidx+2]
        TeamStats[i][11] = inner[tempidx+5]
    elif url == URLBank[1]:
        TeamStats[i][2] = inner[tempidx+2]
        TeamStats[i][3] = inner[tempidx+4]
        tempidx = inner.index(away)
        if inner[tempidx+5] == '--':
            inner[tempidx+5] = inner[tempidx+1]
        TeamStats[i][12] = inner[tempidx+2]
        TeamStats[i][13] = inner[tempidx+5]
    elif url == URLBank[2]:
        TeamStats[i][4] = inner[tempidx+2]
        TeamStats[i][5] = inner[tempidx+4]
        tempidx = inner.index(away)
        if inner[tempidx+5] == '--':
            inner[tempidx+5] = inner[tempidx+1]
        TeamStats[i][14] = inner[tempidx+2]
        TeamStats[i][15] = inner[tempidx+5]
    elif url == URLBank[3]:
        TeamStats[i][6] = float((inner[tempidx+2]).strip('%'))
        TeamStats[i][7] = float((inner[tempidx+4]).strip('%'))
        tempidx = inner.index(away)
        if inner[tempidx+5] == '--':
            inner[tempidx+5] = inner[tempidx+1]
        TeamStats[i][16] = float((inner[tempidx+2]).strip('%'))
        TeamStats[i][17] = float((inner[tempidx+5]).strip('%'))
    elif url == URLBank[4]:
        TeamStats[i][8] = float((inner[tempidx+2]).strip('%'))
        TeamStats[i][9] = float((inner[tempidx+4]).strip('%'))
        tempidx = inner.index(away)
        if inner[tempidx+5] == '--':
            inner[tempidx+5] = inner[tempidx+1]
        TeamStats[i][18] = float((inner[tempidx+2]).strip('%'))
        TeamStats[i][19] = float((inner[tempidx+5]).strip('%'))

    return TeamStats
