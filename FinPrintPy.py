# FinPlot.py -- plot nested bar graphs showing project utilisation
import plotly.express as px
import pandas as pd

# Open Data File
df = pd.read_csv("C:/C-Drive/GRST-TTS37-PRJ_YY_DATA_summary_FITID_YEAR2.csv")
# print(df.iloc[0]) # output the first record to terminal

class PrjRecordList:
    def __init__(self, df):
        self.df = df
        self.maxusd = 0
        self.maxact = 0
        self.numelem = 0
        self.maxlen = 142
        self.RipFile()

    def RipFile(self):
        for i, row in self.df.iterrows():
            usd = int(row["CB$SUM"][1:].replace(",", ""))
            act = int(row["ACT"][1:].replace(",", ""))
            self.maxusd = max(self.maxusd, usd)
            self.maxact = max(self.maxact, act)
            self.numelem = i
        return 1

    def PlotBar(self, val, act, month, i):
        budget = int(int(val[1:].replace(",", "")))
        actual = int(int(act[1:].replace(",", "")))
        print("[FIT-{}][{}] {}".format(self.df["FITID"][i],self.df["FITID_DDCID"][i],self.df["FITID_PRJNAME"][i]))
        strafrag1 = "[{}][{}]".format("$BUD", budget)
        strafrag2 = "[{}][{}]".format("$ACT", actual)
        print(strafrag1, end='')
        print(' ' * (13 - len(strafrag1)), end='|')
        if (budget >= actual):
            print('=' * self.maxlen, end='| ') # 100% len for available budget
        else:
            print('.' * self.maxlen, end='| ') # 100% len for given actual
        print(val)

        print(strafrag2, end='')
        print(' ' * (13 - len(strafrag2)), end='|')
        if (budget >= actual):
            # calculate % ratio based on the value
            if (budget != 0):
                actlen = round(((actual / budget) * self.maxlen))
                print('.' * int(actlen), round((actual / budget) * 100), end='')
            else:
                actlen = 0
                print(" 0", end='')
            print('%')
        else:
            print('=' * self.maxlen, end='| ')
        print()

recList = PrjRecordList(df)
print(recList.maxusd, recList.maxact, recList.numelem)

for i, row in recList.df.iterrows():
    recList.PlotBar(recList.df["CB$SUM"][i],recList.df["ACT"][i],7, i)