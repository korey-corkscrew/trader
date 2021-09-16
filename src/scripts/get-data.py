from brownie import *
import csv
import time


priceFile = 'price.csv'

def getPrice(pair):
    reserve = [0, 0]
    with open(priceFile, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        reserves = list(interface.IUniswapV2Pair(pair).getReserves())
        reserve[0] = reserves[0] * 10**-18
        reserve[1] = reserves[1] * 10**-6
        reserves.append(int(time.time()))
        reserves.append(getAmountOut(reserve[0], reserve[1], 1000))
        #reserves.append(reserves[1]/reserves[0])
        csvwriter.writerow(reserves)
    
def getAmountOut(reserveIn, reserveOut, amountIn):
    return (reserveOut - ((reserveIn * reserveOut)/((amountIn * 0.997) + reserveIn)))/amountIn

def main():
    while True:
        getPrice('0x6e7a5fafcec6bb1e78bae2a1f0b612012bf14827') # WMATIC/USDC
        time.sleep(30)