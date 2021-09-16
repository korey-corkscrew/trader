from brownie import *
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime

priceFile = 'price.csv'
tradeFile = 'trades.csv'

def main():
    trade = False
    while True:
        df = pd.read_csv((priceFile), index_col=3)
        df.columns = ['matic_reserve', 'usdc_reserve', 'last_tx_time', 'price']
        df['100 MA'] = df.price.rolling(window=100).mean()
        print("Price: " + str(df['price'].iloc[-1]))
        print("MA: " + str(df['100 MA'].iloc[-1]))
        print()
        
        if df['price'].iloc[-1] > df['100 MA'].iloc[-1] and not trade:
            print(datetime.datetime.now())
            print(" Buy MATIC @ " + str(df['price'].iloc[-1]))
            print()
            trade = True
            with open(tradeFile, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([datetime.datetime.now(), 'BUY', df['matic_reserve'].iloc[-1], df['usdc_reserve'].iloc[-1], df['price'].iloc[-1]])
        if df['price'].iloc[-1] < df['100 MA'].iloc[-1] and trade:
            print(datetime.datetime.now())
            print(" Sell MATIC @ " + str(df['price'].iloc[-1]))
            print()
            trade = False
            with open(tradeFile, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([datetime.datetime.now(), 'SELL', df['matic_reserve'].iloc[-1], df['usdc_reserve'].iloc[-1], df['price'].iloc[-1]])
        
        time.sleep(30)
