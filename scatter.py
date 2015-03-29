import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullLocator, FormatStrFormatter
import itertools as it
import os

#list behavioral metrics and line number of methods for each file
columns = ["MOUSE TRACKER", "LINE FREQUENCY", "EYE TRACKER"]
methods = list()
methods.append([(14,17), (21,44), (48,55), (58,64), (67,70), (73,77), (82,89), (95,117), (123,143), (147,155), (161,171)])
methods.append([(26,80), (82,102), (105,170), (174,177), (181,188), (191,218), (221,246)])
methods.append([(4,15), (17,24), (26,39), (41,53), (55,62), (64,72), (74,77)])
methods.append([(15,88), (90,110), (113,152), (155,163), (165,168)])
methods.append([(9,59)])

#list metrics
metrics = [("Posnett's Halstead Metric", "Posnett"), ("Cyclomatic Complexity",
	"McCabe"), ("Buse's Metric", "Buse")]

#manual file number input
file_num = 4
fname = "File" + str(file_num) + ".xlsx"
#extract data from excel files


excel_file = pd.ExcelFile(fname)
#this is the file with all the readablity metrics
number_file = pd.ExcelFile("numbers.xlsx")
#extract extract and put in nice lists
sheets = []
for sheet in excel_file.sheet_names:
	sheets.append(excel_file.parse(sheet))

numbers = []
for sheet in number_file.sheet_names:
	numbers.append(number_file.parse(sheet))

for i in range(len(numbers)):
	numbers[i] = numbers[i][0:len(numbers[i])-2]

#average across participants
combined = sum(sheets)/len(sheets)

#make some dicts
average = dict()
aggregate = dict()
for column in columns:
	aggregate[column] = []
	average[column] = []

#get per method and per method per line
for method in methods[file_num-1]:
	for column in columns:
		agg = sum(combined[column][method[0]-1:method[1]])
		aggregate[column].append(agg)
		average[column].append(agg/((method[1] - method[0]) + 1))

#start laying out the graphs
fig, axes = plt.subplots(nrows=len(columns), ncols=len(metrics), figsize=(18, 10))

#actually plot the graphs and calculate the spear
for i in range(len(columns)):
	for x in range(len(metrics)):
		axes[i][x].scatter(aggregate[columns[i]], numbers[file_num-1][metrics[x][0]])
		axes[i][x].set_xlabel(columns[i] + "(aggr)")
		axes[i][x].set_ylabel(metrics[x][1])
		spear = pd.DataFrame(aggregate[columns[i]])[0].corr(pd.DataFrame(numbers[file_num-1][metrics[x][0]])[metrics[x][0]], method='spearman')
		axes[i][x].set_title("Spearman: " + str(spear))

#tighten layout
#fig.suptitle("Aggregates for File " + str(file_num))
plt.tight_layout()
plt.savefig("aggr_scatter" + str(file_num) + ".png")

#and repeat for average
fig, axes = plt.subplots(nrows=len(columns), ncols=len(metrics), figsize=(18, 10))

for i in range(len(columns)):
	for x in range(len(metrics)):
		axes[i][x].scatter(average[columns[i]], numbers[file_num-1][metrics[x][0]])
		axes[i][x].set_xlabel(columns[i] + "(avg)")
		axes[i][x].set_ylabel(metrics[x][1])
		spear = pd.DataFrame(average[columns[i]])[0].corr(pd.DataFrame(numbers[file_num-1][metrics[x][0]])[metrics[x][0]], method='spearman')
		axes[i][x].set_title("Spearman: " + str(spear))


#fig.suptitle("Averages for File " + str(file_num))
plt.tight_layout()
plt.savefig("avg.scatter" + str(file_num) + ".png")
