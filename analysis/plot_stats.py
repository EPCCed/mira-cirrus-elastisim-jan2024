import json
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

jsonInputName = sys.argv[1]

jsonfile = open(jsonInputName, 'r')
statsDict = json.load(jsonfile)

statsList = []
nameList = []
for key, value in statsDict.items():
    value['Name'] = key
    statsList.append(value)
    nameList.append(key)

stats_df = pd.DataFrame(statsList)
print(stats_df)

ax = sns.barplot(data=stats_df, y='Name', x='medianWait')
ax.set_xlabel('Median wait (h)')
sns.despine()
plt.savefig('medianWait.png', dpi=300, bbox_inches='tight')

ax.cla()
ax = sns.barplot(data=stats_df, y='Name', x='usageFraction')
ax.set_xlabel('Use fraction')
sns.despine()
plt.savefig('useFraction.png', dpi=300, bbox_inches='tight')