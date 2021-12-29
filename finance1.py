import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

## Asks user to input their selected stock
stock = input("Enter a stock ticker symbol: ")
print(stock)

## Creating A Time Frame (from Jan 1 2019 to Current Moment)
startyear = 2018
startmonth = 1
startday = 1
start = dt.datetime(startyear, startmonth, startday)
now = dt.datetime.now()

## Creates data table with inputted stocks from time frame specified above
df = pdr.get_data_yahoo(stock, start, now)

##  SIMPLE MOVING AVERAGE ##

# ma = 50 #moving average, 50 days selected currently
# smaString = "Sma_" + str(ma) #moving average string

# df[smaString] = df.iloc[:,4].rolling(window=ma).mean() #adds 50 day average collumn to table
# df = df.iloc[ma:] #removes first 50 entries

# numH = 0
# numC = 0

# for i in df.index:
#     if(df["Adj Close"][i] > df[smaString][i]):
#         print("The close is higher")
#         numH += 1
#     else:
#         print("The close is lower")
#         numC += 1

# print(str(numH))
# print(str(numC))

##  EXPONENTIAL MOVING AVERAGE ##

#different periods of exponential moving averages we need
emasUsed = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]

for ema in emasUsed:
    df["Ema_" + str(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(), 2) 

print(df.tail())

pos=0
num=0
percentchange=[]

for i in df.index:
    cmin = min(df["Ema_3"][i], df["Ema_5"][i], df["Ema_8"][i], df["Ema_10"][i], df["Ema_12"][i], df["Ema_15"][i])
    cmax = max(df["Ema_30"][i], df["Ema_35"][i], df["Ema_40"][i], df["Ema_45"][i], df["Ema_50"][i], df["Ema_60"][i])
    close = df["Adj Close"][i]
    if(cmin > cmax):
        print("Red White Blue")
        if(pos == 0):  ## Buying if cross over and we have no stock
            buyPrice = close
            pos = 1
            print("Buying now at " + str(buyPrice))
    elif(cmin < cmax):
        print("Blue White Red")
        if(pos == 1): ## Selling if cross over and we have stock
            pos = 0
            sellPrice = close
            print("Selling now at " + str(sellPrice))
            pc = (sellPrice/buyPrice-1) * 100
            percentchange.append(pc)
    if(num == df["Adj Close"].count() - 1 and pos == 1):
        pos = 0
        sellPrice = close
        print("Selling now at " + str(sellPrice))
        pc = (sellPrice/buyPrice-1) * 100
        percentchange.append(pc)
    num += 1

print(percentchange)

## Calculating sucess of a strategy
gains = 0
ng = 0 #number of gains
losses = 0
nl = 0 #number of losses
totalR = 1

for i in percentchange:
    if(i>0):
        gains += i
        ng += 1
    else:
        losses += i
        nl += 1 
    totalR = totalR * ((i / 100) + 1)

totalR = round((totalR - 1) * 100, 2)

if(ng > 0):
    avgGain = gains / ng
    maxR = str(max(percentchange))
else:
    avgGain = 0
    maxR = "undefined"

if(nl > 0):
    avgLoss = losses / nl
    maxL = str(min(percentchange))
    ratio=str(-(avgGain / avgLoss))
else:
    avgLoss = 0
    maxL = "undefined"
    ratio = "infinite"

if(ng > 0 or nl > 0):
    battingAverage = ng / (ng + nl)
else:
    battingAverage = 0

#Console Printing Output Summary
print()
print("Statistics results for " + stock + " going back to " + str(df.index[0]) + ", Sample size: " + str(ng + nl)) 
print("EMAs used were " + str(emasUsed))
print("Batting Average: " + str(battingAverage))
print("Gain/Loss ratio: " + str(ratio))
print("Average Gain: " + str(avgGain))
print("Average Loss: " + str(avgLoss))
print("Max Return: " + str(maxR))
print("Max Loss: " + str(maxL))
print("Total returns over " + str(ng + nl) + " trades: " + str(totalR) + "%")
print()


    
