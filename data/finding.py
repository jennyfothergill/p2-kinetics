#Finding data to be used in the code
#NYT csv files at: https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
#
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np

#import pandas as pd
#url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
#df = pd.read_csv(url, error_bad_lines=False)

#library(RCurl)
#x <- getURL(://"raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
#y <- read.csv(text = ix)
#
import pandas as pd
#url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
url = 'https://raw.githubusercontent.com/pydata/pydata-book/master/ch09/stock_px.csv'
#df = pd.read_csv(url,index_col=0,parse_dates=[0])

#print df()
#print(url)
print(pd.read_csv)
