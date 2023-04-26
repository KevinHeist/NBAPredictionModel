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

def accuracyCheck(predScores):
    statsDictList = []
    countA = 0
    countH = 0
    RFCountH = 0
    LRCountH = 0
    NNCountH = 0
    RFCountA = 0
    LRCountA = 0
    NNCountA = 0
    for element in predScores:
        if int(element['TrueHome']) > int(element['TrueAway']):           #Home Team Acutally wins
            if float(element['RFHome']) > float(element['RFAway']):       #randomForest predicts Home team wins
                RFCountH +=  1
            if float(element['LRHome']) > float(element['LRAway']):       #LinearRegression predicts Home team wins
                LRCountH +=  1
            if float(element['NNHome']) > float(element['NNAway']):       #Neural Network predicts Home team wins
                NNCountH +=  1
            countH += 1
        elif int(element['TrueAway']) > int(element['TrueHome']):         #Away team actually wins
            if float(element['RFAway']) > float(element['RFHome']):       #randomForest predicts away team wins
                RFCountA +=  1
            if float(element['LRAway']) > float(element['LRHome']):       #LinearRegression predicts Home team wins
                LRCountA +=  1 
            if float(element['NNAway']) > float(element['NNHome']):       #Neural Network predicts Home team wins
                NNCountA +=  1 
                #print(element)
            countA += 1
    RFHacc = "{:.2f}".format((RFCountH/countH)*100)
    RFAacc = "{:.2f}".format((RFCountA/countA)*100)
    RFacc = "{:.2f}".format(((RFCountA + RFCountH)/(countA + countH))*100)
    LRHacc = "{:.2f}".format((LRCountH/countH)*100)
    LRAacc = "{:.2f}".format((LRCountA/countA)*100)
    LRacc = "{:.2f}".format(((LRCountA + LRCountH)/(countA + countH))*100)
    NNHacc = "{:.2f}".format((NNCountH/countH)*100)
    NNAacc = "{:.2f}".format((NNCountA/countA)*100)
    NNacc = "{:.2f}".format(((NNCountA + NNCountH)/(countA + countH))*100)

    print("Games Assessed: " + str((countA + countH)))
    print()
    print("randomForest home correct games: " + str(RFCountH) + "\t\taway correct games: " + str(RFCountA))
    print("randomForest home accuracy: " + str(RFHacc) + "%\t\taway accuracy: " + str(RFAacc) + "%")
    print("randomForest correct games: " + str(RFCountA + RFCountH) + "\t\t\tAccuracy: " + str(RFacc) + "%")
    print()
    print("LinearRegression home correct games: " + str(LRCountH) + "\taway correct games: " + str(LRCountA))
    print("LinearRegression home accuracy: " + str(LRHacc) + "%\t\taway accuracy: " + str(LRAacc) + "%")
    print("LinearRegression correct games: " + str(LRCountA + LRCountH) + "\t\tAccuracy: " + str(LRacc) + "%")
    print()
    print("Neural Network home correct games: " + str(NNCountH) + "\t\taway correct games: " + str(NNCountA))
    print("Neural Network home accuracy: " + str(NNHacc) + "%\t\taway accuracy: " + str(NNAacc) + "%")
    print("Neural Network correct games: " + str(NNCountA + NNCountH) + "\t\tAccuracy: " + str(NNacc) + "%")
    
        
    return
    #return statsDictList

predScores = genCSVDictList("True-RF-LR-NN_Performance_Scores.csv")
accuracyCheck(predScores)
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
