#!/usr/bin/python3

# Imports
from math import log, log2, log10, prod, sqrt, gcd
from collections import defaultdict
import scipy
import numpy
from numpy import add, array
from datetime import timedelta
import time
#pip3 install primefac
from primefac import primefac
from colorama import Fore, Back, Style
from copy import deepcopy
#print(f"{Fore.GREEN}hello{Fore.RED}World{ansi.Style.RESET_ALL}")

"""
TODO:
    We don't care about the order of the numbers/factor lists, and much of the structure
    of the looping revolves just around the frequency distribution of the lengths of the
    factor lists. For example, we can take
        [[2,3,5], [2,2], [3], [5], [5,7,7,11]]
    to
        [3, 2, 1, 1, 4]
    where each number represents the length of the factor list it replaces, and
    then each round is just to, append a new number that is the length of the
    list input to the current round (5 in this example), subtract one from each
    of the numbers that was in the input list, and remove any such numbers that
    are now zero (0):
        [2, 1, 0, 0, 3, 5] -> [2, 1, 3, 5]
    We loose the abilty to compute the sum of the original entries, but it will be
    faster to find a period. A period of this reduced form must divide a period of
    the original form (proof?). We can further reduce this to just counting the
    frequency of each length, { length: frequency }
        {
            1: 2,
            2: 1,
            3: 1,
            4: 1,
        }
    Then the round is to subtract 1 from each of the keys, removing new key zero (0)
    if it exists, sum up the origal values (2 + 1 + 1 + 1 = 5), which is used as a key
    to insert into the map (or increment if the value already existed, after the first
    step):
        {
            1: 1,
            2: 1,
            3: 1,
            5: 1,
        },
        {
            1: 1,
            2: 1,
            4: 2,
        },
        {
            1: 1,
            3: 2,
            4: 1,
        },
        {
            2: 2,
            3: 1,
            4: 1,
        },
        {
            1: 2,
            2: 1,
            3: 1,
            4: 1,
        },
"""

# Tests
UNKNOWN = "UNKNOWN"
class TestCase:
    def __init__(self, N, numIters, expected,
            period      = UNKNOWN, periodStart      = UNKNOWN,
            shapePeriod = UNKNOWN, shapePeriodStart = UNKNOWN
    ):
        self.N = N
        self.numIters = numIters
        self.expected = expected
        self.period = period
        self.periodStart = periodStart
        self.shapePeriod = shapePeriod
        self.shapePeriodStart = shapePeriodStart

