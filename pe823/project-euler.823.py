#!/usr/bin/env python3

# Imports
from math import log, log2, log10, prod, sqrt, gcd
from collections import defaultdict
import scipy
import numpy
from numpy import add, array
from datetime import timedelta
import time
from primefac import primefac
from colorama import Fore, Back, Style
from copy import deepcopy

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

class TestCaseCollections:
    def __init__(self):
        self.BASE = [
            TestCase(5, 3, 21, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN),
            TestCase(5, 10, 19, 6, 4, 3, UNKNOWN),
            TestCase(10, 101, 175, 60, 9, 1, UNKNOWN),
            TestCase(10, 1000, 257, 60, 9, 1, UNKNOWN),
            TestCase(10, 1001, 175, 60, 9, 1, UNKNOWN),
            TestCase(100, 10**6, 360990789, 232792560, 400, 22, UNKNOWN),
            TestCase(1000, 100000, 803889757, 410555180440430163438262940577600, 4840, 76, UNKNOWN)
        ]
        self.FIRST_100 = [
            TestCase(3, 100000000, 5, 2, 1, 2, 1),
            TestCase(4, 100000000, 14, 6, 1, 3, 1),
            TestCase(5, 100000000, 19, 6, 4, 3, 4),
            TestCase(6, 100000000, 22, 12, 9, 4, 5),
            TestCase(7, 100000000, 58, 12, 9, 2, 5),
            TestCase(8, 100000000, 67, 60, 17, 5, 7),
            TestCase(9, 100000000, 127, 60, 17, 5, 7),
            TestCase(10, 100000000, 257, 60, 9, 1, 9),
            TestCase(11, 100000000, 268, 60, 21, 6, 9),
            TestCase(12, 100000000, 250, 60, 29, 6, 11),
            TestCase(13, 100000000, 394, 60, 25, 6, 19),
            TestCase(14, 100000000, 841, 420, 20, 7, 13),
            TestCase(15, 100000000, 2113, 420, 20, 7, 13),
            TestCase(16, 100000000, 1594, 420, 30, 1, 30),
            TestCase(17, 100000000, 5434, 840, 32, 8, 16),
            TestCase(18, 100000000, 5780, 840, 32, 8, 16),
            TestCase(19, 100000000, 6050, 840, 34, 8, 18),
            TestCase(20, 100000000, 3940, 840, 19, 1, 19),
            TestCase(21, 100000000, 9466, 2520, 64, 9, 19),
            TestCase(22, 100000000, 6034, 2520, 66, 9, 21),
            TestCase(23, 100000000, 6958, 2520, 67, 9, 22),
            TestCase(24, 100000000, 12949, 2520, 73, 1, 73),
            TestCase(25, 100000000, 22105, 2520, 56, 10, 46),
            TestCase(26, 100000000, 26037, 2520, 48, 10, 28),
            TestCase(27, 100000000, 79697, 2520, 77, 10, 37),
            TestCase(28, 100000000, 32130, 2520, 92, 1, 92),
            TestCase(29, 100000000, 41790, 27720, 94, 11, 72),
            TestCase(30, 100000000, 166449, 27720, 62, 11, 29),
            TestCase(31, 100000000, 202449, 27720, 63, 11, 30),
            TestCase(32, 100000000, 139719, 27720, 100, 11, 89),
            TestCase(33, 100000000, 110691, 27720, 80, 12, 80),
            TestCase(34, 100000000, 118341, 27720, 84, 12, 36),
            TestCase(35, 100000000, 310381, 27720, 82, 12, 34),
            TestCase(36, 100000000, 451837, 27720, 71, 12, 35),
            TestCase(37, 100000000, 1032445, 27720, 75, 12, 75),
            TestCase(38, 100000000, 634674, 27720, 127, 1, 127),
            TestCase(39, 100000000, 507422, 360360, 129, 13, 103),
            TestCase(40, 100000000, 326548, 360360, 91, 13, 39),
            TestCase(41, 100000000, 420148, 360360, 93, 13, 54),
            TestCase(42, 100000000, 1624326, 360360, 136, 13, 110),
            TestCase(43, 100000000, 3398406, 360360, 137, 13, 124),
            TestCase(44, 100000000, 9070145, 360360, 153, 14, 139),
            TestCase(45, 100000000, 64301021, 360360, 156, 14, 100),
            TestCase(46, 100000000, 37401802, 360360, 116, 14, 74),
            TestCase(47, 100000000, 37405344, 360360, 116, 14, 74),
            TestCase(48, 100000000, 10245357, 360360, 163, 14, 149),
            TestCase(49, 100000000, 9675349, 360360, 179, 1, 179),
            TestCase(50, 100000000, 6047747, 360360, 182, 15, 137),
            TestCase(51, 100000000, 7252885, 360360, 184, 15, 109),
            TestCase(52, 100000000, 14454957, 360360, 186, 15, 96),
            TestCase(53, 100000000, 30928557, 360360, 187, 15, 112),
            TestCase(54, 100000000, 92400668, 360360, 191, 15, 176),
            TestCase(55, 100000000, 69547142, 360360, 208, 1, 208),
            TestCase(56, 100000000, 14298692, 11531520, 181, 16, 133),
            TestCase(57, 100000000, 10603214, 720720, 216, 16, 88),
            TestCase(58, 100000000, 20597678, 11531520, 185, 16, 57),
            TestCase(59, 100000000, 31705838, 11531520, 186, 16, 58),
            TestCase(60, 100000000, 83930382, 11531520, 189, 16, 157),
            TestCase(61, 100000000, 215258382, 11531520, 190, 16, 174),
            TestCase(62, 100000000, 223986518, 720720, 225, 1, 225),
            TestCase(63, 100000000, 162046732, 12252240, 231, 17, 129),
            TestCase(64, 100000000, 135671456, 104144040, 216, 17, 63),
            TestCase(65, 100000000, 438327890, 104144040, 217, 17, 64),
            TestCase(66, 100000000, 474948670, 104144040, 220, 17, 101),
            TestCase(67, 100000000, 474949792, 104144040, 221, 17, 119),
            TestCase(68, 100000000, 947679093, 12252240, 263, 18, 173),
            TestCase(69, 100000000, 156590387, 12252240, 265, 18, 139),
            TestCase(70, 100000000, 1132018687, 12252240, 267, 18, 105),
            TestCase(71, 100000000, 1133284357, 12252240, 268, 18, 88),
            TestCase(72, 100000000, 475545473, 12252240, 270, 18, 108),
            TestCase(73, 100000000, 481714433, 12252240, 271, 18, 127),
            TestCase(74, 100000000, 1083087326, 12252240, 273, 18, 165),
            TestCase(75, 100000000, 75546672, 360360, 205, 1, 203),
            TestCase(76, 100000000, 974190472, 232792560, 263, 19, 149),
            TestCase(77, 100000000, 72289873, 232792560, 265, 19, 113),
            TestCase(78, 100000000, 475466486, 232792560, 267, 19, 77),
            TestCase(79, 100000000, 475725836, 232792560, 267, 19, 77),
            TestCase(80, 100000000, 526331837, 4423058640, 269, 19, 79),
            TestCase(81, 100000000, 435212699, 232792560, 310, 19, 272),
            TestCase(82, 100000000, 309464189, 232792560, 299, 20, 159),
            TestCase(83, 100000000, 563341947, 232792560, 300, 20, 140),
            TestCase(84, 100000000, 999509319, 61261200, 303, 20, 83),
            TestCase(85, 100000000, 1078162250, 232792560, 343, 20, 83),
            TestCase(86, 100000000, 1202979773, 232792560, 345, 20, 85),
            TestCase(87, 100000000, 1173219092, 232792560, 347, 20, 127),
            TestCase(88, 100000000, 981881020, 232792560, 349, 20, 169),
            TestCase(89, 100000000, 1091558889, 232792560, 335, 20, 295),
            TestCase(90, 100000000, 1048540830, 232792560, 359, 21, 338),
            TestCase(91, 100000000, 1063507007, 232792560, 361, 21, 298),
            TestCase(92, 100000000, 1034486066, 232792560, 364, 21, 238),
            TestCase(93, 100000000, 717480582, 232792560, 345, 21, 198),
            TestCase(94, 100000000, 132609609, 232792560, 346, 21, 178),
            TestCase(95, 100000000, 271276851, 232792560, 348, 21, 201),
            TestCase(96, 100000000, 339777873, 1629547920, 333, 21, 333),
            TestCase(97, 100000000, 357552876, 232792560, 376, 21, 355),
            TestCase(98, 100000000, 1052482442, 232792560, 400, 22, 378),
            TestCase(99, 100000000, 615117769, 232792560, 403, 22, 315)
        ]
        self.CHALLENGES = [
            TestCase(3000, 10**16, 1013079068, 1749342047920660916901891145781670987072592322134428432000, 16470, 135, UNKNOWN),
            TestCase(6000, 10**16, 132286426, 8603769834781171457272804805623074954273764323780252384481978979089202817658786064000, 33511, 194, UNKNOWN),
            TestCase(10**4, 10**16, UNKNOWN, 8337245403447921335829504375888192675135162254454825924977726845769444687965016467695833282339504042669808000, 58435, 253, UNKNOWN),
        ]

