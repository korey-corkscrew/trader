from brownie import *
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime

priceFile = 'price.csv'
tradeFile = 'trades.csv'

def getAmountOut(amtIn, reserveIn, reserveOut):
    return int(reserveOut - ((reserveIn * reserveOut) / ((amtIn * .997) + reserveIn)))

def buySignal(df, i):
    if i == 0:
        return False
    if df['price'].iloc[i] > df['100 MA'].iloc[i]:
        if df['price'].iloc[i-1] < df['100 MA'].iloc[i-1]:
            return True

def sellSignal(df, i):
    if i == 0:
        return False
    if df['price'].iloc[i] < df['100 MA'].iloc[i]:
        if df['price'].iloc[i-1] > df['100 MA'].iloc[i-1]:
            return True
    

def main():
    trade = []

    startAmt = int(1000 * 10**6)
    #startAmt = []
    maticAmt = []
    profit = 0

    for n in range(30):
        trade.append(False)
        #startAmt.append(startAmt)
        maticAmt.append(0)

    df = pd.read_csv((priceFile), index_col=3)
    df.columns = ['matic_reserve', 'usdc_reserve', 'last_tx_time', 'price']
    df['100 MA'] = df.price.rolling(window=100).mean()
    
    for i in range(len(df)):

        # Buy signal
        if buySignal(df, i):
            # Find first open trade
            for j, val in enumerate(trade):
                if not val:
                    trade[j] = True
                    print(datetime.datetime.fromtimestamp(df.index[i]))
                    print("Buy MATIC @ " + str(df['price'].iloc[i]))
                    maticAmt[j] = getAmountOut(startAmt, int(df['usdc_reserve'].iloc[i]), int(df['matic_reserve'].iloc[i]))
                    print("Trade: " + str(j) + " --- " + str(startAmt*10**-6) + " USDC --> " + str(maticAmt[j]*10**-18) + " MATIC")
                    print("---------------------------------------------------\n\n")
                    break


        if sellSignal(df, i):
            for j, val in enumerate(trade):
                #print(val)
                if val:
                    amt = getAmountOut(maticAmt[j], int(df['matic_reserve'].iloc[i]), int(df['usdc_reserve'].iloc[i]))
                    if amt > startAmt:
                        trade[j] = False
                        profit = profit + (amt - startAmt)
                        #startAmt[j] = amt
                        print(datetime.datetime.fromtimestamp(df.index[i]))
                        print("Sell MATIC @ " + str(df['price'].iloc[i]))
                        print("Trade: " + str(j) + " --- " + str(maticAmt[j]*10**-18) + " MATIC --> " + str(startAmt*10**-6) + " USDC")
                        maticAmt[j] = 0
                        print("---------------------------------------------------\n\n")

    totalVal = 0
    numTrades = 0
    for n, val in enumerate(trade):
        if val:
            numTrades = numTrades + 1
            totalVal = totalVal + (getAmountOut(maticAmt[n], int(df['matic_reserve'].iloc[i]), int(df['usdc_reserve'].iloc[i])) * 10**-6)
            print("Trade: " + str(n) + " --- " + str(maticAmt[n]*10**-18) + " MATIC ($" + str(getAmountOut(maticAmt[n], int(df['matic_reserve'].iloc[i]), int(df['usdc_reserve'].iloc[i])) * 10**-6) + ")")
        #elif not val and startAmt[n] > startAmt:
        #    numTrades = numTrades + 1
        #    print("Trade: " + str(n) + " --- " + str(startAmt[n]*10**-6) + " USDC")
        #    totalVal = totalVal + startAmt[n]*10**-6

    #profit = totalVal - (numTrades * startAmt * 10**-6)
    print()
    #print("Total Value: " + str(totalVal))
    print("Profit: " + str(profit * 10**-6))
    