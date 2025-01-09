import json
import sys
import pandas as pd

jsonInputName = sys.argv[1]

jsonfile = open(jsonInputName, 'r')
statsDict = json.load(jsonfile)

statsList = []
nameList = []
for key, value in statsDict.items():
    statsList.append(value)
    nameList.append(key)

stats_df = pd.DataFrame(statsList)
stats_df = stats_df.transpose()
stats_df.columns = nameList

stats_df = stats_df.apply(pd.to_numeric)


print(stats_df.to_markdown(floatfmt=".3f"))

stats_df.to_csv('stats.csv', float_format='%.3f')
