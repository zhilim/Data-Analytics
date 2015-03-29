import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullLocator, FormatStrFormatter
import itertools as it
import os

columns = ["MOUSE TRACKER", "LINE FREQUENCY", "EYE TRACKER", "CARET", "HIGHLIGHT"]

major = []
for filename in os.listdir(os.getcwd()):
	if filename.startswith("File") and filename.endswith(".xlsx"):
		file_num = int(filename[4])
		excel_file = pd.ExcelFile(filename)
		sheets = []
		for sheet in excel_file.sheet_names:
			sheets.append(excel_file.parse(sheet))
		combined = sum(sheets)/len(sheets)
		major.append(combined)

df = pd.concat(major)
combi = list(it.combinations(columns, 2))
correlations = list()
for pair in combi:
	correlations.append(df[pair[0]].corr(df[pair[1]], method="spearman"))

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 18), sharex=False)

ax.bar(range(0, len(combi)*2, 2), correlations)
ax.set_xticks(range(0, len(combi)*2, 2))
ax.set_xticklabels(combi, rotation='vertical')
ax.set_xlabel("Data Pairs")
ax.set_ylabel('Spearman Correlations for All')
ax.set_title("")

ax.get_figure().suptitle("")


fig.tight_layout()
fig.suptitle("Spearman", fontsize=20)

# df.boxplot(column=columns, by="LINE NUMBER")

plt.savefig("spearman_all.png")