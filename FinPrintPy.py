# FinPlot.py -- plot nested bar graphs showing project utilisation
import pandas as pd

from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"default": "white on grey11", "repr.number": "white on grey11"})
#custom_theme = Theme({"default": "grey89 on grey0", "repr.number": "grey89"})  # Invert default style (black text on white -> white text on black)
console = Console(record=True, soft_wrap=False, width=148, theme=custom_theme)

# Open Data File
df = pd.read_csv("C:/C-Drive/GRST-TTS37-25AUG.csv")

class PrjRecordList:
    def __init__(self, df):
        self.df = df
        self.maxusd = 0
        self.maxact = 0
        self.numelem = 0
        self.maxlen = 120
        self.RipFile()

    def RipFile(self):
        for i, row in self.df.iterrows():
            usd = int(row["USD"][1:].replace(",", ""))
            act = int(row["ACT"][1:].replace(",", ""))
            self.maxusd = max(self.maxusd, usd)
            self.maxact = max(self.maxact, act)
            self.numelem = i
        return 1

    def PlotBar(self, val, act, month, i):
        budget = int(int(val[1:].replace(",", "")))
        actual = int(int(act[1:].replace(",", "")))
        console.print("[FIT-{}][{}] {}".format(self.df["FITID"][i],self.df["DDC"][i],self.df["PRJ"][i])) # line 1
        strafrag1 = "[{}][{}]".format("$BUD", budget)
        strafrag2 = "[{}][{}]".format("$ACT", actual)
        console.print(strafrag1, end='') # line 2
        console.print(' ' * (13 - len(strafrag1)), end='|')

        if (budget >= actual):
            # divide the budget line into pre and post YTD - print preYTD red and postYTD green
            if (budget > 0):
                preYTDmult = int((self.maxlen / 12) * month)
                postYTDmult = int((self.maxlen / 12) * (12 - month))
                console.print('[bright_cyan]=[/bright_cyan]' * preYTDmult, end='')
                console.print('[bright_red]=[/bright_red]' * postYTDmult, end='| ')
                console.print(val)

                console.print(strafrag2, end='') # line 3
                console.print(' ' * (13 - len(strafrag2)), end='|')

                # calculate % ratio based on the value
                actlen = int(round(((actual / budget) * self.maxlen)))
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
                    console.print("[bright_green]{}[/bright_green] [{}%][{}{}]".format((('-' * actlen) + 'o'), (round((actual / budget) * 100)), sign, delta))
                else:
                    console.print("[bright_green]{}[/bright_green] [{}%][{}{}]".format(('-' * actlen), (round((actual / budget) * 100)), sign, delta))
            else: # budget is 0
                console.print(" $0")
                console.print(strafrag2, end='')  # line 3
                console.print(' ' * (13 - len(strafrag2)), end='|')
                if (actual > 0):
                    console.print("{}".format(('-' * self.maxlen) + 'o'))
                else: # actual = 0
                    console.print(" [0%]") # ACT line add on
        else: # budget < actual
            if (actual > 0):
                if (budget > 0):
                    budlen = round(((budget / actual) * self.maxlen))
                    # divide the budget line into pre and post YTD - print preYTD red and postYTD green
                    preYTDmult = int((budlen / 12) * month)
                    postYTDmult = int((budlen / 12) * (12 - month))
                    console.print('[bright_cyan]=[/bright_cyan]' * preYTDmult, end='')
                    console.print('[bright_red]=[/bright_red]' * postYTDmult, end='| ')
                    console.print(val)

                    console.print(strafrag2, end='')  # line 3
                    console.print(' ' * (13 - len(strafrag2)), end='|')
                    console.print(('[bright_green]-[/bright_green]' * (self.maxlen - 1) + 'o'), end=' ')

                    console.print("{}%".format(round((actual / budget) * 100)))
                else: # budget is 0
                    console.print(' $0')
                    console.print(strafrag2, end='')  # line 3
                    console.print(' ' * (13 - len(strafrag2)), end='|')
                    console.print("[bright_green]{}[/bright_green] ${}".format(('-' * self.maxlen) + 'o', actual))
            else: # actual is 0
                console.print(" 0%")
        console.print()

# MAIN PROGRAM SECTION
recList = PrjRecordList(df)

console.print() # generate initial space at the top of the printout
for i, row in recList.df.iterrows():
    recList.PlotBar(recList.df["USD"][i].strip(),recList.df["ACT"][i].strip(),8, i)

# Export to HTML
html_content = console.export_html(inline_styles=True)
# Save to HTML file
html_file = "C:/C-Drive/colored_output.html"
with open(html_file, 'w') as f:
    f.write(f'''
    <!DOCTYPE html>
    <html><head><title>Colored Console Output</title>
        <style>
            body {{ background-color: #1C1C1C !important; margin: 0; padding: 10px; }}
            pre {{ font-family: monospace; white-space: pre; color: #BCBCBC !important; background-color: #1C1C1C !important; margin: 0; }}
            .rich-terminal {{ background-color: #1C1C1C !important; color: #BCBCBC !important; width: 100%; height: 100%;}}
            div, span {{ background-color: transparent !important; }}
            .rich-terminal > pre > div {{ background-color: #1C1C1C !important; }}
        </style>
    </head><body>
    <div class="rich-terminal">{html_content}</div>
    </body></html>
    ''')

print(f"HTML saved as '{html_file}'")