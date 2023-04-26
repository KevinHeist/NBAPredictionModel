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

def buildNewGamesDictList(teamDict):
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

def buildStatsDictList(predScores):
    statsDictList = []
    count = 0
    RFCount = 0
    LRCount = 0
    NNCount = 0
    for element in predScores:
        if element['TrueHome'] > element['TrueAway']:       #Home Team Acutally wins
            if element['RFHome'] > element['RFAway']:       #randomForest predicts Home team wins
                RFCount +=  1
            if element['LRHome'] > element['LRAway']:       #LinearRegression predicts Home team wins
                LRCount +=  1
            if element['NNHome'] > element['NNAway']:       #Neural Network predicts Home team wins
                NNCount +=  1
        else:                                               #Away team actually wins
            if element['RFAway'] > element['RFHome']:       #randomForest predicts away team wins
                RFCount +=  1
            if element['LRAway'] > element['LRHome']:       #LinearRegression predicts Home team wins
                LRCount +=  1 
            if element['NNAway'] > element['NNHome']:       #Neural Network predicts Home team wins
                NNCount +=  1 
        count += 1
    
    print("Games Assessed: " + str(count))
    print("randomForest correct games: " + str(RFCount) + " Accuracy: " + str(((RFCount/count)*100)) + "%")
    print("LinearRegression correct games: " + str(LRCount) + " Accuracy: " + str(((LRCount/count)*100)) + "%")
    print("Neural Network correct games: " + str(NNCount) + " Accuracy: " + str(((NNCount/count)*100)) + "%")

        
    return
    #return statsDictList

predScores = genCSVDictList("True-RF-LR-NN_Performance_Scores.csv")
buildStatsDictList(predScores)
''' 
'' = index
0 = real home score
1 = real away score
2 = randomForest home score
3 = randomForest away score
4 = LinearRegression home score
5 = LinearRegression away score
'''


#print(predScores)
#fieldnames = ['Date', 'Home_Team_Name', 'Vistor_Team_Name', 'Home_Points', 'Away_Points']
#teamDict = genTeamDict()
#newDictList = buildNewDict(teamDict)
#writeDictToCSV(fieldnames, "newGames.csv", newDictList)
