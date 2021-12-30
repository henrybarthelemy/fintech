import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import hutils as hu
from pandas_datareader import data as pdr

#yahoo finance sidestep
yf.pdr_override()

#Asking user for stock ticket
stock = input("Please enter a stock ticket to backtrack short term trades on: ")
print("Runinng research tactics on : " + stock)


#Time frame for data table
sYear = 2019
sMonth = 1
sDay = 1
startDate = dt.datetime(sYear, sMonth, sDay)
now = dt.datetime.now()

#Setting up data table for stock
df = pdr.get_data_yahoo(stock, startDate, now)

## SHORT TERM RSI STRATEGY ##

# Setting up RPI w/ window of 6 days on datatable
window = 14
delta = df['Adj Close'].diff(1).dropna()
loss_rpi = delta.copy()
gains_rpi = delta.copy()

gains_rpi[gains_rpi < 0] = 0
loss_rpi[loss_rpi > 0] = 0

gain_ewm = gains_rpi.ewm(com=window - 1, adjust=False).mean()
loss_ewm = abs(loss_rpi.ewm(com=window - 1, adjust=False).mean())

RS = gain_ewm / loss_ewm
df["RSI_6"] = 100 - 100 / (1 + RS)
df = df.iloc[window:]

percentChangeRSI = []
pos = 0
num = 0

for i in df.index:
    currentRSI = df["RSI_6"][i]
    close = df["Adj Close"][i]
    if(currentRSI < 50): #if RSI is below 30, we buy
        if(pos == 0):
            buyPrice = close
            pos = 1
    elif(currentRSI > 90): #if RSI is above 70, we sell
        if(pos == 1):
            sellPrice = close
            pos = 0
            pc = ((sellPrice/buyPrice) - 1) * 100
            percentChangeRSI.append(pc)
    if(num == df["Adj Close"].count() - 1 and pos == 1): #checks if theres a transaction currently held at end of list
        sellPrice = close
        pos = 0
        pc = ((sellPrice/buyPrice) - 1) * 100
        percentChangeRSI.append(pc)
    num += 1 #adds on to the count of days handled

hu.summary_statistics(percentChangeRSI, "Short Term RSI", stock)


## SHORT TERM EMA STRATEGY ##

## Buy/sell at crossovers of exponential moving average of 5 and 10
emaList = [5, 10]

#adding nessesary data for emas into the data table for the stock
for ema in emaList:
    df["Ema_" + str(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(), 2)

pos = 0
num = 0
percentChange = []

for i in df.index:
    cmin = df["Ema_5"][i]
    cmax = df["Ema_10"][i]
    close = df["Adj Close"][i]
    if(cmin > cmax): #checks if crossover to buy has happened
        if(pos == 0):
            buyPrice = close
            pos = 1
    elif(cmin < cmax): #checks if crossover to sell has happened
        if(pos == 1):
            sellPrice = close
            pos = 0
            pc = ((sellPrice/buyPrice) - 1) * 100
            percentChange.append(pc)
    if(num == df["Adj Close"].count() - 1 and pos == 1): #checks if theres a transaction currently held at end of list
        sellPrice = close
        pos = 0
        pc = ((sellPrice/buyPrice) - 1) * 100
        percentChange.append(pc)
    num += 1 #adds on to the count of days handled

hu.summary_statistics(percentChange, "Short Term EMA", stock)