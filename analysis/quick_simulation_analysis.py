import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
import csv
import json
import pandas as pd
import math
import statistics
import argparse

# Constants - currently for Cirrus CPU
nCoreTot = 13248 # Total cores available
timeLower = 500000 # Start time of analysis window
timeUpper= 2800000 # End time of analysis window

# Parse command line arguments
parser = argparse.ArgumentParser(description='Analyse results of Elastisim scheduler simulation.')
parser.add_argument('-p', dest='prefix', type=str, action='store', default='elastisim', help='Prefix to use for output files. Default: "elastisim"')
parser.add_argument('-d', dest='datadir', type=str, action='store', default=".", help='Directory containing output files from Elastisim simulation. Output files must be called "node_utilization.csv" and "job_statistics.csv". Default: current directory.')
parser.add_argument('-i', dest='inputjson', type=str, action='store', default=None, required=True, help='Elastisim input JSON job list file. No default.')
args = parser.parse_args()

# Setup the file names
jsonInputName = args.inputjson
csvJobStatsName = f'{args.datadir}/job_statistics.csv'
csvNodeUtilizationName = f'{args.datadir}/node_utilization.csv'

histSizePlotFile = f'{args.prefix}_size_hist.png'
statsJSON = f'{args.prefix}_simulation_stats.json'

csvfile = open(csvJobStatsName, 'r')

csvreader = csv.DictReader(csvfile)
jobList = []
for row in csvreader:
    jobList.append(row)

jsonfile = open(jsonInputName, 'r')
jobDict = json.load(jsonfile)
i = 0
maxtime = 0
totuse = 0
jobidList = []
for job in jobDict['jobs']:
    jobidList.append(job['arguments']['jobid'])
    jobList[i]['JobID'] = job['arguments']['jobid']
    jobList[i]['BaseNodes'] = int(job['arguments']['base_nodes'])
    if job['type'] == 'moldable':
        jobList[i]['MinNodes'] = int(job['num_nodes_min'])
        jobList[i]['MaxNodes'] = int(job['num_nodes_max'])
    else:
        jobList[i]['MinNodes'] = int(job['num_nodes'])
        jobList[i]['MaxNodes'] = int(job['num_nodes'])
    i += 1

nodedata_df = pd.read_csv(csvNodeUtilizationName)
nodedata_df['Count'] = 1
nodedata_df.tail()

nodecount_grouped = nodedata_df.loc[nodedata_df['State'] == 'allocated'].groupby(by='Running jobs', sort=False)['Running jobs'].count()

for i, job in enumerate(jobList):
    cores = nodecount_grouped.iloc[i]
    jobList[i]['Nodes'] = cores
    totuse = totuse + float(jobList[i]['Makespan']) * jobList[i]['Nodes']
    if float(jobList[i]['End Time']) > maxtime:
        maxtime = math.ceil(float(jobList[i]['End Time']))

job_df = pd.DataFrame(jobList)
job_df['Start Time'] = job_df['Start Time'].astype(float)
job_df['Wait Time'] = job_df['Wait Time'].astype(float)
job_df['End Time'] = job_df['End Time'].astype(float)
job_df['Nodes'] = job_df['Nodes'].astype(int)
job_df['Makespan'] = job_df['Makespan'].astype(float)
job_df['Coreh'] = job_df['Makespan'] * job_df['Nodes'] / 3600.0
job_df['Turnaround Time'] = job_df['Turnaround Time'].astype(float)
job_df['Efficiency'] = job_df['Makespan'] / job_df['Turnaround Time']
job_df['Fractional Size Change'] = job_df['Nodes']/job_df['BaseNodes']

nrigid = len(job_df.loc[job_df['Nodes'] == job_df['BaseNodes']])
nmoldable = len(job_df.loc[job_df['Nodes'] != job_df['BaseNodes']])
nlarger = len(job_df.loc[job_df['Nodes'] > job_df['BaseNodes']])
nsmaller = len(job_df.loc[job_df['Nodes'] < job_df['BaseNodes']])
ntot = len(job_df)

print(f"\n\nMoldability statistics (full dataset):")
print(f'Number of jobs at original size = {nrigid}/{ntot} ({100*nrigid/ntot:.2f}%)')
print(f'Number of jobs molded = {nmoldable}/{ntot} ({100*nmoldable/ntot:.2f}%)')
print(f'Number of jobs larger = {nlarger}/{ntot} ({100*nlarger/ntot:.2f}%)')
print(f'Number of jobs smaller = {nsmaller}/{ntot} ({100*nsmaller/ntot:.2f}%)')

sns.set_context("paper")
sns.set_style("ticks")
sns.histplot(data=job_df, x='Fractional Size Change', bins=50, stat='percent')
sns.despine()
plt.savefig(histSizePlotFile, dpi=300)

maxUsage = (timeUpper - timeLower) * nCoreTot

# Descriptive statistics
stats = {}

stats['nJobStart'] = sum((job_df['Start Time'] >= timeLower) & (job_df['Start Time'] <= timeUpper))

print(f"\n\nSimulation statistics (analysis period):")
print(f"\nJob data:")
print(f"    nJobs = {stats['nJobStart']}")

slice_df = job_df.loc[(job_df['Start Time'] >= timeLower) & (job_df['Start Time'] <= timeUpper)]
stats['minWait'] = slice_df['Wait Time'].min() / 3600
stats['medianWait'] = slice_df['Wait Time'].median() / 3600
stats['maxWait'] = slice_df['Wait Time'].max() / 3600
stats['meanWait'] = slice_df['Wait Time'].mean() / 3600

print(f"\nWait time statistics:")
print(f"    min = {stats['minWait']}")
print(f" median = {stats['medianWait']}")
print(f"    max = {stats['maxWait']}")
print(f"   mean = {stats['meanWait']}")

stats['minTurnaroundTime'] = slice_df['Turnaround Time'].min() / 3600
stats['medianTurnaroundTime'] = slice_df['Turnaround Time'].median() / 3600
stats['maxTurnaroundTime'] = slice_df['Turnaround Time'].max() / 3600
stats['meanTurnaroundTime'] = slice_df['Turnaround Time'].mean() / 3600

print(f"\nTurnaround time statistics:")
print(f"    min = {stats['minTurnaroundTime']}")
print(f" median = {stats['medianTurnaroundTime']}")
print(f"    max = {stats['maxTurnaroundTime']}")
print(f"   mean = {stats['meanTurnaroundTime']}")

