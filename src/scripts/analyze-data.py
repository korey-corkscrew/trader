from brownie import *
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime

priceFile = 'price.csv'
tradeFile = 'trades.csv'

def getAmountOut(amtIn, reserveIn, reserveOut):
    return reserveOut - ((reserveIn * reserveOut) / ((amtIn * .997) + reserveIn))

def main():
    trade = False
    buyPrice = 0
    usdcAmt = 1000 *10**6
    maticAmt = 0
    while True:
        df = pd.read_csv((priceFile), index_col=3)
        df.columns = ['matic_reserve', 'usdc_reserve', 'last_tx_time', 'price']
        df['100 MA'] = df.price.rolling(window=100).mean()
        u = int(df['usdc_reserve'].iloc[-1])
        m = int(df['matic_reserve'].iloc[-1])
        p = df['price'].iloc[-1]
        ma = df['100 MA'].iloc[-1]

        
        if p > ma and not trade:
            print(datetime.datetime.now())
            print("Buy MATIC @ " + str(p))
            #maticAmt = int(m - ((m * u) / ((usdcAmt * .997) + u)))
            maticAmt = getAmountOut(usdcAmt, u, m)
            print(str(usdcAmt*10**-6) + " USDC --> " + str(maticAmt*10**-18) + " MATIC")
            print()
            trade = True
            with open(tradeFile, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([datetime.datetime.now(), 'BUY', df['matic_reserve'].iloc[-1], df['usdc_reserve'].iloc[-1], df['price'].iloc[-1]])
        if df['price'].iloc[-1] < df['100 MA'].iloc[-1] and trade:
            amt = getAmountOut(maticAmt, m, u)
            if amt > usdcAmt:
                usdcAmt = amt
                print(datetime.datetime.now())
                print("Sell MATIC @ " + str(df['price'].iloc[-1]))
                print(str(maticAmt*10**-18) + " MATIC --> " + str(usdcAmt*10**-6) + " USDC")
                print()
                trade = False
                with open(tradeFile, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([datetime.datetime.now(), 'SELL', df['matic_reserve'].iloc[-1], df['usdc_reserve'].iloc[-1], df['price'].iloc[-1]])
            
        time.sleep(30)
