from bs4 import BeautifulSoup as bs
import requests as rq

# This includes the functions used for pulling the games played at each date and putting them into a dict that has HOME/AWAY/DATE
# Potential issue when 14-15 season and the seasons prior do not include the power rankings so the string splicing needs to be different
# 2016 is the most number of data we can do if we do not fix the splicing issue
def GenerateDates(initial_year = 2023): 
    dateMatrix = []
    # 2024 sets it so the final date is 2023-03-31
    for year in range(2024 - (initial_year)):
        year = initial_year + year
        for month in range(5):
            # Nov 1st to March 31st if range = 5
            # Function for doing the proper month with switch statement ie 11 - 03
            month = MonthCheck(month)
            #31 days for range unless testing
            for day in range(31):
                day = DayCheck(day)
                dateMatrix.append(str(YearCheck(year, month)) + '-' + str(month) + '-' + str(day))
    DateArray = dateMatrix
    return DateArray

# Searches the site for each game played in the given date that is inputted into it
def ScrapingSched(url, gameList, dates): 
    for YMD in dates:
        urlDate = url + str(YMD)
        print(YMD)
        page = rq.get(urlDate).text
        soup = bs(page,features="html.parser")

        # Takes the url info and puts it into a Python object (ListOfGames) --- works because there is only one table and this is the first
        table = soup.find('table')
        ListOfGames = []
        
        for row in table.find_all('tr')[1:]:
            temp = row.text.replace('\n\n', ' ').strip()
            temp_list = temp.split('\n')
            ListOfGames.append((temp_list[2]))
        
        # Outputs all the games of the day in a list

        # For loop that goes through the table contents of the scraped data and sending it into a dictionary -> gameList
        for gameTitle in ListOfGames:
            firstGame = gameTitle
            #print(firstGame) for troubleshooting
            if ' at' in firstGame:
                abridgedIdx = firstGame.index(' at')
                homeTeam = firstGame[abridgedIdx+8:]
                awayTeam = firstGame[3:abridgedIdx-1]
                gameList['Home'].append(homeTeam.strip())
                gameList['Away'].append(awayTeam.strip())
                gameList['Year-Month-Day'].append(YMD)
            elif ' vs.' in firstGame:
                abridgedIdx = firstGame.index(' vs.')
                homeTeam = firstGame[abridgedIdx+9:]
                awayTeam = firstGame[3:abridgedIdx-1]
                gameList['Home'].append(homeTeam.strip())
                gameList['Away'].append(awayTeam.strip())
                gameList['Year-Month-Day'].append(YMD)

    return gameList

# Converts the day generation into the form that the URL accepts it in
def DayCheck(day):
    day = day + 1
    if day < 10:
        day = '0' + str(day)
        return day
    return str(day)

# Converts month generation into the form that the URL accepts it in
def MonthCheck(month):
    if month == 0:
        return '11'
    elif month == 1:
        return '12'
    elif month == 2:
        return '01'
    elif month == 3:
        return '02'
    elif month == 4:
        return '03'

# Ensures that the years for a given date are correct
def YearCheck(year, month):
    if (int(month) == 11 or int(month) == 12):
        year = int(year) - 1
        return str(year)
    else:
        return str(year)

# Converts the dates so they are in the correct format for a given cites url structure
def DateConverterToURL (date):
    # year-month-day  ---->  month=04&day=8&year=2023
    ScoreDate = 'month=' + str(int(date[5:7])) + '&day=' + str(int(date[8:10])) + '&year=' + str(date[0:4])
    return str(ScoreDate)
