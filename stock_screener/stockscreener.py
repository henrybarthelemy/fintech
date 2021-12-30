import datetime as dt
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import yfinance as yf
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from pandas import ExcelWriter

yf.pdr_override()
start = dt.datetime(2017, 12, 1)
now = dt.datetime(2020, 1, 24) #tutorial is from feb 2020

# root = Tk()
# ftypers = [(".xlsm", ".xlsx", ".xls")]
# ttk = "Title"
# dir1 = 'C:\\'
# filePath = askopenfilename(filetypes = ftypes, initaldir = dir1, title = ttl)
filePath = r"/Users/henrybarthelemy/Desktop/fintechgit/stock_screener/stockstoscreen.xlsx"

stocklist = pd.read_excel(filePath)
stocklist = stocklist.head()

exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

for i in stocklist.index:
    stock = str(stocklist["Symbol"][i])
    RS_Rating = stocklist["RS Rating"][i]
    

    try:
        df = pdr.get_data_yahoo(stock, start, now)
        smaUsed = [50, 150, 200]
        for sma in smaUsed:
            df["SMA_" + str(sma)] = round(df.iloc[:,4].rolling(window=sma).mean(), 2)
        
        currentClose = df["Adj Close"][-1]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        low_of_52week = min(df["Adj Close"][-260:])
        high_of_52week = max(df["Adj Close"][-260:])

        try: #tries to set moving average from 20 days ago, if dne then sets to 0
            moving_average_200_20past = df["SMA_150"][-20]
        except Exception:
            moving_average_200_20past = 0

        print("Checking "+ stock + ".....")
        
        #Condition 1: Current Price > 150 SMA and > 200 SMA
        cond1 = currentClose > moving_average_150 and currentClose > moving_average_200
        
		#Condition 2: 150 SMA and > 200 SMA
        cond2 =  moving_average_150 > moving_average_200

		#Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        cond3 = moving_average_200 > moving_average_200_20past

		#Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        cond4 = moving_average_50 > moving_average_150 and moving_average_50 > moving_average_200

		#Condition 5: Current Price > 50 SMA
        cond5 = currentClose > moving_average_50

		#Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
        cond6 = currentClose >= (1.3 * low_of_52week)

		#Condition 7: Current Price is within 25% of 52 week high
        cond7 = currentClose >= (0.75 * high_of_52week)

		#Condition 8: IBD RS rating >70 and the higher the better
        cond8 = RS_Rating > 70

        print("cond1 " + str(cond1))
        print("cond2 " + str(cond2))
        print("cond3 " + str(cond3))
        print("cond4 " + str(cond4))
        print("cond5 " + str(cond5))
        print("cond6 " + str(cond6))
        print("cond7 " + str(cond7))
        print("cond9 " + str(cond8))

        if(cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8):
            exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
    except Exception:
        print("No data on " + stock)

print(exportList)

#creates a new excel file with the data on it
newFilePath = os.path.dirname(filePath) + "/ScreenOutput.xlsx"
writer = ExcelWriter(newFilePath)
exportList.to_excel(writer, "Sheet1")
writer.save()