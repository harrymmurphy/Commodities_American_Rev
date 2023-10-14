import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import statsmodels.api as sm 
import sklearn

commodities= 'https://raw.githubusercontent.com/harrymmurphy/Commodities_American_Rev/main/1770-1790%2C%20price%20indices%20-%20Sheet1.csv'
data = pd.read_csv(commodities)

# reorganize into timeseries data

data.rename(columns = {'m':'MONTH', 'y':'YEAR'}, inplace = True)
data['DATE'] = pd.to_datetime(data[['YEAR', 'MONTH']].assign(DAY=1))
timeseries = data.drop(['MONTH', 'YEAR'], axis = 1)


# Basic Plot to Visualize Prices
sns.lineplot(data=timeseries.replace('nan', float('nan')).melt(id_vars=['DATE']),
             x='DATE', y= "value", hue='variable')