# Constants
MOD = 1234567891

# Logging
info = True
debug = False
verbose = False
timing = True
def logInfo(msg = ""):
    if info:
        print("INFO: " + msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print("DEBUG: " + msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print("VERBOSE: " + msg, flush=True)
def logTiming(msg = ""):
    if timing:
        print("TIME: " + msg, flush=True)

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

def stepMulti(currList, currIndex, numSteps):
    for i in range(numSteps):
        currList = nextList(currList)
    return currList, currIndex + numSteps

def logValueMap(valueMap, indent=2, logger = logVerbose):
    for i in sorted(valueMap.keys()):
        v = valueMap[i]
        logger(f"{' '*indent}  {i}: {v}")

def printTestResult(tc, result):
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
    logInfo(f"{c}{b}TestCase({tc.N}, {tc.numIters}, {result.expected}, {result.period}, {result.periodStart}, {result.shapePeriod}, {result.shapePeriodStart}),{RESET_COLOR}")

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
                2:2, 3:2,       # 4 = 2*2
                4:5,            # 5
                5:2, 6:3,       # 6 = 2*3
                7:7,            # 7
                8:2, 9:2, 10:2  # 8 = 2*2*2
            }
    """

    symbolToValueMap = {}
    valueToIndexListMap = defaultdict(list)
    logDebug(f"toDenatured input:")
    logList(inputList, -1, logDebug)
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

    logDebug(f"toDenatured output:")
    logList(outputList, -1, logDebug)
    logDebug(f"  symbolToValueMap")
    logValueMap(symbolToValueMap, indent=4, logger=logDebug)

    return outputList, symbolToValueMap

def getTupleAndShapeFromList(currList):
    tmp = sorted([(len(e), e) for e in currList])
    currShape = tuple(n for (n, entry) in tmp)
    currTuple = tuple(tuple(v for v in entry) for (n, entry) in tmp)

    return currTuple, currShape

def getShapeFromList(currList):
    return [len(e) for e in currList]

def nextShape(inShape):
    shape = [e - 1 for e in inShape if e > 1]
    shape.append(len(inShape))

    return tuple(shape)

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
    logVerbose(f"Running computePerm")
    logVerbose(f"  Checking perm for:")
    logVerbose(f"    prevTuple: {prevTuple}")
    logVerbose(f"    currTuple: {currTuple}")

    symbols = set(symbolsIn)
    perm = dict()
    for j in range(len(prevTuple)):
        for k in range(len(prevTuple[j])):
            perm[prevTuple[j][k]] = currTuple[j][k]

    if verbose:
        logVerbose(f"Permutation:")
        logVerbose(f"  Base permutation:")
        for s in sorted(symbols):
            logVerbose(f"  {s:2}: {perm[s]:2}")

    permFactored = list()
    logVerbose(f"    Factored permutation:")
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
        logVerbose(f"      {factor}")
        permFactored.append(factor)
    permFactored = tuple(permFactored)
    logVerbose(f"    -> {permFactored}")
    return perm, permFactored

def transformPermToIndexedFactors(perm):
    logDebug(f"Transforming permutation to indexed-factors permutation")
    logVerbose(f"  perm: {perm}")
    indexedFactors = dict()
    symbols = sorted(perm.keys())
    for a in symbols:
        factor = [a]
        b = perm[a]
        while b != a:
            factor.append(b)
            b = perm[b]
        indexedFactors[a] = factor
        logVerbose(f"    {a:2}: {factor}")

    return indexedFactors

def lcm(a, b):
    return a * b // gcd(a, b)

def lcmArray(arr):
    if len(arr) < 2:
        raise Exception(f"lcm requires an array of at least two numbers, but got {arr}")
    ret = 1
    for e in arr:
        ret = lcm(ret, e)
    return ret

def determineShapePeriodDetails(n, numIters):
    """
    Determine the shapePeriod and the shapePeriodStart for the given
    n and numIters. If these cannot be found by numIters, return UNKNOWN
    for both values, which will indicate that the shape period shortcut
    is not helpful for these values.
    """
    origList = transformRange(n)
    currShape = getShapeFromList(origList)
    shapeToIndexMap = defaultdict(int)
    shapePeriod, shapePeriodStart = UNKNOWN, UNKNOWN
    w = int(log10(numIters)) + 1
    logDebug(f"Determining shape period detials for n = {n} and numIters = {numIters}")
    logVerbose(f"  {0:{w}}: {currShape}")
    for currIndex in range(1, numIters+1):
        currShape = nextShape(currShape)
        logVerbose(f"  {currIndex:{w}}: {currShape}")

        prevIndex = shapeToIndexMap[currShape]
        if prevIndex:
            shapePeriodStart = prevIndex
            shapePeriod = currIndex - shapePeriodStart
            logDebug(f"  Found a repeated shape: shapePeriod {shapePeriod} starting at index {shapePeriodStart}")
            logVerbose(f"  Shape: {currShape}")
            break
        else:
            shapeToIndexMap[currShape] = currIndex

    return shapePeriod, shapePeriodStart

def runFactorShuffle(n, numIters):
    logInfo(f"Running {numIters} rounds for n = {n}:")

    period, periodStart = UNKNOWN, UNKNOWN
    prevPerm, currPerm = UNKNOWN, UNKNOWN
    perm, permFactored, indexedPermFactors = UNKNOWN, UNKNOWN, UNKNOWN
    permPeriod = UNKNOWN
    remainingIters, fullPeriodsToSkip, itersAfterFullPeriods, shortCircuitIndex = UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN

    shapePeriod, shapePeriodStart = determineShapePeriodDetails(n, numIters)

    origList = transformRange(n)
    logList(origList, 0, logDebug)
    currList, symbolToValueMap = toDenatured(origList)
    symbols = set(symbolToValueMap.keys())
    finalList = UNKNOWN
    currIndex = 0
    if shapePeriod == UNKNOWN:
        logDebug(f"Shape period will NOT help, so running all {numIters} iters")
        currList, currIndex = stepMulti(currList, currIndex, numIters)
    else:
        logDebug(f"Shape period WILL help")
        currList, currIndex = stepMulti(currList, currIndex, shapePeriodStart)
        if verbose:
            currShape = getShapeFromList(currList)
            logVerbose(f"After shapePeriodStart={shapePeriodStart} iters:")
            logVerbose(f"  List:  {currList}")
            logVerbose(f"  Shape: {currShape}")

        prevPerm, currPerm = UNKNOWN, UNKNOWN
        # Figure out perm to shortcut with. Stop at numIters if encountered first.
        while ((prevPerm == UNKNOWN) or (prevPerm != currPerm)):
            prevList = currList
            maxNextSteps = numIters - currIndex
            numSteps = min(maxNextSteps, shapePeriod)
            currList, currIndex = stepMulti(currList, currIndex, numSteps)
            if maxNextSteps <= shapePeriod:
                break
            prevPerm = currPerm
            currPerm, currPermFactored = computePerm(prevList, currList, symbols)

        if prevPerm == currPerm:
            perm = currPerm
            permFactored = currPermFactored
            permPeriod = lcmArray([len(factor) for factor in permFactored])
            period = permPeriod * shapePeriod
            periodStart = currIndex - 2*shapePeriod

            remainingIters = numIters - currIndex
            fullPeriodsToSkip = remainingIters // period
            itersAfterFullPeriods = remainingIters % period
            shortCircuitIndex = currIndex + itersAfterFullPeriods

            # extend list, if needed
            logList(currList, currIndex)
            logInfo(f"Need to perform {remainingIters} more steps")
            logInfo(f"  Need to perform {fullPeriodsToSkip} full periods to skip")
            additionalShortCircuitSteps = shortCircuitIndex - currIndex
            logInfo(f"  Need to perform {additionalShortCircuitSteps} more steps after ignoring full periods")
            if additionalShortCircuitSteps > 0:
                shapeLoops = additionalShortCircuitSteps // shapePeriod
                additionalSubSteps = additionalShortCircuitSteps % shapePeriod
                logInfo(f"    {shapeLoops} shape periods")
                indexedPermFactors = transformPermToIndexedFactors(perm)
                tmpList = []
                for e in currList:
                    newE = []
                    for v in e:
                        factor = indexedPermFactors[v]
                        lenFactor = len(factor)
                        newV = factor[shapeLoops % lenFactor]
                        newE.append(newV)
                    tmpList.append(newE)
                currIndex += shapeLoops * shapePeriod
                logDebug(f"  After shape periods:")
                logDebug(f"  {currIndex + shapeLoops*shapePeriod:2}: {finalList}")
                logList(finalList, currIndex)

                logInfo(f"    {additionalSubSteps} steps after shape periods")
                for i in range(additionalSubSteps):
                    tmpList = nextList(tmpList)
                    currIndex += 1
                    logDebug(f"  {currIndex}: {finalList}")
                currList = tmpList
                logList(currList, currIndex)

    finalIndex = currIndex
    finalList = currList
    finalShape = getShapeFromList(finalList)

    finalListOrigValues = [[symbolToValueMap[e] for e in ee] for ee in finalList]

    logInfo(f"------------------- RESULT DETAILS -------------------")
    logInfo(f"  n                  {n}")
    logInfo(f"  numIters           {numIters}")
    logInfo(f"  " + "-" * 50)
    logInfo(f"  finalIndex         {finalIndex}")
    logInfo(f"  shortCircuitIndex: {shortCircuitIndex}")
    logInfo(f"  finalShape:        {tuple(finalShape)}")
    logInfo(f"  " + "-" * 50)
    # index of first repeated shape
    # index of start of first loop
    # shapeLoop len
    # permutation len
    # full period len
    logInfo(f"  periodStart        {periodStart}")
    logInfo(f"  shapePeriod        {shapePeriod}")
    logInfo(f"  permPeriod         {permPeriod}")
    logInfo(f"  period             {period} = {shapePeriod} * {permPeriod}")
    logInfo(f"  remainingIters     {remainingIters}")
    logInfo(f"  loopsToSkip:       {fullPeriodsToSkip}")
    logInfo(f"  itersAfterLooping: {itersAfterFullPeriods}")
    logDebug(f"  " + "-" * 50)
    logDebug(f"  finalList:           {finalList}")
    logDebug(f"  finalListOrigValues: {finalListOrigValues}")
    logInfo(f"------------------------------------------------------")

    if verbose:
        logVerbose(f"Final symbol list:")
        logList(currList, numIters, logVerbose)
        logVerbose(f"Final value list:")
        logList(finalListOrigValues, numIters, logVerbose)

    prodList = transformFactoredListIntoProductList(finalListOrigValues)
    finalSum = sum(prodList)
    finalSumAfterMod = finalSum % MOD
    logInfo(f"S({n}, {numIters}) -> {finalSum}")
    logDebug(f"S({n}, {numIters}) -> {prodList} -> {finalSum}")

    return finalSum, finalSumAfterMod, period, periodStart, shapePeriod, shapePeriodStart

def runTests(tests):
    for test in tests:
        startTime = getTimeInMillis()
        N = test.N
        numIters = test.numIters
        logInfo(f"Running against N = {N}")

        ansBeforeMod, ans, period, periodStart, shapePeriod, shapePeriodStart = runFactorShuffle(N, numIters)
        result = TestCase(N, numIters, ans, period, periodStart, shapePeriod, shapePeriodStart)
        printTestResult(test, result)

        endTime = getTimeInMillis()
        logTimeDiff = endTime - startTime
        logTiming(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")
        logInfo()
        logInfo()
        logInfo()

def troubleshoot():
    for n in range(3, 100):
        numIters = 10 ** 8
        finalSum, period, periodStart = runFactorShuffle(n, numIters)
        logInfo(f"period(n = {n:7d}) = {period:7d} (starts at {periodStart:7}) (final sum after {numIters} rounds: {finalSum}")
        ans = finalSum % MOD
        TestCase()
        logInfo(f"TestCase({n}, {numIters}, {ans}, {period}, {periodStart}, UNKNOWN, UNKNOWN),")

# Main logic
def main():
    #troubleshoot()

    testCaseCollections = TestCaseCollections()
    tests = testCaseCollections.CHALLENGES
    runTests(tests)

# Main logic
if __name__ == '__main__':
    main()
