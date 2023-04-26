import numpy as np
import pandas as pd
import torch 
from torch import nn, save, load
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import TensorDataset, DataLoader
import torch.nn.functional as F
import sklearn.metrics as mt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sklearn.metrics as mt
import sklearn.ensemble as sk

# ScoresCopy is converted to the correct date format
df1Games = pd.read_csv('ScoresCopy.csv', index_col=False)
# TeamStats...Revising was edited to remove any errors between games to keep it consistent to the scores
df2Stats = pd.read_csv('TeamStatsDFFinalRevising.csv', index_col=False)

outputData = df1Games[['Home_Points','Away_Points']].to_numpy()
inputsData = df2Stats.to_numpy()

#deleting index col
inputsData = np.delete(inputsData, 0, 1)

# Splitting up data into training and testing data sets, allowing for it to be randomized
xtrain, xtest, ytrain, ytest = train_test_split(inputsData, outputData, test_size=0.05, random_state=None)

# Necessary data type conversions for PyTorch
xtestNN = torch.from_numpy(xtest)
ytestNN = torch.from_numpy(ytest)
xtestNN = xtestNN.float()
ytestNN = ytestNN.float()
xtrainNN = torch.from_numpy(xtrain)
ytrainNN = torch.from_numpy(ytrain)
xtrainNN = xtestNN.float()
ytrainNN = ytestNN.float()

# Converting to tensor
train_ds = TensorDataset(xtrainNN, ytrainNN)

# Creating data set for input into NN framework
batch_size = 100
train_dl = DataLoader(train_ds, batch_size, shuffle=True)
next(iter(train_dl))

# Neural Network
class ScorePred(nn.Module): 
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            # Layer Construction
            nn.Linear(20, 50), 
            nn.ELU(),
            nn.Linear(50,100),
            nn.ReLU(),
            nn.Linear(100,40),
            nn.ELU(),
            nn.Linear(40, 20),
            nn.ELU(),
            nn.Linear(20, 10),
            nn.ReLU(),
            nn.Linear(10, 5), 
            nn.ELU(),
            nn.Linear(5, 2),
        )

    def forward(self, x): 
        return self.model(x)

# Instance of the neural network, loss, optimizer 
clf = ScorePred().to('cpu')
opt = Adam(clf.parameters(), lr=1e-3)
loss_fn = nn.MSELoss() 


# Training flow 
if __name__ == "__main__": 
    print('Done')
    for epoch in range(20): # train for 20 epochs
        for batch in train_dl: 
            X,y = batch 
            X, y = X.to('cpu'), y.to('cpu') 
            yhat = clf(X) 
            loss = loss_fn(yhat, y) 

            # Apply backprop 
            opt.zero_grad()
            loss.backward() 
            opt.step() 

        print(f"Epoch:{epoch} loss is {loss.item()}")
    
    # Saving model
    # with open('model_state.pt', 'wb') as f: 
    #     save(clf.state_dict(), f) 

#Opening saved model
with open('model_state.pt', 'rb') as f:
    clf.load_state_dict(load(f))

# Generating predictions based off outputs   
ypred2 = np.zeros((len(ytestNN),2))
ypred2 = torch.from_numpy(ypred2)
ypred2 = ypred2.float()
for i in range(len(xtestNN)):
    ypred2[i] = clf(xtestNN[i][:])

# Mean Squared Error is outputted for the NN
print('NN MSE:', mt.mean_squared_error((ytrainNN.detach()).numpy(),(ypred2.detach()).numpy()))

# Creating new df to store home/away scores predictions from NN
newdf = np.zeros((len(ypred2),4))
for j in range(len(ypred2)):
    newdf[j][0] = ypred2[j][0]
    newdf[j][1] = ypred2[j][1]


# Create the rf model structure
# n_estimators = number of trees generated
# max_depth = max number of nodes in each tree
rf = sk.RandomForestRegressor(n_estimators=100, max_depth=8,)
rf.fit(xtrain,ytrain)
ypred = rf.predict(xtest)

# Create the lr model structure using training data
# fit_intercept = allow a y-intercept in model
# positive = ensures all coefficients are positive
LR1 = LinearRegression(fit_intercept=True, positive = True)
LR1.fit(xtrain, ytrain)
ypred1=  LR1.predict(xtest)

# Mean squared error outputted of LR and RF
print('LR MSE:',mt.mean_squared_error(ytest, ypred1))
print('RF MSE:', mt.mean_squared_error(ytest,ypred))

# creates data type to have the outputs of each model
newdf = np.zeros((len(ytest),8))

# ytrue ypred(RF) ypred1(LR) ypred2(NN)
for j in range(len(ytest)):
    newdf[j][0] = ytest[j][0]
    newdf[j][1] = ytest[j][1]
    newdf[j][2] = ypred[j][0]
    newdf[j][3] = ypred[j][1]
    newdf[j][4] = ypred1[j][0]
    newdf[j][5] = ypred1[j][1]
    newdf[j][6] = ypred2[j][0]
    newdf[j][7] = ypred2[j][1]

# saving dataframe to csv file
savedDF = pd.DataFrame(newdf)
savedDF = savedDF.round(1)
#savedDF.to_csv("PerformanceMLnew8.csv")