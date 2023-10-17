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

### Hodrick-Prescott Filtering

# Lambda Parameter calculation 100*(period)^2
lambda_param = 100*(12)^2  


timeseries1 = timeseries.iloc[:,0:25]

# Hodrick-Prescott Filtering
def Hodrick_Prescott (self):
    for col in cols:
        trend, cyclical = sm.tsa.filters.hpfilter(timeseries[col], lamb=lambda_param)
        print(cyclical.head(500)) #observe values, make sure they make sense
        print(trend.head(500)) # same as above^
        return(trend)
        return(cyclical)
HP_df = pd.DataFrame()
cols = timeseries1.columns
HP_df[cols] = timeseries1[cols].apply(Hodrick_Prescott)
print(HP_df.head(100))

# Verifty that apply function 
trend,cyclical = sm.tsa.filters.hpfilter(timeseries['Beef'], lamb=lambda_param)
print(trend.head(100))

date = timeseries['DATE']
HP_timeseries = pd.concat([HP_df, date], axis=1).reindex(HP_df.index)

# Graph the Hodrick_Prescott cyclical component to understand volatility in the short-term.
sns.lineplot(data=HP_timeseries.replace('nan', float('nan')).melt(id_vars=['DATE']),
             x='DATE', y= "value", hue='variable')

## Plots for Individual Commodities
# Cocoa        
Cocoa_df = HP_df['Chocolate']
Cocoa_timeseries = pd.concat([Cocoa_df, date], axis=1).reindex(Cocoa_df.index)
Cocoa_timeseries.plot(x='DATE', y='Chocolate')
# Coffee
Coffee_df = HP_df['Coffee']
Coffee_timeseries = pd.concat([Coffee_df, date], axis=1).reindex(Coffee_df.index)
Coffee_timeseries.plot(x='DATE', y='Coffee')
# Iron
Iron_df= HP_df['Iron Bar']
Iron_timeseries = pd.concat([Iron_df, date], axis=1).reindex(Iron_df.index)
Iron_timeseries.plot(x='DATE', y='Iron Bar')

