import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import statsmodels.api as sm 
from statsmodels.tsa.stattools import adfuller
from sklearn.decomposition import PCA

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

### PCA Analysis on Colonial Commodities Data
## Begin with timeseries1 with removed time column
# Also start with calculating change in PCs

cov_matrix = timeseries1.cov()

# PCA (fit & transform)

pca = PCA()
pca.fit_transform(cov_matrix)

# Explained variance

per_var = np.round(pca.explained_variance_ratio_*100,decimals=2)
labels = ['PC'+str(x) for x in range(1,len(per_var)+1)]
raw_bars = pd.DataFrame(per_var,index=labels) # quick dataframe to enable easy plotting of % variance explained by the principal components


# Check both raw_bars and cov_matrix for accuracy
print(raw_bars.head(5)) # PC1 Takes up majortiy of variance
print(cov_matrix.head(5))

#c Reduce prinipal components to the first 3 which have significance.

principal_components = raw_bars.iloc[0:3, :]
raw_bars.to_csv('1770-1790_change_PCs.csv')

# Now Calculating Raw PCs

# You must normalize the data before applying the fit method
timeseries1_normalized=(timeseries1 - timeseries1.mean()) / timeseries1.std()
pca = PCA(n_components=timeseries1.shape[1])
pca.fit(timeseries1_normalized)

# Reformat and view results
loadings = pd.DataFrame(pca.components_.T,
columns=['PC%s' % _ for _ in range(len(timeseries1_normalized.columns))],
index=timeseries1.columns)
date = timeseries['DATE']


# Keep Components Data in Seperate Excel File

loadings.to_csv('1770-1790_PCA_components.csv')
loadings.to_csv('C:/Users/Harry Murphy/OneDrive/Desktop/export.csv', index = None, header = True)

### Lagged Time Series Data for # Death and Commodities Price Indices

### Death # Time Series Regression

deaths= 'https://raw.githubusercontent.com/harrymmurphy/Commodities_American_Rev/main/Peckham%20Revolutionary%20War%20%23%20Death%20Timeseries%20-%20Sheet1.csv'
deaths_df= pd.read_csv(deaths)

deaths_df.rename(columns = {'m':'MONTH', 'y':'YEAR'}, inplace = True)
deaths_df['DATE'] = pd.to_datetime(data[['YEAR', 'MONTH']].assign(DAY=1))
deaths_timeseries = deaths_df.drop(['MONTH', 'YEAR'], axis = 1)

timeseries1_reduced =timeseries1.iloc[0:164,:]
cum_timeseries = pd.concat([timeseries1_reduced, deaths_timeseries], axis=1).reindex(timeseries1_reduced.index)

sns.lineplot(data=cum_timeseries.replace('nan', float('nan')).melt(id_vars=['DATE']),
             x='DATE', y= "value")
print(cum_timeseries.head(250))
# Visualize timeseries
sns.lineplot(data=deaths_timeseries .replace('nan', float('nan')).melt(id_vars=['DATE']),
             x='DATE', y= "value", hue='variable')


## Saving my savityzky_golay function for later. Don't use it here but wrote code for excercise
def savitzky_golay(y, window_size, order, deriv=0, rate=1):   
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError():
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

# ADF testing for stationary data

test = cum_timeseries.iloc[:,24:25]


from statsmodels.tsa.stattools import adfuller
def adf_test(self):
    dftest = adfuller(test, autolag='AIC')
    result = pd.Series(dftest[0:4], index=['Test Statistic', 'P-Value', 'Lags Used', 'Number of Observations'])
    for key,value in dftest[4].items():
        result['Critical Value (%s)'%key] = value
    return result
    print(result)
    
adf_test(test)



## Time Series Cross Correlation

def autocorr(self, lag=1):
    """
    Lag-N autocorrelation

    Parameters
    ----------
    lag : int, default 1
        Number of lags to apply before performing autocorrelation.

    Returns
    -------
    autocorr : float
    """
    return self.corr(self.shift(lag))

def crosscorr(datax, datay, lag=0):
    """ Lag-N cross correlation. 
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """
    return datax.corr(datay.shift(lag))
 
# Cross Correlation

wine = cum_timeseries.iloc[:,24:25]
death = cum_timeseries.iloc[:,25:26]
reg = sm.tsa.stattools.ccf(wine, death, adjusted=False)
print(reg[84:144]) # Show all coefficients for lags from 7 to 12 years


