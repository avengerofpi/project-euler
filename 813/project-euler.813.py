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
TestCase(1, 11),
TestCase(2, 69),
TestCase(3, 743),
TestCase(4, 4113),
TestCase(5, 45243),
TestCase(6, 283669),
TestCase(7, 3038359),
TestCase(8, 16777473),
TestCase(12, 5737774),
TestCase(2**50 * 3**8, 955927129),
TestCase(2**50 * 3**9, 790653055),
TestCase(2**50 * 3**8 * 5, 45088448),
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

def runXorPowersBasic(N):
    logDebug(f"Computing runXorPower for N = {N}:")
    ret = 1
    for i in range(N):
        ret = xorProduct(11, ret)
    return ret

def runXorPowersEfficient(N):
    binN = bin(N)[2:]
    lenBinN= len(binN)
    setBitsN = [i for i in range(lenBinN) if binN[lenBinN -1 - i] == '1']

    ansExpos = [0]
    for k in setBitsN:
        expos = [0, 1 << k, 3 * (1 << k)]
        logDebug(f"Expos for bit {k}: {expos}")
        ansExpos = xorProductUsingExpos(ansExpos, expos)

    logDebug(f"ansExpos {len(ansExpos)}: {ansExpos}")
    logDebug()
    if len(ansExpos) > 0:
        maxExpo = max(ansExpos)
        if maxExpo > 0:
            maxPower = int(log2(maxExpo))
        else:
            maxPower = 0
    else:
        maxPower = 0

    exponentsToModValueMap = { 0: 2, 1: 4 }
    power = 2
    for i in range(1, maxPower+1):
        power = (power * power) % MOD
        exponentsToModValueMap[i] = power

    logDebug(f"exponentsToModValueMap:")
    for k,v in sorted(exponentsToModValueMap.items()):
        logDebug(f"  {k:>2}: {v}")

    ret = 0
    for expo in ansExpos:
        logDebug(f"Handling expo {expo}")
        expoBin = bin(expo)[2:]
        logDebug(f"  -> bin: {expoBin}")
        lenExpoBin = len(expoBin)
        expoExpos = [i for i in range(lenExpoBin) if expoBin[lenExpoBin - 1 - i] == '1']
        logDebug(f"  -> set bit indices: {expoExpos}")
        summand = prod(exponentsToModValueMap[i] for i in expoExpos) % MOD
        logDebug(f"  -> increment summard: {summand}")
        ret = (ret + summand) % MOD
        logDebug(f"  -> current total: {ret}")

    #logInfo(f"TestCase({N}, {ret}),")

    return ret

def printTestResult(tc, result):
    PATH_COLOR = Fore.RED
    RESET_COLOR = Style.RESET_ALL

    expected = tc.expected
    ans = result.expected
    if expected == UNKNOWN:
        successStr = UNKNOWN
        b = Back.YELLOW
        c = Fore.RED
    elif ans == expected:
        successStr = "SUCCESS"
        b = Back.GREEN
        c = Fore.RED
    else:
        successStr = f"FAILURE (expected {expected} but got {ans})"
        b = Back.RED
        c = Fore.YELLOW
    logInfo(f"{c}{b} Result for {tc.N}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")

def runTest(test):
    startTime = getTimeInMillis()

    N = test.N
    logInfo(f"Running against N = {N}")

    ans = runXorPowersEfficient(N)
    result = TestCase(N, ans)
    printTestResult(test, result)

    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")

    logInfo()

def runTests():
    for test in TESTS:
        runTest(test)

def troubleshoot(N):

    # Double check, for small N
    if N < 10 ** 3:
        ans = runXorPowers(N)
        logDebug(ans)
        logDebug(ans % MOD)
        logDebug(bin(ans % MOD))

def troubleshoot2():
    logInfo()

    ans = runXorPowers(81)
    logInfo(f"ans:  {ans}")

    b1 = runXorPowers(64)
    b2 = runXorPowers(16)
    b3 = runXorPowers(1)
    bAns = xorProduct(xorProduct(b1, b2), b3)
    logInfo(f"  b1: {bin(b1)}")
    logInfo(f"  b2: {bin(b2)}")
    logInfo(f"  b3: {bin(b3)}")
    logInfo(f"bAns: {bAns}")

# Main logic
def main():
    #troubleshoot2()
    #return

    #for N in [1, 2, 3, 4, 5, 6, 7, 8, 12, 8**12 * 12**8]:
    #    troubleshoot(N)
    #    logInfo(f"{'-' * 50}")
    #return

    runTests()

# Main logic
if __name__ == '__main__':
    main()
