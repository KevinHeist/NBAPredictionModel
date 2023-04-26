import numpy as np
import pandas as pd
import bs4 as bs
from ScrapingFunctions import *
import time
from TeamConverter import *


# Test used to ensure that the df's are all the same sizes and each of the team stats are correctly in the
# same row across all files
df1 = pd.read_csv('ScoresCopy.csv', index_col=False)
df2 = pd.read_csv('GameListFinal.csv', index_col=False)
df3 = pd.read_csv('TeamStatsDFFinalRevising.csv', index_col=False)

i = range(len(df1))

print(len(df1))
print(len(df2))
print(len(df3))
k = 0

# Checks that the hometeam for row x in df1 is the same as the home team in row x in df2
for j in i[:10]:
    if j % 100 == 0 and j != 0:
        k = k+1
        print('Another', 100*k,' done of', len(i))
    print('-----')
    print(df1['Home_Team_Name'][j])
    print(TeamConverter(df2['Home'][j]))

