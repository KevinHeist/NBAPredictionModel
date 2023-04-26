import os
import csv
from csv import DictReader

#Code used from:
#https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/
def genCSVDictList(csvName):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    csvList = csvName
    csvList = os.path.join(dirPath, csvList)
    with open(csvList, 'r') as f:
        
        dict_reader = DictReader(f)
        dictList = list(dict_reader)
    
    f.close()
    return dictList

def buildNewDict(teamDict):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    games = "games.csv"
    games = os.path.join(dirPath, games)
    with open(games, 'r') as f:
        
        dict_reader = DictReader(f)
        gameDict = list(dict_reader)
    
    f.close()
    newGameDictList = []
    for element in gameDict:
        newGameDict = {}    
        for key in element:
            if key == "GAME_DATE_EST":
                newGameDict["Date"] = element[key]
            if key == "VISITOR_TEAM_ID":
                teamName = teamFinder(element[key], teamDict)
                newGameDict["Vistor_Team_Name"] = teamName
            if key == "HOME_TEAM_ID":
                teamName = teamFinder(element[key], teamDict)
                newGameDict["Home_Team_Name"] = teamName
            if key == "PTS_home":
                newGameDict["Home_Points"] = element[key]
            if key == "PTS_away":    
                newGameDict["Away_Points"] = element[key]
        newGameDictList.append(newGameDict)
    
    return newGameDictList
    
# Finds team in csv file and converts its teamID to its nickname found in dict
def teamFinder(teamID, teamDict):
    for element in teamDict:
        for key in element:
            if key == "TEAM_ID":
                if element[key] == teamID:
                    #print("team id " + teamID + " element id " + element[key])
                    team = element
                    for teamKey in team:
                        if teamKey == "NICKNAME":
                            teamName = element[teamKey]    
                            #print(teamName)
                            return teamName
    
def writeDictToCSV(fieldnames, csvName, dictList):    
    dirPath = os.path.dirname(os.path.realpath(__file__))
    csvName = os.path.join(dirPath, csvName)
    with open(csvName, 'w', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for element in dictList:
            writer.writerow(element)

fieldnames = ['Date', 'Home_Team_Name', 'Vistor_Team_Name', 'Home_Points', 'Away_Points']
teamDict = genTeamDict()
newDictList = buildNewDict(teamDict)
writeDictToCSV(fieldnames, "newGames.csv", newDictList)
