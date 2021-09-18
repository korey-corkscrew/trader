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
    if df['price'].iloc[i] > df['100 MA'].iloc[i]:# and df['price'].iloc[i] < df['200 MA'].iloc[i]:
        if df['price'].iloc[i-1] < df['100 MA'].iloc[i-1]:
            return True

def sellSignal(df, i):
    if i == 0:
        return False
    if df['price'].iloc[i] < df['100 MA'].iloc[i]:
        if df['price'].iloc[i-1] > df['100 MA'].iloc[i-1]:
            return True


def plot(df):
    #fig, ax = plt.subplots()
    #ax2 = ax.twinx()
    plt.figure(figsize=(12, 8))
    #plt.title('MATIC/USDC - Current Price - 100 MA')
    plt.plot(df.index, df[['100 MA', 'price']])
    plt.plot(df.index, df['buy'], '^', color='g')
    plt.plot(df.index, df['sell'], 'v', color='r')
    plt.xlabel('Trading Dates')
    plt.ylabel('Price (USDC)')
    #fig.xticks(df.index[::20], rotation='vertical')
    #fig.legend(('100 MA'), loc='lower right')
    plt.show()
    

def main():
    trade = []

    startAmt = int(1000 * 10**6)
    #startAmt = []
    maticAmt = []
    profit = 0

    tradeCount = 0

    for n in range(30):
        trade.append(False)
        #startAmt.append(startAmt)
        maticAmt.append(0)

    df = pd.read_csv((priceFile), index_col=3)
    df.columns = ['matic_reserve', 'usdc_reserve', 'last_tx_time', 'price']

    df = df[3440:]

    df['100 MA'] = df.price.rolling(window=100).mean()
    df['200 MA'] = df.price.rolling(window=150).mean()
    df['buy'] = None
    df['sell'] = None
    
    for i in range(len(df)):

        # Buy signal
        if buySignal(df, i):
            # Find first open trade
            for j, val in enumerate(trade):
                if not val:
                    trade[j] = True
                    tradeCount = tradeCount + 1
                    print(datetime.datetime.fromtimestamp(df.index[i]))
                    print("Buy MATIC @ " + str(df['price'].iloc[i]))
                    df['buy'].iloc[i] = df['price'].iloc[i]
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
                        tradeCount = tradeCount + 1
                        profit = profit + (amt - startAmt)
                        #startAmt[j] = amt
                        print(datetime.datetime.fromtimestamp(df.index[i]))
                        print("Sell MATIC @ " + str(df['price'].iloc[i]))
                        df['sell'].iloc[i] = df['price'].iloc[i]
                        print("Trade: " + str(j) + " --- " + str(maticAmt[j]*10**-18) + " MATIC --> " + str(amt*10**-6) + " USDC")
                        maticAmt[j] = 0
                        print("---------------------------------------------------\n\n")

    totalVal = 0
    numTrades = 0
    for n, val in enumerate(trade):
        if val:
            numTrades = numTrades + 1
            totalVal = totalVal + (getAmountOut(maticAmt[n], int(df['matic_reserve'].iloc[i]), int(df['usdc_reserve'].iloc[i])) * 10**-6)
            print("Trade: " + str(n) + " --- " + str(maticAmt[n]*10**-18) + " MATIC ($" + str(getAmountOut(maticAmt[n], int(df['matic_reserve'].iloc[i]), int(df['usdc_reserve'].iloc[i])) * 10**-6) + ")")

    print()
    print("Profit: " + str(profit * 10**-6))
    print(str(tradeCount) + " Trades")
    print("Current MATIC price: " + str((int(df['usdc_reserve'].iloc[i]) * 10**-6) / (int(df['matic_reserve'].iloc[i]) * 10**-18)))
    plot(df)
    