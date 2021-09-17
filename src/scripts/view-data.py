from brownie import *
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime

priceFile = 'price.csv'

def main():
    df = pd.read_csv((priceFile), index_col=3)
    df.columns = ['matic_reserve', 'usdc_reserve', 'last_tx_time', 'price']
    df['100 MA'] = df.price.rolling(window=100).mean()
    df['200 MA'] = df.price.rolling(window=200).mean()
    plt.figure(figsize=(12, 8))
    plt.title('MATIC/USDC - Current Price - 100 MA')
    plt.plot(df.index, df[['100 MA', '200 MA', 'price']])
    plt.xlabel('Trading Dates')
    plt.ylabel('Price (USDC)')
    plt.xticks(df.index[::20], rotation='vertical')
    plt.legend(('100 MA'), loc='lower right')
    plt.show()
