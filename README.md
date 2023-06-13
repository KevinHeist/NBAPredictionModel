# NBAPredictionModel
First, generated the various dates within the specified range. 
Which then allowed for me to find the teams that played on those days. This was compiled into a schedule csv dataframe.
After we then searched the scores given the teams that played on each day.
Then, various stats were scraped for the teams playing prior to that game.
Once that data was harvested then we would preprocess the data into a form that would allow for it to be inputted into our models.
Three models were leveraged: Deep Neural Network, Linear Regression, and Random Forest for Linear Regression.
These models were then trained and tested and the results were analyzed amongst another.

Used libraries/packages: BeautifulSoup, NumPy, Pandas, PyTorch, Scikit-Learn.
