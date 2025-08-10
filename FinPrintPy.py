# FinPlot.py -- plot nested bar graphs showing project utilisation
import pandas as pd

# Open Data File
df = pd.read_csv("C:/C-Drive/GRST-TTS37-PRJ_YY_DATA_summary_FITID_YEAR2.csv")

class PrjRecordList:
    def __init__(self, df):
        self.df = df
        self.maxusd = 0
        self.maxact = 0
        self.numelem = 0
        self.maxlen = 144
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
        print("[FIT-{}][{}] {}".format(self.df["FITID"][i],self.df["FITID_DDCID"][i],self.df["FITID_PRJNAME"][i])) # line 1
        strafrag1 = "[{}][{}]".format("$BUD", budget)
        strafrag2 = "[{}][{}]".format("$ACT", actual)
        print(strafrag1, end='') # line 2
        print(' ' * (13 - len(strafrag1)), end='|')

        if (budget >= actual):
            # divide the budget line into pre and post YTD - print preYTD red and postYTD green
            preYTDmult = int((self.maxlen / 12) * month)
            postYTDmult = int((self.maxlen / 12) * (12 - month))
            print('\033[34m=' * preYTDmult, end='\033[0m')
            print('\033[31m=' * postYTDmult, end='\033[0m| ')
            print(val)

            print(strafrag2, end='') # line 3
            print(' ' * (13 - len(strafrag2)), end='|')

            # calculate % ratio based on the value
            if (budget > 0):
                actlen = int(round(((actual / budget) * self.maxlen)))
                actlen1 = actlen
                if (actlen > 0):
                    actlen1 = actlen
                elif (actlen < 1):
                    actlen1 = 0
                sign = '?'
                delta = int(self.df["DELTA"][i][:-1].replace(",", ""))
                if (delta >= 100):
                    delta = delta - 100
                    sign = '+'
                elif (delta < 100) and (delta > 0):
                    delta = 100 - delta
                    sign = '-'
                elif (delta == 0):
                    sign = ''

                if (actlen > 0):
                    print("{} [{}%][{}{}]".format((('-' * actlen1) + 'o'), (round((actual / budget) * 100)), sign, delta))
                else:
                    print("{} [{}%][{}{}]".format(('-' * actlen1), (round((actual / budget) * 100)), sign, delta))
            else: # budget is 0
                actlen = 0
                print(" [0%][0]")
        else: # budget < actual
            if (actual > 0):
                if (budget > 0):
                    budlen = round(((budget / actual) * self.maxlen))
                    # divide the budget line into pre and post YTD - print preYTD red and postYTD green
                    preYTDmult = int((budlen / 12) * month)
                    postYTDmult = int((budlen / 12) * (12 - month))
                    print('\033[34m=' * preYTDmult, end='\033[0m')
                    print('\033[31m=' * postYTDmult, end='\033[0m| ')
                    print(val)

                    print(strafrag2, end='')  # line 3
                    print(' ' * (13 - len(strafrag2)), end='|')
                    print(('-' * (self.maxlen - 1) + 'o'), end=' ')

                    print("{}%".format(round((actual / budget) * 100)))
                else: # budget is 0
                    print(' $0')
                    print('[$ACT][0]    | 0%')
            else: # actual is 0
                budlen = 0
                print(" 0%")
        print()

recList = PrjRecordList(df)
print(recList.maxusd, recList.maxact, recList.numelem)

for i, row in recList.df.iterrows():
    recList.PlotBar(recList.df["CB$SUM"][i],recList.df["ACT"][i],7, i)