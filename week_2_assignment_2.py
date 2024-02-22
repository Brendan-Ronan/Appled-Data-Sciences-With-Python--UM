import pandas as pd
df = pd.read_csv('assets/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df.head()

# In this code cell, transform the Data_Value column
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

minimum = []
maximum = []

df['Data_Value'] = df['Data_Value'] / 10 # transform the Data_value column to Celsius 

df = df[~(df['Date'].str.endswith(r'02-29'))]  # remove leap year entries 
times = pd.DatetimeIndex(df['Date']) # convert to DatetimeIndex 

df1 = df[times.year != 2015] # create new df for all years except 2015
times1 = pd.DatetimeIndex(df1['Date']) # convert to DatetimeIndex

for j in df1.groupby([times1.month, times1.day]): # group data in df1 by month & day
    minimum.append(min(j[1]['Data_Value'])) # add each min value to minimum list
    maximum.append(max(j[1]['Data_Value'])) # add each max value to maximum list

df2015 = df[times.year == 2015] # df for year 2015
times2015 = pd.DatetimeIndex(df2015['Date']) # convert to DatetimeIndex

# min & max list for 2015
minimum2015 = []
maximum2015 = []

# grouping data by month and day for 2015
for j in df2015.groupby([times2015.month, times2015.day]):
    minimum2015.append(min(j[1]['Data_Value']))
    maximum2015.append(max(j[1]['Data_Value']))

# create lists to store values where 2015 temps are lower/higher than previous decade 
minaxis = []
maxaxis = []
minvals = []
maxvals = []

# iterate min and max values and append to lists
for i in range(len(minimum)):
    
    if((minimum[i] - minimum2015[i]) > 0):
       minaxis.append(i)
       minvals.append(minimum2015[i])
        
    if((maximum[i] - maximum2015[i]) < 0):
       maxaxis.append(i)
       maxvals.append(maximum2015[i])

import matplotlib.pyplot as plt
from calendar import month_abbr

# create new figure
plt.figure(figsize=(12,8))

# set colors
colors = ['lightgrey', 'lightseagreen', 'lightcoral']

# plot max and min temps 2005-2014
plt.plot(maximum, c='lightcoral', alpha=0.5, label='Max Temp 2005-2014')
plt.plot(minimum, c='lightseagreen', alpha=0.5, label='Min Temp 2005-2014')

# scatter plots for max and min records 2015
plt.scatter(maxaxis, maxvals, s=10, c='red', label='Max Record 2015')
plt.scatter(minaxis, minvals, s=10, c='darkslategrey', label='Min Record 2015')

# fill area between min and max lines
plt.gca().fill_between(range(len(minimum)), minimum, maximum, facecolor='lightgrey', alpha=0.5)

# set y axis limits
plt.ylim(-50, 50)

# remove plot frame
for spine in plt.gca().spines.values():
    spine.set_visible(False)

# formatting 
plt.legend(loc=8, frameon=False, fontsize=8)

# x-axis ticks and labels 
plt.xticks(np.linspace(15,15+30*11, num=12), (r'Jan', r'Feb', r'Mar', r'Apr', r'May', r'June', r'July', r'Aug', r'Sep', r'Oct', r'Nov', r'Dec',))
plt.ylabel('Temp (C)')
plt.title(r'Ann Arbor Temperature Levels 2004-2015')

plt.show()