TESTS = [
TestCase(5, 3, 21, UNKNOWN, UNKNOWN, UNKNOWN),
TestCase(5, 10, 19, 3, 4, UNKNOWN),
TestCase(10, 100, 257, 60, 16, UNKNOWN),
TestCase(10, 101, 175, 60, 16, UNKNOWN),
TestCase(10, 1000, 257, 60, 16, UNKNOWN),
TestCase(10, 1001, 175, 60, 16, UNKNOWN),
TestCase(100, 1000, 989136573, 232792560, 400, 22, UNKNOWN),
#TestCase(100, 10**3, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN), # test for UNKNOWN warning
#TestCase(100, 10**3, 1, UNKNOWN, UNKNOWN, UNKNOWN), # test for error
TestCase(100, 10**6, 360990789, 232792560, 400, 22, UNKNOWN),
TestCase(1000, 10000, 204600045, 410555180440430163438262940577600, 4840, 76, UNKNOWN),
TestCase(1000, 100000, 803889757, 410555180440430163438262940577600, 4840, 76, UNKNOWN),
TestCase(3000, 10**16, 1013079068, 1749342047920660916901891145781670987072592322134428432000, 16470, 135, UNKNOWN),
TestCase(6000, 10**16, 132286426, 8603769834781171457272804805623074954273764323780252384481978979089202817658786064000, 33511, 194, UNKNOWN),
TestCase(10**4, 10**16, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN),
# require too much memory atm
#TestCase(1000, 1000000, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN),
#TestCase(a, b, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN),
]
"""
#TestCase(3, 100000000, 5, 2, 1),
#TestCase(4, 100000000, 14, 3, 1),
#TestCase(5, 100000000, 19, 3, 4),
#TestCase(6, 100000000, 22, 12, 8),
#TestCase(7, 100000000, 58, 12, 8),
#TestCase(8, 100000000, 67, 20, 15),
#TestCase(9, 100000000, 127, 20, 11),
#TestCase(10, 100000000, 257, 20, 9),
#TestCase(11, 100000000, 268, 60, 9),
#TestCase(12, 100000000, 250, 6, 24),
#TestCase(13, 100000000, 394, 6, 25),
#TestCase(14, 100000000, 841, 210, 18),
#TestCase(15, 100000000, 2113, 210, 18),
#TestCase(16, 100000000, 1594, 7, 30),
#TestCase(17, 100000000, 5434, 56, 30),
#TestCase(18, 100000000, 5780, 168, 31),
#TestCase(19, 100000000, 6050, 168, 31),
#TestCase(20, 100000000, 3940, 168, 19),
#TestCase(21, 100000000, 9466, 504, 59),
#TestCase(22, 100000000, 6034, 72, 51),
#TestCase(23, 100000000, 6958, 72, 51),
#TestCase(24, 100000000, 12949, 504, 73),
#TestCase(25, 100000000, 22105, 2520, 46),
#TestCase(26, 100000000, 26037, 2520, 45),
#TestCase(27, 100000000, 79697, 630, 77),
#TestCase(28, 100000000, 32130, 630, 92),
#TestCase(29, 100000000, 41790, 6930, 92),
#TestCase(30, 100000000, 192177, 6930, 87),
#TestCase(31, 100000000, 228177, 6930, 87),
#TestCase(32, 100000000, 139719, 440, 89),
#TestCase(33, 100000000, 110687, 1320, 113),
#TestCase(34, 100000000, 118341, 1320, 53),
#TestCase(35, 100000000, 310381, 1320, 71),
#TestCase(36, 100000000, 451837, 1320, 54),
#TestCase(37, 100000000, 1032445, 1320, 75),
#TestCase(38, 100000000, 634674, 1320, 127),
#TestCase(39, 100000000, 507422, 17160, 128),
#TestCase(40, 100000000, 326296, 5148, 131),
#TestCase(41, 100000000, 419896, 5148, 132),
#TestCase(42, 100000000, 1624326, 5148, 120),
#TestCase(43, 100000000, 3398406, 5148, 124),
#TestCase(44, 100000000, 9070145, 36036, 152),
#TestCase(45, 100000000, 64301021, 36036, 153),
#TestCase(46, 100000000, 37401802, 36036, 101),
#TestCase(47, 100000000, 37405344, 36036, 101),
#TestCase(48, 100000000, 10245357, 5460, 157),
#TestCase(49, 100000000, 9675349, 5460, 179),
#TestCase(50, 100000000, 6047747, 5460, 180),
#TestCase(51, 100000000, 7252885, 5460, 180),
#TestCase(52, 100000000, 14454957, 5460, 180),
#TestCase(53, 100000000, 30928557, 5460, 180),
#TestCase(54, 100000000, 92400668, 5460, 176),
#TestCase(55, 100000000, 69547142, 5460, 208),
#TestCase(56, 100000000, 14464776, 21840, 208),
#TestCase(57, 100000000, 10603214, 21840, 208),
#TestCase(58, 100000000, 15507348, 21840, 208),
#TestCase(59, 100000000, 25446228, 21840, 208),
#TestCase(60, 100000000, 58414230, 240240, 192),
#TestCase(61, 100000000, 148270230, 240240, 192),
#TestCase(62, 100000000, 223986518, 240240, 225),
]
"""

# Constants
MOD = 1234567891
CLEARED = "cleared"

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
def logList(currList, iterNum, logger = logDebug):
    width = 5
    logger(f"  {iterNum:{width}d}:")
    for e in currList:
        logger(f" {' ' * width} {e}")

def transformFactoredListIntoProductList(currList):
    return [prod(e) for e in currList]

def transformRange(n):
    return list(list(primefac(i)) for i in range(2,n+1))

def nextList(currList):
    nextE = []
    nextList = []
    for e in currList:
        p = e[0]
        nextE.append(p)
        if len(e) > 1:
            e = e[1:]
            nextList.append(e)
    nextE.sort()
    nextList.append(nextE)
    return nextList

