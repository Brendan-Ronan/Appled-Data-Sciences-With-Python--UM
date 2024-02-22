%matplotlib inline

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
import pandas as pd
import numpy as np

avg = []
std = []
for year in range(1992,1996):
    avg.append(df[str(year)].mean())
    std.append(df[str(year)].std())
    
import math 

n = len(df)
z = 1.96

lower = []
upper = []
ci = []
for year in range(1992,1996):
    lower.append(avg[year-1992] - (z*(std[year-1992]/math.sqrt(n))))
    upper.append(avg[year-1992] + (z*(std[year-1992]/math.sqrt(n))))
    ci.append(upper[year-1992] - lower[year-1992])


norm = Normalize(vmin=-1.96, vmax=1.96)
cmap = get_cmap('seismic')
df_c = pd.DataFrame(index = [0,1,2,3], columns = ['Value', 'Color'])

y=40000

for i in range(0,4):
    df_c['Value'][i] = norm((avg[i]-y)/std[i])
    
df_c['Color'] = [cmap(x) for x in df_c['Value']]

generic = [0,1,2,3]
x = ['1992', '1993', '1994', '1995']

plt.figure(figsize=(10,8))
plt.bar(generic, avg, yerr=ci, color=df_c['Color'])
plt.axhline(y=y, color = 'black', alpha=.3)

plt.text(3.65, y, 'y=%d' %y)
plt.xticks(generic, x)
plt.xlabel('Year')
plt.ylabel('Mean Votes')
plt.title('Average Votes per Year')
