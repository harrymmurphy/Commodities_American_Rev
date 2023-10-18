###### *NOTE: This is a working paper*
<h6>I am currently in the process of cleaning data, running analysis, and writing textual analysis on historical sources. I am hoping to blend a historical commentary on Merchant notebooks from 1770-1790 with deep statistical analysis on this robust dataset. Below are some initial models to fit the dataset. There are several key components to this paper that are currently missing. Most of the models currently here will likely stay in the final product. The Hodrick-Prescott filter and PCA reduction both give insights into the nature of the supercycle, specifically volatility behavior around the Revolutionary War. I am currently investigating more modern time series analysis techniques in macrofinance, but these should do for now.



The main components I am currently working on are the relationships between changes in colonial monetary regimes and commodities prices in this era. While I have the lagged regression with a proxy variable for strength of the War (a newly cleaned dataset on death counts per battle from Peckham (1974)), I am currently in the process of cleaning data from some early 20th century secondary sources with information on price indices for colonial coinage. There is A LOT of missing data as I am cleaning the coinage price indices, so I am currently looking into Machine Learning methods to fix this issue. 

# Commodities, Supercycles, and the American Revolution
Most supercycles identified in working commodities datasets from 1800-2023 show supercycles caused by warfare--including the Napleonic Wars, Civil War, World War I, World War II, and the Cold War (although it could be contested that the depreciation of the dollar upon the removal of the fixed-exchange rate caused this supercycle)--except the recent supercycle from 2005-2013. I identify a new supercycle from 1770-1790, and look to see if the American Revolution was causal for this supercycle, or if constant shifts in monetary regimes over this time period (and frequent re-defining of coinage standards) caused increases in commodities prices. 

# Data
This paper uses data from archival resources in the Historical Society of Pennsylvania and secondary source materials. Archival materials with price figures recorded and cleaned include The Logan Family Papers, 1664-1871, the McCall Family Papers, 1764-1891, and the Orr, Dunlap & Glenholme Letterbook, 1767-1769. Secondary sources include 
Anne Bezanson's "Prices and Inflation during the American Revolution: Pennsylvania, 1770-1790" (1951) and Anne Bezanson, R.D. Gray, and M. Hussey, "Prices in Colonial Pennsylvania." (1935)

The dataset includes price levels and indices on beaf, bread, corn, flour, gunpowder, molasses, pitch, pork, rice, salt, rum, staves, sugar, tar, turpentine, wheat, whine, copper, silver, chocolate, coffee, corn, indigo, iron bar, and leather.

For inference on the cause of this supercycle, this paper examines both number of death count during the Revolutionary War, as well as devaluation of local currencies because of changes in currency standards. For death figures on the Revolutionary War, I cleaned data from Peckham's "Toll of Independence" (1974). We use this dataset, as well as Grubb (2022) on coinage regime changes, to test casuality. 

# The Nature of the Supercycle


<img width="350" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/64c68896-9ac9-479e-b225-37143b75565b"> <img width="368" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/9c97368c-4313-4158-b3a8-d6cac47a8cc8">


# Methods
## For understanding the Supercycle
### Hodrick-Prescott (HP) Filter
Let Yt  for t = 1,2..T denote the logarithms of a time series variable. Yt is composed of a trend component, a cyclical component, and an error component, expressed as Yt = Ct + ERRORt. There is a trend component that can solve the following, given lamda > 0:

<img width="360" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/a4164e0e-747e-42eb-9f61-48d05172ddb7">

We use the Hodrick-Prescott filter to solve the "trend" component of this time series dataset. In the short term, we use this to approximate volatility in colonial commodities markets. The HP filter is given formally by:

<img width="319" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/a725e57e-abc7-4a43-904a-9ac03fb50b9f">

where L is the lag operator.

Lamda dampens volatility as it increases. We use Harold Uhlig's suggestion for 100*(period)^2 given a 12-month annual periodization. 
A quick word on the distributions. Interestingly, despite high prices throughout 1770-1790, there is certainly a volatility spike right around the revolutionary war. Vol during this period does not return for the remainder of the decade. 
# All Commodities
<img width="228" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/2d240908-aa93-481e-959e-7a7c56a12e2a">

# Chocolate
<img width="361" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/cb0ebd5f-f75e-4046-9bd5-a73ce7d4e355">

# Iron Bar
<img width="346" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/4563f72b-719d-4a3c-a405-e91067918f1a">

# Coffee
<img width="347" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/4c41a597-c002-47f0-8836-66e13add44a2">


### Principal Component Analysis (PCA) 
#### Principal Components
<img width="619" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/2ab3048d-bd9a-4b61-8bbc-e45ad6b2fa18">

#### Correlation Matrix (reduced)
One thing to note: the each commodity is highly correlated with each other, with beef, iron, gunpowder, coffee, and tobacco having the highest correlations. Perhaps there is something to note that commodities with higher correlations maybe havea  closer relationship to the war?
<img width="732" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/d4400685-8a16-4ac1-bb5d-f5d17745b4b1">

### Percent Explained by PCs
Most of the variance is explained by PC1. PC1 is the eigenvector which explains most of the information variance. In this case, since so much of the variance is left to PC1, there are not many sub-trends in the data to investigate. This is likely because I use monthly data.
<img width="360" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/a434dd09-05a0-44f6-bf97-8b2fd72b2e6a">

## For understanding the supercycle with respect to geopolitical events
### Lagged Time Series Regression

Unsmooted

<img width="676" alt="image" src="https://github.com/harrymmurphy/Commodities_American_Rev/assets/143562527/2f4acdb5-496b-46ac-8611-d88baa3ed34b">
Death Count and Supercycle plotted on same timeseries.

### Differences-in-Differences (DiD) Analysis
Once the coinage data is finished, I intend on applying applied econometric techniques for causal inference. Looking to detect the relationship between deflation of colonial paper money and commodities prices, and whether it is more causal for the supercycle as compared to the war. 

# Empirical Results

This is a more "paper-y" part that I will not include on Github, but I intend on doing textual analysis on Merchant books to contextualize price shifts in commodities markets. While we can try to intuit market behavior using modern applied econometrics and statistics, these guys had a closer pulse to markets. 

# Working Arguments
I am looking for stronger understanding of commodities cycles outside of Hodrick-Prescott. This is a really simple and outdated forecasting model. Also, I am looking to add some base metals to the dataset. This might add more robust results for the PCA PC2 and PC3 results. 
# Concluding Remarks
N/A