def logValueMap(valueMap, logger = logVerbose):
    #logger(f"IndexToValueMap:")
    for i in sorted(valueMap.keys()):
        v = valueMap[i]
        logger(f"  {i}: {v}")
        #logger(f"  {i:5}: {v:5}")

def printTestResult(tc, result):
    PATH_COLOR = Fore.RED
    RESET_COLOR = Style.RESET_ALL

    expected = tc.expected
    numIters = tc.numIters
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
    logInfo(f"{c}{b} Result for {tc.N} after {numIters} rounds: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10} (period len {tc.period:7} starting at {tc.periodStart})")
    logInfo(f"  Actual:   {result.expected:10} (period len {result.period:7} starting at {result.periodStart})")

def toDenatured(inputList):
    """
    Transform input list to symbols. E.g.,
        [ [2], [3], [2, 2], [5], [2, 3], [7], [2, 2, 2] ]
    transforms into
        [ [0], [1], [2, 3], [4], [5, 6], [7], [8, 9, 10] ]
    and
        {
            0:2,            # 2
            1:3,            # 3
            2:2, 3:2,       # 4
            4:5,            # 5
            5:2, 6:3,       # 6
            7:7,            # 7
            8:2, 9:2, 10:2  # 8
        }
    """
    logger = logDebug
    symbolToValueMap = {}
    valueToIndexListMap = defaultdict(list)
    logger(f"toDenatured input:")
    logList(inputList, -1, logger = logger)
    for i in range(len(inputList)):
        eIn = inputList[i]
        for j in range(len(eIn)):
            v = eIn[j]
            valueToIndexListMap[v].append([i,j])
    symbol = 0
    outputList = deepcopy(inputList)
    values = sorted(valueToIndexListMap.keys())
    for v in values:
        # should already be in sorted order, by construction
        indexList = valueToIndexListMap[v]
        for [i,j] in indexList:
            outputList[i][j] = symbol
            symbolToValueMap[symbol] = inputList[i][j]
            symbol += 1
    logger(f"valueToIndexListMap")
    logValueMap(valueToIndexListMap, logger)
    logger(f"symbolToValueMap")
    logValueMap(symbolToValueMap, logger)
    logger(f"toDenatured output:")
    logList(outputList, -1, logger)
    return outputList, symbolToValueMap

def getShapeFromTuple(t):
    return tuple(len(e) for e in t)

def computePerm(prevTuple, currTuple, symbolsIn):
    """
        Return perm in three forms:
            perm: dict(key -> value)
                { 1: 3, 2: 7, ... }
            factored: 
                (
                    (1, 3, ...),
                    (2, 7, ...),
                    (4, ...),
                    ...
                )
            indexedFactors:
                {
                    1: (1, 3, ...),
                    2: (2, 7, ...),
                    3: (3, ..., 1),
                    4: (4, ...),
                    ...
                }
    """
    logDebug(f"    Checking perm for:")
    logDebug(f"      prevTuple: {prevTuple}")
    logDebug(f"      currTuple: {currTuple}")
    symbols = set(symbolsIn)
    perm = dict()
    for j in range(len(prevTuple)):
        for k in range(len(prevTuple[j])):
            perm[prevTuple[j][k]] = currTuple[j][k]

    logVerbose(f"Permutation:")
    logVerbose(f"  Base permutation:")
    for s in sorted(symbols):
        logVerbose(f"  {s:2}: {perm[s]:2}")

    permFactored = list()
    logDebug(f"    Factored permutation:")
    while len(symbols):
        a = min(symbols)
        symbols.remove(a)
        factor = [a]
        b = perm[a]
        while b != a:
            factor.append(b)
            symbols.remove(b)
            b = perm[b]
        factor = tuple(factor)
        logDebug(f"      {factor}")
        permFactored.append(factor)
    permFactored = tuple(permFactored)
    logDebug(f"    -> {permFactored}")
    return perm, permFactored

