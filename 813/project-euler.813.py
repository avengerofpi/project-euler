#!/usr/bin/python3

"""
Observe that xorPowers is commutative, associative, and the following:
  P(a + b) = P(a) (X) P(b)
  P(2**k) = 1 + 2**(2**k) + 2**(3 * 2**k)
For example,
  P(1) =       11 = 0b                     1011
  P(2) =       69 = 0b                  1000101
  P(4) =      743 = 0b            1000000010001
  P(8) = 16777473 = 0b1000000000000000100000001
In the following code, we focus on using exponents/set bits, rather than
full numbers, since we are working with numbers that are sparse / have low
popcount (number of set bits in base 2).

So we can compute, e.g.,
  P(81) = P(64 + 16 + 1) = P(64) (X) P(16) (X) P(1)
and we can do this efficiently with the exponents
"""

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
TestCase(81, 793162484),
TestCase(2**50 * 3**8, 955927129),
TestCase(2**50 * 3**9, 790653055),
TestCase(2**50 * 3**8 * 5, 45088448),
# addition between powers of two and other factor, rather than multiplication
TestCase(2**52 + 3**8, 527697869),
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
    """
    e.g., 23 -> 0b10111 -> ['1', '1', '1', '0', '1']
    """
    ret = list(bin(x)[2:])
    logVerbose(f"toBinaryList({x}) = {ret}")
    return ret

def toReverseBinaryList(x):
    """
    e.g., 23 -> 0b10111 -> ['1', '1', '1', '0', '1'] --(reverse)--> ['1', '0', '1', '1', '1']
    """
    bList = toBinaryList(x)
    bList.reverse()
    logVerbose(f"toReverseBinaryList({x}) = {bList}")
    return bList

def getSetBits(N):
    """
    e.g., 23 -> 0b10111 -> [0, 1, 2, 4]
    """
    binN = bin(N)[2:]
    lenBinN= len(binN)
    return [i for i in range(lenBinN) if binN[lenBinN -1 - i] == '1']

def xorProductUsingExpos(exposX, exposY):
    """
    Use symmetric differences between expo sets as analog to binary XOR.
    """
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

    xLen = len(xRevBinList)
    yLen = len(yRevBinList)

    width = xLen + yLen
    shiftList = [i for i in range(xLen) if xRevBinList[i] == '1']

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

def computeXorProductSetBitsFromInputSetBits(setBits):
    """
    Based on
        P(a + b) = P(a) (X) P(b)
        P(2**k) = 1 + 2**(2**k) + 2**(3 * 2**k)
    So, for example,
        P(81) = P(64 + 16 + 1) = P(64) (X) P(16) (X) P(1)
    The set bits are [0, 4, 6], leading to exponent index lists
        0 -> [0,  1,   3]
        4 -> [0, 16,  48]
        6 -> [0, 64, 192]
    """
    ansSetBits = [0]
    for k in setBits:
        xorProductSetBits = [0, 1 << k, 3 * (1 << k)]
        logDebug(f"xorProductSetBits for bit {k}: {xorProductSetBits}")
        ansSetBits = xorProductUsingExpos(ansSetBits, xorProductSetBits)
    logDebug(f"ansSetBits (length {len(ansSetBits)}): {ansSetBits}")
    logDebug()
    return ansSetBits

def computeExponentsToModValueMap(expos):
    """
    Values of 2**(2**k) mod (10**9 + 7)
    e.g.
        k: value
        0: 2
        1: 4
        2: 16
        3: 256
        ...
        10: 812734592
    """
    maxPower = 0
    if len(expos) > 0:
        maxExpo = max(expos)
        if maxExpo > 0:
            maxPower = int(log2(maxExpo))

    exponentsToModValueMap = { 0: 2 }
    power = 2
    for i in range(1, maxPower+1):
        power = (power * power) % MOD
        exponentsToModValueMap[i] = power

    logDebug(f"exponentsToModValueMap:")
    for k,v in sorted(exponentsToModValueMap.items()):
        logDebug(f"  {k:>2}: {v}")

    return exponentsToModValueMap

def computeModValueFromSetBits(ansSetBits):
    exponentsToModValueMap = computeExponentsToModValueMap(ansSetBits)
    ret = 0
    for expo in ansSetBits:
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
    return ret

def runXorPowersEfficiently(N):
    inputSetBits = getSetBits(N)
    ansSetBits = computeXorProductSetBitsFromInputSetBits(inputSetBits)
    return computeModValueFromSetBits(ansSetBits)

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
    ans = runXorPowersEfficiently(N)
    result = TestCase(N, ans)
    printTestResult(test, result)

    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")

    logInfo(f"{'-' * 60}")

def runTests():
    for test in TESTS:
        runTest(test)

def troubleshoot(N):
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
    #troubleshoot()
    #troubleshoot2()
    runTests()

# Main logic
if __name__ == '__main__':
    main()
