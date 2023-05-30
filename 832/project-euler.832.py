#!/usr/bin/python3

# Imports
from math import log, log2, log10

# Constants
N = 2000
wN = int(log10(N)) + 1
wn     = int(log10(3*N)) + 1
wnBits = 2 * (int(log(3*N, 4)) + 1)
esimatedMaxTupeSum = 16*N
wTupleSumDigits = int(log10(esimatedMaxTupeSum )) + 1
wTupleSumBits = wnBits + 3
debug = True

# Functions
def logFormatDetails():
    print(f"width of indices:     {wN} digits")
    print(f"width of a,b,ab:      {wn} digits")
    print(f"width of a,b,ab:      {wnBits} bits")
    print(f"width of sum(a,b,ab): {wTupleSumDigits} digits")
    print(f"width of sum(a,b,ab): {wTupleSumBits} bits")

def logLineSummaryWithFstring(i, a, b, ab):
    newTuple = (a, b, ab)
    sumNewTuple = sum(newTuple)

    sep = " "
    formatIndex = f"{i:{wN}}"
    formatTupleDigits = f"{a:{wn}} {b:{wn}} {ab:{wn}}"
    formatTupleBits   = f"{a:0{wnBits}b} {b:0{wnBits}b} {ab:0{wnBits}b}"
    formatSumDigits = f"{sum(newTuple):{wTupleSumDigits}}"
    formatSumBits   = f"{sum(newTuple):0{wTupleSumBits}b}"

    #formatIndexAndTupleDigits = f"{formatIndex}{formatTupleDigits}"
    #formatIndexAndTupleBits   = f"{formatIndex}{formatTupleBits}"
    formatSumDigitsAndBits = f"{formatSumDigits}{sep}{formatSumBits}"

    formatDigits = f"{formatTupleDigits}{sep}{formatSumDigits}"
    formatBits   = f"{formatTupleBits}{sep}{formatSumBits}"
    formatDigitsAndBits = f"{formatIndex}{sep}{formatSumDigitsAndBits}"
    #formatDigitsAndBitsWithRatio = f"{formatIndex}{sep}{formatSumDigitsAndBits} {sumNewTuple / i:5.2f} {(int(sumNewTuple / i) + 1) * '*'}"

    print(formatDigitsAndBits)
    #print(f"{formatIndex}{sep}{formatSumDigits}{sep}{formatSumBits}{sep}{sumNewTuple // 6}")
    #print(f"{sumNewTuple}")

def logDebug(msg):
    if debug:
        print(msg)

def generateListOfSums(numIters = N):
    used = set()
    #usedTuples = list()
    sums = []
    a = 1

    for i in range(1, numIters+1):
        while a in used:
            a += 1
        used.add(a)

        b = a + 1
        ab = a ^ b
        while ((b in used) or (ab in used)):
            b += 1
            ab = a ^ b

        used.add(b)
        used.add(ab)

        sums.append(a + b + ab)

        #newTuple = (a, b, ab)
        #sumTuple = sum(newTuple)
        #usedTuples.append(newTuple)

        #logLineSummary(i, a, b, ab)
        #logLineSummaryWithFstring(i, a, b, ab)
        #f = f"{formatDigitsAndBits}"
        #ogDebug(f"{f'{ {f"{f}"} }'}""")
        #logDebug(f"{f'{formatDigitsAndBits}'}")
    return sums

def simulateListofSums(numIters = N):
    powerOf4 = 1
    initForPowerOf4set = 6
    sums = []
    s = 6
    sums.append(s)
    i = 1
    while len(sums) < numIters:
        sums.append(nextPowerOf4set(s
        if ((3 * (i - 1)) == ((4 ** powerOf4) - 1)):
            # Start next power of 4 set

def genPowerOf4list(setNum):
    sums = []
    if setNum == 1:
        return [6]
    start = 6 * (4 ** (setNum - 1))
    lenOfList = 4 ** (setNum - 1)
    addOuter = 24
    addInner = 6
    while len(sum) < lenOfList:
        nn = next4(start)
    #for i in range(lenOfList):


def next4(n):
    return [n] + 3 * [n + 6]

def main():
    #logFormatDetails()

    sums = generateListOfSums(1000)
    print(f"M({N}) = {sum(sums)}")
    for s in sums:
        print(s)

# Main logic
if __name__ == '__main__':
    main()
