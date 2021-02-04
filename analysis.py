
"""
Created on Tue Feb  2 10:52:18 2021

@author: bdaqqah
"""

"""
Importing libraries 
"""
import numpy as np
print ('Numpy version:', np.__version__)

import pandas as pd
print ('Pandas version:', pd.__version__)

import matplotlib as mpl
import matplotlib.pyplot as plt
print ('Matplotlib version:', mpl.__version__)

import seaborn as sns 


from datetime import datetime
import datetime
import time

from statsmodels.tsa.seasonal import seasonal_decompose


downloads = pd.read_csv('cs_downloads.csv', parse_dates=['date'])
#downloads = downloads.groupby(['ticker'])
usage = pd.read_csv('cs_usage.csv', parse_dates=['date'])

"""
Splitting Data
"""

lyft_d = downloads[downloads['ticker'] == 'LYFT']
uber_d = downloads[downloads['ticker'] == 'UBER']
lyft_u = usage[usage['ticker'] == 'LYFT']
uber_u = usage[usage['ticker'] == 'UBER']


"""
create a moving average and standard deviation for plotting 
"""
window = 15 
count = 0 
for df in [uber_d, lyft_d]: 
    df["Rolling_mean"]= df['total_downloads'].rolling(window).mean()
    df["Rolling_std"]= df['total_downloads'].rolling(window).std()
    plt.figure()
    plt.plot(df['date'], df["total_downloads"], color='#000000', label = "Total Downloads")
    ## rolling mean in red
    plt.plot(df['date'], df["Rolling_mean"], color='#FF0000', label = "Moving Average")
    ## rolling standard deviation in orange 
    plt.plot(df['date'], df["Rolling_std"], color='#FFA500', label = "Moving Standard Deviation")
    plt.xlabel('Date')
    plt.ylabel("Total Downloads")
    plt.legend()
    plt.show()
    
"""
Percent Change
"""
# a plot will be created to make sure that the result looks similar to the moving average 
## we got in the beginning 
count = 0 
plt.figure()

for df in [uber_d, lyft_d]: 
    #group every 7 days together and sum their values (total number of days)
    weekly_df = df.groupby(df.index // 7).sum()
    #insert the number of weeks as a column in the data frame
    weekly_df.insert(0, 'week', [i for i in range(1, len(weekly_df)+1)])
    weekly_returns = weekly_df['total_downloads'].pct_change()

    if count == 0: 
        company = "Uber"
        color = "#000000"
    else: 
        company = "Lyft"
        color = '#b80045'   
        
    plt.plot(weekly_df['week'], weekly_returns, color=color, label = company )
    
    count += 1
    
plt.title("Weekly Percent Change for both Uber and Lyft Total Downloads")
plt.xlabel('Week Number')
plt.ylabel("Weekly Percent Change")
plt.legend()
plt.show() 



"""
Weekdays Analysis 
"""
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
properties = ["total_time", "users", "sessions"]

def usage_plotting(df, prop, company, color): 
    plt.figure() 
    plt.plot(df["Day"], df[prop],color=color, label = company)
    plt.xlabel('Weekdays')
    plt.ylabel(prop)
    plt.legend()
    plt.show() 

## count 0 stands for uber, but 1 stands dfor lyft (just a way to keep 
#track of which company i'm plotting)
count = 0 

for df in [uber_u, lyft_u]: 

    weekdays_usage = df.groupby(df['date'].dt.weekday).mean()
    weekdays_usage["Day"] = days 
    if count == 0: 
        company = "Uber"
        color = "#000000"
        uber_weekdays_usage = weekdays_usage
    else: 
        company = "Lyft"
        color = '#b80045'
        lyft_weekdays_usage = weekdays_usage
        
    
    for prop in properties: 
        usage_plotting(weekdays_usage, prop, company, color)
    
    count += 1



"""
More analysis to get insight on lyft's odd trend of application usage during weekends'
"""

count = 0 
plt.figure() 
for df in [uber_weekdays_usage, lyft_weekdays_usage]:
    if count == 0: 
        company = "Uber"
        color = "#000000"
    else: 
        company = "Lyft"
        color = '#b80045'
    ##divide total time by the number of users 
    df["time_per_user"]= df["total_time"]/df["users"]
    plt.plot(df["Day"], df["time_per_user"],color=color, label = company)
    count += 1

plt.xlabel('Weekdays')
plt.ylabel('Time per user')
plt.legend()
plt.show() 


"""
Seasonality Analysis 
"""

lyft_d = lyft_d.set_index('date')
res = seasonal_decompose(lyft_d['total_downloads'],model='additive')
plt.rcParams['figure.figsize'] = (10, 8)
x = res.plot()

uber_d = uber_d.set_index('date')
res = seasonal_decompose(uber_d['total_downloads'],model='additive')
plt.rcParams['figure.figsize'] = (10, 8)
x = res.plot()


