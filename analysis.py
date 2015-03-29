import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullLocator, FormatStrFormatter
import itertools as it

columns = ["MOUSE TRACKER", "HIGHLIGHT", "LINE FREQUENCY", "EYE TRACKER", "CARET"]

excel_file = pd.ExcelFile("File5.xlsx")
sheets = []
for sheet in excel_file.sheet_names:
	sheets.append(excel_file.parse(sheet))

for sheet in sheets:
	for i in range(len(columns)):
		column_sum = float(sheet[columns[i]].sum())
		if(column_sum != 0):
			sheet[columns[i]] = sheet[columns[i]] / column_sum
df = pd.concat(sheets)
codelen = len(sheet)
width = int (codelen/10)

average = sheets[0]
for i in range(1, len(sheets)):
	average = average + sheets[i]
average = average / len(sheets)

fig, axes = plt.subplots(nrows=len(columns)+1, ncols=1, figsize=(width, 5 * len(columns)), sharex=False)

#plt.suptitle("File4.xlsx")

major_locator = MultipleLocator(20)
major_formatter = FormatStrFormatter('%d')
minor_locator = MultipleLocator(5)

for i in range(len(columns)):
	separated = pd.DataFrame(df, columns=["LINE NUMBER", columns[i]])
	separated.boxplot(column=columns[i], ax=axes[i], by="LINE NUMBER", return_type="axes", sym="", showfliers=False)

	axes[i].xaxis.set_major_locator(major_locator)
	axes[i].xaxis.set_major_formatter(major_formatter)
	axes[i].xaxis.set_minor_locator(minor_locator)
	
	axes[i].set_xlabel("")
	axes[i].set_xticks(range(0,codelen,10))
	axes[i].set_ylabel(columns[i])
	axes[i].set_title("")

	axes[i].get_figure().suptitle("")

axes[i].set_xlabel("LINE NUMBER")
axes[i].set_xticks(range(0,codelen,10))

i = i + 1
axes[i].xaxis.set_major_locator(major_locator)
axes[i].xaxis.set_major_formatter(major_formatter)
axes[i].xaxis.set_minor_locator(minor_locator)

combi = list(it.combinations(columns, 2))
correlations = list()
for pair in combi:
	correlations.append(average[pair[0]].corr(average[pair[1]], method='spearman'))
axes[i].bar(range(0, len(combi)*2, 2), correlations)
axes[i].set_xticks(range(0, len(combi)*2, 2))
axes[i].set_xticklabels(combi, rotation='vertical')
axes[i].set_xlabel("Data Pairs")
axes[i].set_ylabel('Spearman Correlations')
axes[i].set_title("")

axes[i].get_figure().suptitle("")


fig.tight_layout()
fig.suptitle("File 5", fontsize=20)

# df.boxplot(column=columns, by="LINE NUMBER")

plt.savefig("plot5.png")






