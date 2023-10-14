import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm 
import sklearn

1720_1775 = "https://raw.githubusercontent.com/harrymmurphy/Commodities_American_Rev/main/1720-1775%20-%20Sheet1.csv"
1770_1790 = "https://raw.githubusercontent.com/harrymmurphy/Commodities_American_Rev/main/1770-1790%20-%20Sheet1.csv"

1770_1790 = pd.read_csv(1770-1790)
1720_1775 = pd.read_csv(1720-1775)
# Inspect DF
print(1770-1790.head(5))
print(1720-1775.head(5))
