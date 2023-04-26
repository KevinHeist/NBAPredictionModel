import numpy as np
import pandas as pd
import sklearn.ensemble as sk
import sklearn.datasets as ds
import sklearn.metrics as mt
import random
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


df1Games = pd.read_csv('ScoresCopy.csv', index_col=False)
df2Stats = pd.read_csv('TeamStatsDFFinalRevising.csv', index_col=False)

outputData = df1Games[['Home_Points','Away_Points']].to_numpy()
inputsData = df2Stats.to_numpy()

y = np.zeros((len(outputData),1))

xtrain, xtest, ytrain, ytest = train_test_split(inputsData, outputData, test_size=0.10, random_state=None)

# xtrain = inputsData[200:]
# xtest = inputsData[:200]
# ytrain = outputData[200:]
# ytest = outputData[:200]
# xtrain = inputsData[:6000]
# xtest = inputsData[6000:]
# ytrain = outputData[:6000]
# ytest = outputData[6000:]



rf = sk.RandomForestRegressor(n_estimators=100, max_depth=8,)
# by rf model ypred
rf.fit(xtrain,ytrain)
ypred = rf.predict(xtest)
mse = mt.mean_squared_error(ytest,ypred)

# for i in range(len(ypred)):
#     print(ytest[i], '=>', ypred[i])

modelydiff = np.zeros((len(ypred),1))
trueydiff = np.zeros((len(ypred),1))

for i in range(len(ypred)):
    trueydiff[i] = (outputData[i][0] - outputData[i][1])
    modelydiff[i] = (ypred[i][0] - ypred[i][1])
    #print(trueydiff[i], '=>', modelydiff[i])

LR1 = LinearRegression(fit_intercept=True, positive = True)
LR1.fit(xtrain, ytrain)
ypred1 =  LR1.predict(xtest)


modelydiff = np.zeros((len(ypred),1))
trueydiff = np.zeros((len(ypred),1))

for i in range(len(ypred)):
    trueydiff[i] = (outputData[i][0] - outputData[i][1])
    modelydiff[i] = (ypred1[i][0] - ypred1[i][1])
    #print(trueydiff[i], '=>', modelydiff[i])

print('LR MSE:',mt.mean_squared_error(ytest, ypred1))
print('RF MSE:', mt.mean_squared_error(ytest,ypred))

# ytrue ypred(RF) ypred1(LR)
newdf = np.zeros((len(ytest),6))

for j in range(len(ytest)):
    newdf[j][0] = ytest[j][0]
    newdf[j][1] = ytest[j][1]
    newdf[j][2] = ypred[j][0]
    newdf[j][3] = ypred[j][1]
    newdf[j][4] = ypred1[j][0]
    newdf[j][5] = ypred1[j][1]

savedDF = pd.DataFrame(newdf)
savedDF.to_csv("PerformanceML.csv")
