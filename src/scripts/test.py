from brownie import *

def main():
    r0 = 11913891917915405588896
    r1 = 460901921304310582983
    amtIn = 1000000000000000000

    #amtOut = r1 - ((r1 * r0) / ((amtIn*.997) + r0))
    for i in range(10):
        amountInWithFee = amtIn * i * 997
        numerator = amountInWithFee * r1
        denominator = (r0 * 1000) + amountInWithFee
        amtOut = int(numerator / denominator)
        diff = amtOut - (amtIn * i)
        print(diff)
        print()