def transformPermToIndexedFactors(perm):
    logDebug(f"    Indexed factored permutation")
    indexedFactors = dict()
    symbols = perm.keys()
    for a in symbols:
        factor = [a]
        b = perm[a]
        while b != a:
            factor.append(b)
            b = perm[b]
        indexedFactors[a] = factor
        logDebug(f"      {a:2}: {factor}")

    return indexedFactors

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmArray(arr):
    if len(arr) < 2:
        raise Exception(f"lcm requires an array of at least two numbers, but got {arr}")
    ret = 1
    for e in arr:
        ret = lcm(ret, e)#ret * e // gcd(ret, e)
    return ret

def runFactorShuffle(n, numIters):
    logInfo(f"Running {numIters} rounds for n = {n}:")
    origList = transformRange(n)
    logger = logDebug
    logList(origList, 0, logger)
    # The first list will not be seen again, so don't bother adding it
    # This way we can use index 0 as a flag for unseen tuples.
    """List of tuples previously seen. May get trimmed for memory sake."""
    prevTupleList = [()]
    """Map from shape-tuples to lists of indices for tuples with that shape."""
    shapeToIndicesMap = defaultdict(list)
    """Map from indices to permutation from that index to the next index with the same shape."""
    indexToPermMap = defaultdict(tuple)
    period = UNKNOWN
    periodStart = UNKNOWN

    currList, symbolToValueMap = toDenatured(origList)
    symbols = set(symbolToValueMap.keys())
    logList(currList, 0, logger)
    for currIndex in range(1, numIters+1):
        currList = nextList(currList)
        logList(currList, currIndex, logger)

        currTuple = tuple(tuple(e) for e in currList)
        currShape = getShapeFromTuple(currTuple)

        prevTupleList.append(currTuple)

        if currIndex % (10 ** 5) == 0:
            logDebug(f"At step {currIndex}")

        prevIndices = shapeToIndicesMap[currShape]
        if len(prevIndices) > 0:
            # compute and store new perm
            if debug:
                logDebug(f"    prevIndices: {prevIndices}")
                logDebug(f"    prevTuples:")
                for prevI in prevIndices:
                    prevT = prevTupleList[prevI]
                    logDebug(f"      {prevI:2}: {prevT}")
                logDebug(f"    prevPerms:")
                for prevI in prevIndices[:-1]:
                    # logDebug(f"  prevI: {prevI}")
                    _, prevP, _ = indexToPermMap[prevI]
                    logDebug(f"      {prevI:2}: {prevP}")

            prevIndex = prevIndices[-1]
            prevTuple = prevTupleList[prevIndex]
            perm, permFactored = computePerm(prevTuple, currTuple, symbols)
            indexToPermMap[prevIndex] = permFactored

        permA = 0
        permB = 1
        if len(prevIndices) > 1:
            prevIndexA = prevIndices[-2]
            prevIndexB = prevIndices[-1]
            permA = indexToPermMap[prevIndexA]
            permB = indexToPermMap[prevIndexB]

        if permA == permB:
            logDebug(f"Found two identical perms: {permA}")
            periodStart = prevIndexA
            # extract permutation going from prevIndex to i = currIndex
            shapePeriod = prevIndexB - prevIndexA
            # permPeriod = int(numpy.lcm.reduce([len(factor) for factor in permFactored]))
            permPeriod = lcmArray([len(factor) for factor in permFactored])
            period = permPeriod * shapePeriod

            remainingIters = numIters - currIndex
            loopsToSkip = remainingIters // period
            itersAfterLooping = remainingIters % period
            shortCircuitIndex = currIndex + itersAfterLooping

            # extend list, if needed
            additionalSteps = shortCircuitIndex - currIndex
            if additionalSteps > 0:
                # additionalSteps = shortCircuitIndex - currIndex
                shapeLoops = additionalSteps // shapePeriod
                additionalSubSteps = additionalSteps % shapePeriod
                logInfo(f"Need to perform {additionalSteps} more steps")
                logInfo(f"  {shapeLoops:4} shape periods")
                indexedFactors = transformPermToIndexedFactors(perm)
                finalList = []
                for e in currList:
                    newE = []
                    for v in e:
                        factor = indexedFactors[v]
                        lenFactor = len(factor)
                        newV = factor[shapeLoops % lenFactor]
                        newE.append(newV)
                    finalList.append(newE)
                logInfo(f"  After shape periods:")
                logDebug(f"  {currIndex + shapeLoops*shapePeriod:2}: {finalList}")
                # logList(finalList, currIndex + shapeLoops*shapePeriod, logInfo)
                logInfo(f"  {additionalSubSteps:4} steps after shape periods")
                for ii in range(1, additionalSubSteps+1):
                    finalList = nextList(finalList)
                    logDebug(f"  {currIndex + shapeLoops*shapePeriod + ii:2}: {finalList}")
                    # logList(finalList, currIndex + shapeLoops*shapePeriod + 11, logInfo)
            else:
                finalList = prevTupleList[shortCircuitIndex]

            finalListOrigValues = [[symbolToValueMap[e] for e in ee] for ee in finalList]

            logInfo(f"---------- THIS ENTRY HAS BEEN SEEN BEFORE ----------")
            logInfo(f"  n                  {n}")
            logInfo(f"  numIters           {numIters}")
            logInfo(f"  " + "-" * 50)
            logInfo(f"  currIndex          {currIndex}")
            logInfo(f"  periodStart        {periodStart}")
            logInfo(f"  shapePeriod        {shapePeriod}")
            logInfo(f"  currShape:         {currShape}")
            logInfo(f"  permPeriod         {permPeriod}")
            logInfo(f"  period             {period} = {shapePeriod} * {permPeriod}")
            logInfo(f"  remainingIters     {remainingIters}")
            logInfo(f"  loopsToSkip:       {loopsToSkip}")
            logInfo(f"  itersAfterLooping: {itersAfterLooping}")
            logInfo(f"  shortCircuitIndex: {shortCircuitIndex}")
            logInfo(f"  " + "-" * 50)
            logInfo(f"  finalList:           {finalList}")
            logInfo(f"  finalListOrigValues: {finalListOrigValues}")
            logInfo(f"-----------------------------------------------------")

            currList = finalList
            break
        else:
            shapeToIndicesMap[currShape].append(currIndex)
            
        # only track the last two indices/perms/etc
        indicesToTrim = shapeToIndicesMap[currShape][0:-2]
        indicesToKeep = shapeToIndicesMap[currShape][-2:]
        logInfo(f"currIndex: {currIndex} - trimming indices {indicesToTrim} - keep indices {indicesToKeep}")
        for ii in indicesToTrim:
            indexToPermMap.pop(ii)
        shapeToIndicesMap[currShape] = indicesToKeep
        # 
        minIndexToKeep = min([0] + indicesToKeep)
        for ii in range(minIndexToKeep):
            prevTuple[ii] = CLEARED
            
    finalValueList = [[symbolToValueMap[i] for i in e] for e in currList]

    logVerbose(f"Final symbol list:")
    logList(currList, numIters, logVerbose)
    logVerbose(f"Final value list:")
    logList(finalValueList, numIters, logVerbose)

    prodList = transformFactoredListIntoProductList(finalValueList)
    finalSum = sum(prodList)
    logInfo(f"S({n}, {numIters}) -> {prodList} -> {finalSum}")

    return finalSum, period, periodStart

def runTests():
    for test in TESTS:
        startTime = getTimeInMillis()
        N = test.N
        numIters = test.numIters
        expected = test.expected
        logInfo(f"Running against N = {N}")

        ansBeforeMod, period, periodStart = runFactorShuffle(N, numIters)
        logInfo(f"period(n = {N:7d}) = {period:7} (starts at {periodStart:7}) (final sum after {numIters} rounds: {ansBeforeMod}")
        ans = ansBeforeMod % MOD
        result = TestCase(N, numIters, ans, period, periodStart)
        printTestResult(test, result)

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()
        logInfo()
        logInfo()

def troubleshoot():
    #for n in [16]:
    for n in range(3, 100):
        numIters = 10 ** 8
        finalSum, period, periodStart = runFactorShuffle(n, numIters)
        logInfo(f"period(n = {n:7d}) = {period:7d} (starts at {periodStart:7}) (final sum after {numIters} rounds: {finalSum}")
        ans = finalSum % MOD
        logInfo(f"TestCase({n}, {numIters}, {ans}, {period}, {periodStart}),")

# Main logic
def main():
    #troubleshoot()
    runTests()

# Main logic
if __name__ == '__main__':
    main()
