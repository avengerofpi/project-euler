#!/usr/bin/python3

# Imports
from math import log, log2, log10, prod, sqrt
from collections import defaultdict
import scipy
import numpy
from numpy import array
from datetime import timedelta
import time
#pip3 install primefac
from primefac import primefac
from colorama import Fore, Back, Style
from copy import deepcopy
#print(f"{Fore.GREEN}hello{Fore.RED}World{ansi.Style.RESET_ALL}")

# Tests
UNKNOWN = "UNKNOWN"
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
TestCase(2, 69),
# 8**12 * 12**8 = 2**52 * 3**8
# wrong: 817937001
# wrong: 5021107
# wrong: 779447732
# wrong: 80380684
# wrong: 335375497
# wrong: 617013410
# wrong: 527697869
TestCase(8**12 * 12**8, UNKNOWN),
]

# Constants
MOD = 10**9 + 7

# Logging
info = True
debug = False
verbose = False
timing = True
def logInfo(msg = ""):
    if info:
        print(msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print(msg, flush=True)
def logTiming(msg = ""):
    if timing:
        print(msg, flush=True)

def getTimeInMillis():
    return int(time.time() * 1000)

# Functions
def toBinaryList(x):
    ret = list(bin(x)[2:])
    logVerbose(f"toBinaryList({x}) = {ret}")
    return ret

def toReverseBinaryList(x):
    bList = toBinaryList(x)
    bList.reverse()
    logVerbose(f"toReverseBinaryList({x}) = {bList}")
    return bList

def xorProductUsingExpos(exposX, exposY):
    logDebug(f"Computing xorProductUsingExpos(x, y)")
    logDebug(f"  x = {exposX}")
    logDebug(f"  y = {exposY}")
    logDebug(f"XOR expo summands:")
    ret = set()
    for expoX in exposX:
        newExpos = { expoY + expoX for expoY in exposY }
        ret.symmetric_difference_update(newExpos)
        logDebug(f"Shift {expoX} -> {sorted(newExpos)} -> {sorted(ret)}")
        #for newExpo in newExpos: 
        #    if newExpo in ret:
        #        ret.remove(newExpo)
        #    else:
        #        ret.add(newExpo)
        #    logDebug(f"  {}")
    return sorted(ret)

def xorProduct(x, y):
    xRevBinList = toReverseBinaryList(x)
    yRevBinList = toReverseBinaryList(y)
    yBin = bin(y)[2:]
    logVerbose(f"xRevBinList = {xRevBinList}")
    logVerbose(f"yRevBinList = {yRevBinList}")
    xLen = len(xRevBinList)
    yLen = len(yRevBinList)
    logVerbose(f"xLen: {xLen}")
    logVerbose(f"yLen: {yLen}")
    width = xLen + yLen
    shiftList = [i for i in range(xLen) if xRevBinList[i] == '1']
    logVerbose(f"ShiftList: {shiftList}")
    ret = 0
    logDebug(f"Computing xorProduct({x}, {y})")
    logDebug(f"  x = {x} = {bin(x)}")
    logDebug(f"  y = {y} = {bin(y)}")
    logDebug(f"Using x to shift y")
    for shift in shiftList:
        summand = (y << shift)
        logDebug(f"  {bin(summand)[2:]:>{width}}")
        ret ^= summand
    logDebug(f"  {'-' * width}")
    logDebug(f"  {bin(ret)[2:]:>{width}}")
    return ret

def runXorPowers(n):
    logInfo(f"Computing runXorPower for n = {n}:")
    ret = 1
    for i in range(n):
        ret = xorProduct(11, ret)
    return ret

def runTests():
    for test in TESTS:
        startTime = getTimeInMillis()
        N = test.N
        expected = test.expected
        logInfo(f"Running against N = {N}")

        ansBeforeMod, period, periodStart = runXorPowers(N)
        logInfo(f"period(n = {N:7d}) = {period:7} (starts at {periodStart:7}) (final sum after {numIters} rounds: {ansBeforeMod}")
        ans = ansBeforeMod % MOD
        result = TestCase(N, numIters, ans, period, periodStart)
        printTestResult(test, result)

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()

def extractParts(N):
    k = 0
    q = N
    while (q % 2 == 0):
        k += 1
        q = q // 2
    if q == 1:
        q = 0
    return k, q

def troubleshoot(N):
    logInfo(f"Running troubleshoot(N = {N})")
    # 8**12 * 12**8 = 2**52 * 3**8
    #N = 8**12 * 12**8
    #N = 4
    k, remainingIters = extractParts(N)
    logInfo(f"k: {k}")
    logInfo(f"remainingIters: {remainingIters}")

    #k = 52
    #remainingIters = 3**8

    #k = 2
    #remainingIters = 1

    if k == 0 and N != 1:
        expo2s = [0]
    else:
        expo2s = [0, 1 << k, 3 * (1 << k)]
    # TOO BIG - MEMORY ERRORS !!
    #ret = sum(2 << i for i in expo2s)

    # reverse it?
    otherFactor = runXorPowers(remainingIters)
    otherFactorBin = bin(otherFactor)[2:]
    lenOtherFactorBin = len(otherFactorBin)
    expoOthers = [i for i in range(lenOtherFactorBin) if otherFactorBin[lenOtherFactorBin -1 - i] == '1']

    #expoOthers = [0]

    #logInfo(f"otherFactor: {otherFactor}")
    #logInfo(f"otherFactorBin: {otherFactorBin}")
    logInfo(f"expo2s {len(expo2s)}: {expo2s}")
    logInfo()
    logInfo(f"expoOthers {len(expoOthers)}: {expoOthers}")
    logInfo()
    ansExpos = xorProductUsingExpos(expo2s, expoOthers)
    logInfo(f"ansExpos {len(ansExpos)}: {ansExpos}")
    logInfo()
    if len(ansExpos) > 0:
        maxExpo = max(ansExpos)
        if maxExpo > 0:
            maxPower = int(log2(maxExpo))
        else:
            maxPower = 0
    else:
        maxPower = 0
    #exponentsToModValueMap = { 0: 1, 1: 2 }
    exponentsToModValueMap = { 0: 2, 1: 4 }
    power = 2
    #for i in range(2, maxPower+1):
    for i in range(1, maxPower+1):
        power = (power * power) % MOD
        #power = (2 * power) % MOD
        exponentsToModValueMap[i] = power
    
    logInfo(f"exponentsToModValueMap:")
    for k,v in sorted(exponentsToModValueMap.items()):
        logInfo(f"  {k:>2}: {v}")

    ret = 0
    for expo in ansExpos:
        logInfo(f"Handling expo {expo}")
        expoBin = bin(expo)[2:]
        logInfo(f"  -> bin: {expoBin}")
        lenExpoBin = len(expoBin)
        expoExpos = [i for i in range(lenExpoBin) if expoBin[lenExpoBin - 1 - i] == '1']
        logInfo(f"  -> set bit indices: {expoExpos}")
        summand = prod(exponentsToModValueMap[i] for i in expoExpos) % MOD
        logInfo(f"  -> increment summard: {summand}")
        ret = (ret + summand) % MOD
        logInfo(f"  -> current total: {ret}")

    #for i in range(remainingIters):
    #    #ret = xorProduct(11, ret)
    #    ret = xorProduct(ret, 11)
    logInfo(ret)
    logInfo(ret % MOD)
    logInfo(bin(ret % MOD))

    # Double check, for small N
    if N < 10 ** 3:
        ans = runXorPowers(N)
        logInfo(ans)
        logInfo(ans % MOD)
        logInfo(bin(ans % MOD))

# Main logic
def main():
    #for N in [8**12 * 12**8]:
    for N in [1, 2, 3, 4, 5, 6, 7, 8, 12]:
        troubleshoot(N)
        logInfo(f"{'-' * 50}")
    #8**12 * 12**8
    #runTests()

# Main logic
if __name__ == '__main__':
    main()
