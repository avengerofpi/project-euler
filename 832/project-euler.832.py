#!/usr/bin/python3

# Imports
from math import log, log2, log10

# Constants
N = 1000
wN = int(log10(N)) + 1
wn     = int(log10(3*N)) + 1
wnBits = 2 * (int(log(3*N, 4)) + 1)
wTupleSumDigits = int(log10(9*N)) + 1
wTupleSumBits = wnBits + 2
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

    sep = " - "
    formatIndex = f"{i:{wN}}: "
    formatTupleDigits = f"{a:{wn}} {b:{wn}} {ab:{wn}}"
    formatTupleBits   = f"{a:0{wnBits}b} {b:0{wnBits}b} {ab:0{wnBits}b}"
    formatSumDigits = f"{sum(newTuple):{wTupleSumDigits}}"
    formatSumBits   = f"{sum(newTuple):0{wTupleSumBits}b}"

    formatIndexAndTupleDigits = f"{formatIndex}{formatTupleDigits}"
    formatIndexAndTupleBits   = f"{formatIndex}{formatTupleBits}"
    formatSumDigitsAndBits = f"{formatSumDigits}{sep}{formatSumBits}"

    formatDigits = f"{formatTupleDigits}{sep}{formatSumDigits}"
    #formatBits   = f"{formatIndexAndTupleBits}{sep}{formatSumBits}"
    formatBits   = f"{formatTupleBits}{sep}{formatSumBits}"
    formatDigitsAndBits = f"{formatIndex}{formatDigits}{sep}{formatBits}{sep}{formatSumDigitsAndBits}"

    print(formatDigitsAndBits)

def logDebug(msg):
    if debug:
        print(msg)

def main():
    logFormatDetails()

    used = set()
    usedTuples = list()
    a = 1

    for i in range(1, N+1):
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

        newTuple = (a, b, ab)
        usedTuples.append(newTuple)

        #logLineSummary(i, a, b, ab)
        logLineSummaryWithFstring(i, a, b, ab)
        #f = f"{formatDigitsAndBits}"
        #ogDebug(f"{f'{ {f"{f}"} }'}""")
        #logDebug(f"{f'{formatDigitsAndBits}'}")
    print(sum(used))

# Main logic
if __name__ == '__main__':
    main()
