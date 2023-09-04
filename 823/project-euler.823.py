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
TestCase(5, 3, 21, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN),
TestCase(5, 10, 19, 6, 4, 3, UNKNOWN),
TestCase(10, 100, 257, 60, 9, 1, UNKNOWN),
TestCase(10, 101, 175, 60, 9, 1, UNKNOWN),
TestCase(10, 1000, 257, 60, 9, 1, UNKNOWN),
TestCase(10, 1001, 175, 60, 9, 1, UNKNOWN),
TestCase(100, 1000, 989136573, 232792560, 400, 22, UNKNOWN),
TestCase(100, 10**6, 360990789, 232792560, 400, 22, UNKNOWN),
TestCase(1000, 100000, 803889757, 410555180440430163438262940577600, 4840, 76, UNKNOWN),
TestCase(3000, 10**16, 1013079068, 1749342047920660916901891145781670987072592322134428432000, 16470, 135, UNKNOWN),
TestCase(6000, 10**16, 132286426, 8603769834781171457272804805623074954273764323780252384481978979089202817658786064000, 33511, 194, UNKNOWN),
TestCase(10**4, 10**16, UNKNOWN, 8337245403447921335829504375888192675135162254454825924977726845769444687965016467695833282339504042669808000, 58435, 253, UNKNOWN),
]
"""
TestCase(3, 100000000, 5, 2, 1, 2, UNKNOWN),
TestCase(4, 100000000, 14, 6, 1, 3, UNKNOWN),
TestCase(5, 100000000, 19, 6, 4, 3, UNKNOWN),
TestCase(6, 100000000, 22, 12, 9, 4, UNKNOWN),
TestCase(7, 100000000, 58, 12, 9, 2, UNKNOWN),
TestCase(8, 100000000, 87, 150, 9, 5, UNKNOWN),
TestCase(9, 100000000, 127, 60, 16, 5, UNKNOWN),
TestCase(10, 100000000, 257, 60, 9, 1, UNKNOWN),
TestCase(11, 100000000, 268, 60, 16, 6, UNKNOWN),
TestCase(12, 100000000, 250, 60, 25, 6, UNKNOWN),
TestCase(13, 100000000, 394, 60, 25, 6, UNKNOWN),
TestCase(14, 100000000, 841, 420, 20, 7, UNKNOWN),
TestCase(15, 100000000, 2113, 420, 20, 7, UNKNOWN),
TestCase(16, 100000000, 1594, 420, 30, 1, UNKNOWN),
TestCase(17, 100000000, 5434, 840, 31, 8, UNKNOWN),
TestCase(18, 100000000, 5780, 840, 31, 8, UNKNOWN),
TestCase(19, 100000000, 6050, 840, 31, 8, UNKNOWN),
TestCase(20, 100000000, 3940, 840, 19, 1, UNKNOWN),
TestCase(21, 100000000, 5938, 11340, 47, 9, UNKNOWN),
TestCase(22, 100000000, 6034, 2520, 60, 9, UNKNOWN),
TestCase(23, 100000000, 6958, 2520, 60, 9, UNKNOWN),
TestCase(24, 100000000, 12949, 2520, 73, 1, UNKNOWN),
TestCase(25, 100000000, 22105, 2520, 47, 10, UNKNOWN),
TestCase(26, 100000000, 26037, 2520, 47, 10, UNKNOWN),
TestCase(27, 100000000, 79697, 2520, 77, 10, UNKNOWN),
TestCase(28, 100000000, 32130, 2520, 92, 1, UNKNOWN),
TestCase(29, 100000000, 41790, 27720, 93, 11, UNKNOWN),
TestCase(30, 100000000, 166449, 27720, 62, 11, UNKNOWN),
TestCase(31, 100000000, 202449, 27720, 62, 11, UNKNOWN),
TestCase(32, 100000000, 139719, 27720, 96, 11, UNKNOWN),
TestCase(33, 100000000, 110691, 27720, 80, 12, UNKNOWN),
TestCase(34, 100000000, 118341, 27720, 79, 12, UNKNOWN),
TestCase(35, 100000000, 310381, 27720, 79, 12, UNKNOWN),
TestCase(36, 100000000, 451837, 27720, 62, 12, UNKNOWN),
TestCase(37, 100000000, 1032445, 27720, 75, 12, UNKNOWN),
TestCase(38, 100000000, 634674, 27720, 127, 1, UNKNOWN),
TestCase(39, 100000000, 507422, 360360, 128, 13, UNKNOWN),
TestCase(40, 100000000, 326548, 360360, 90, 13, UNKNOWN),
TestCase(41, 100000000, 420148, 360360, 90, 13, UNKNOWN),
TestCase(42, 100000000, 1624326, 360360, 132, 13, UNKNOWN),
TestCase(43, 100000000, 3398406, 360360, 132, 13, UNKNOWN),
TestCase(44, 100000000, 9070145, 360360, 153, 14, UNKNOWN),
TestCase(45, 100000000, 64301021, 360360, 153, 14, UNKNOWN),
TestCase(46, 100000000, 37401802, 360360, 114, 14, UNKNOWN),
TestCase(47, 100000000, 37405344, 360360, 114, 14, UNKNOWN),
TestCase(48, 100000000, 10245357, 360360, 157, 14, UNKNOWN),
TestCase(49, 100000000, 9675349, 360360, 179, 1, UNKNOWN),
TestCase(50, 100000000, 6047747, 360360, 180, 15, UNKNOWN),
TestCase(51, 100000000, 7252885, 360360, 180, 15, UNKNOWN),
TestCase(52, 100000000, 14454957, 360360, 180, 15, UNKNOWN),
TestCase(53, 100000000, 30928557, 360360, 180, 15, UNKNOWN),
TestCase(54, 100000000, 92400668, 360360, 180, 15, UNKNOWN),
TestCase(55, 100000000, 69547142, 360360, 208, 1, UNKNOWN),
TestCase(56, 100000000, 14298692, 11531520, 180, 16, UNKNOWN),
TestCase(57, 100000000, 10603214, 720720, 209, 16, UNKNOWN),
TestCase(58, 100000000, 20597678, 11531520, 180, 16, UNKNOWN),
TestCase(59, 100000000, 31705838, 11531520, 180, 16, UNKNOWN),
TestCase(60, 100000000, 83930382, 11531520, 180, 16, UNKNOWN),
TestCase(61, 100000000, 215258382, 11531520, 180, 16, UNKNOWN),
TestCase(62, 100000000, 223986518, 720720, 225, 1, UNKNOWN),
TestCase(63, 100000000, 162046732, 12252240, 226, 17, UNKNOWN),
TestCase(64, 100000000, 135671456, 104144040, 209, 17, UNKNOWN),
TestCase(65, 100000000, 438327890, 104144040, 209, 17, UNKNOWN),
TestCase(66, 100000000, 474948670, 104144040, 209, 17, UNKNOWN),
TestCase(67, 100000000, 474949792, 104144040, 209, 17, UNKNOWN),
TestCase(68, 100000000, 578737716, 6486480, 240, 18, UNKNOWN),
TestCase(69, 100000000, 436540770, 6486480, 240, 18, UNKNOWN),
TestCase(70, 100000000, 1132018687, 12252240, 259, 18, UNKNOWN),
TestCase(71, 100000000, 1133284357, 12252240, 259, 18, UNKNOWN),
TestCase(72, 100000000, 475545473, 12252240, 259, 18, UNKNOWN),
TestCase(73, 100000000, 481714433, 12252240, 259, 18, UNKNOWN),
TestCase(74, 100000000, 1083087326, 12252240, 259, 18, UNKNOWN),
TestCase(75, 100000000, 75546672, 360360, 205, 1, UNKNOWN),
TestCase(76, 100000000, 974190472, 232792560, 259, 19, UNKNOWN),
TestCase(77, 100000000, 72289873, 232792560, 259, 19, UNKNOWN),
TestCase(78, 100000000, 475466486, 232792560, 259, 19, UNKNOWN),
TestCase(79, 100000000, 475725836, 232792560, 259, 19, UNKNOWN),
TestCase(80, 100000000, 526331837, 4423058640, 258, 19, UNKNOWN),
TestCase(81, 100000000, 435212699, 232792560, 294, 19, UNKNOWN),
TestCase(82, 100000000, 309464189, 232792560, 294, 20, UNKNOWN),
TestCase(83, 100000000, 563341947, 232792560, 294, 20, UNKNOWN),
TestCase(84, 100000000, 999509319, 61261200, 294, 20, UNKNOWN),
TestCase(85, 100000000, 1078162250, 232792560, 331, 20, UNKNOWN),
TestCase(86, 100000000, 1202979773, 232792560, 331, 20, UNKNOWN),
TestCase(87, 100000000, 1173219092, 232792560, 331, 20, UNKNOWN),
TestCase(88, 100000000, 981881020, 232792560, 331, 20, UNKNOWN),
TestCase(89, 100000000, 1091558889, 232792560, 331, 20, UNKNOWN),
TestCase(90, 100000000, 1048540830, 232792560, 359, 21, UNKNOWN),
TestCase(91, 100000000, 1063507007, 232792560, 359, 21, UNKNOWN),
TestCase(92, 100000000, 1034486066, 232792560, 359, 21, UNKNOWN),
TestCase(93, 100000000, 717480582, 232792560, 331, 21, UNKNOWN),
TestCase(94, 100000000, 132609609, 232792560, 331, 21, UNKNOWN),
TestCase(95, 100000000, 271276851, 232792560, 331, 21, UNKNOWN),
TestCase(96, 100000000, 339777873, 1629547920, 333, 21, UNKNOWN),
TestCase(97, 100000000, 357552876, 232792560, 370, 21, UNKNOWN),
TestCase(98, 100000000, 1052482442, 232792560, 400, 22, UNKNOWN),
TestCase(99, 100000000, 615117769, 232792560, 400, 22, UNKNOWN)
# ]
# """

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
    logInfo(f"{c}{b}TestCase({tc.N}, {tc.numIters}, {result.expected}, {result.period}, {result.periodStart}, {result.shapePeriod}, {result.shapePeriodStart}, UNKNOWN),{RESET_COLOR}")

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
    # logger(f"toDenatured input:")
    # logList(inputList, -1, logger = logger)
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
    # logger(f"valueToIndexListMap")
    # logValueMap(valueToIndexListMap, logger)
    # logger(f"symbolToValueMap")
    # logValueMap(symbolToValueMap, logger)
    # logger(f"toDenatured output:")
    # logList(outputList, -1, logger)
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
    #logDebug(f"    Checking perm for:")
    #logDebug(f"      prevTuple: {prevTuple}")
    #logDebug(f"      currTuple: {currTuple}")
    symbols = set(symbolsIn)
    perm = dict()
    for j in range(len(prevTuple)):
        for k in range(len(prevTuple[j])):
            perm[prevTuple[j][k]] = currTuple[j][k]

    # if verbose:
    #     logVerbose(f"Permutation:")
    #     logVerbose(f"  Base permutation:")
    #     for s in sorted(symbols):
    #         logVerbose(f"  {s:2}: {perm[s]:2}")

    permFactored = list()
    #logDebug(f"    Factored permutation:")
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
        #logDebug(f"      {factor}")
        permFactored.append(factor)
    permFactored = tuple(permFactored)
    #logDebug(f"    -> {permFactored}")
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
    logger = logDebug
    # logList(origList, 0, logger)

    period, periodStart = UNKNOWN, UNKNOWN
    prevPerm, currPerm = UNKNOWN, UNKNOWN
    perm, permFactored, indexedFactors = UNKNOWN, UNKNOWN, UNKNOWN
    permPeriod = UNKNOWN
    remainingIters, loopsToSkip, itersAfterLooping, shortCircuitIndex = UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN

    shapePeriod, shapePeriodStart = determineShapePeriodDetails(n, numIters)

    origList = transformRange(n)
    currList, symbolToValueMap = toDenatured(origList)
    symbols = set(symbolToValueMap.keys())
    finalList = UNKNOWN
    currIndex = 0
    if shapePeriod == UNKNOWN:
        logDebug(f"Shape period will NOT help, so running all {numIters} iters")
        for i in range(numIters):
            currIndex += 1
            currList = nextList(currList)
        finalList = currList
    else:
        logDebug(f"Shape period WILL help")
        for i in range(shapePeriodStart):
            currIndex += 1
            currList = nextList(currList)
        if verbose:
            currShape = getShapeFromList(currList)
            logVerbose(f"After {shapePeriodStart} iters:")
            logVerbose(f"  List:  {currList}")
            logVerbose(f"  Shape: {currShape}")

        prevPerm, currPerm = UNKNOWN, UNKNOWN
        # Figure out perm to shortcut with. Stop at numIters if encountered first.
        while ((prevPerm == UNKNOWN) or (prevPerm != currPerm)) and (currIndex != numIters):
            prevList = currList
            for i in range(shapePeriod):
                currIndex += 1
                currList = nextList(currList)
                if currIndex == numIters:
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
            # fullPeriodsToSkip = remainingIters // period
            loopsToSkip = remainingIters // period
            # itersAfterFullPeriods = remainingIters % period
            itersAfterLooping = remainingIters % period
            shortCircuitIndex = currIndex + itersAfterLooping

            # extend list, if needed
            # logList(currList, currIndex)
            logInfo(f"Need to perform {remainingIters} more steps")
            logInfo(f"  Need to perform {loopsToSkip} full periods to skip")
            # additionalShortCircuitSteps = shortCircuitIndex - currIndex
            additionalSteps = shortCircuitIndex - currIndex
            logInfo(f"  Need to perform {additionalSteps} more steps after ignoring full periods")
            if additionalSteps > 0:
                shapeLoops = additionalSteps // shapePeriod
                additionalSubSteps = additionalSteps % shapePeriod
                logInfo(f"    {shapeLoops} shape periods")
                # indexedPermFactors = transformPermToIndexedFactors(perm)
                indexedFactors = transformPermToIndexedFactors(perm)
                tmpList = []
                for e in currList:
                    newE = []
                    for v in e:
                        factor = indexedFactors[v]
                        lenFactor = len(factor)
                        newV = factor[shapeLoops % lenFactor]
                        newE.append(newV)
                    tmpList.append(newE)
                # logDebug(f"  After shape periods:")
                #logDebug(f"  {currIndex + shapeLoops*shapePeriod:2}: {finalList}")
                # logList(finalList, currIndex + shapeLoops*shapePeriod, logDebug)

                logInfo(f"    {additionalSubSteps} steps after shape periods")
                for i in range(additionalSubSteps):
                    tmpList = nextList(tmpList)
                    #logDebug(f"  {currIndex + shapeLoops*shapePeriod + ii:2}: {finalList}")
                    # logList(finalList, currIndex + shapeLoops*shapePeriod + 11, logInfo)
                # logList(currList, currIndex)
                currList = tmpList

        finalList = currList
        finalShape = getShapeFromList(finalList)
        # logList(finalList, numIters)

        # finalListOrigValues = [[symbolToValueMap[e] for e in ee] for ee in finalList]

        logInfo(f"---------- THIS ENTRY HAS BEEN SEEN BEFORE ----------")
        logInfo(f"  n                  {n}")
        logInfo(f"  numIters           {numIters}")
        logInfo(f"  " + "-" * 50)
        logInfo(f"  currIndex          {currIndex}")
        logInfo(f"  periodStart        {periodStart}")
        logInfo(f"  shapePeriod        {shapePeriod}")
        logInfo(f"  finalShape:        {tuple(finalShape)}")
        logInfo(f"  permPeriod         {permPeriod}")
        logInfo(f"  period             {period} = {shapePeriod} * {permPeriod}")
        logInfo(f"  remainingIters     {remainingIters}")
        logInfo(f"  loopsToSkip:       {loopsToSkip}")
        logInfo(f"  itersAfterLooping: {itersAfterLooping}")
        logInfo(f"  shortCircuitIndex: {shortCircuitIndex}")
        # logInfo(f"  " + "-" * 50)
        # logInfo(f"  finalList:           {finalList}")
        # logInfo(f"  finalListOrigValues: {finalListOrigValues}")
        logInfo(f"-----------------------------------------------------")

    finalValueList = [[symbolToValueMap[i] for i in e] for e in finalList]

    # if verbose:
    #     logVerbose(f"Final symbol list:")
    #     logList(currList, numIters, logVerbose)
    #     logVerbose(f"Final value list:")
    #     logList(finalValueList, numIters, logVerbose)

    prodList = transformFactoredListIntoProductList(finalValueList)
    finalSum = sum(prodList)
    logInfo(f"S({n}, {numIters}) -> {prodList} -> {finalSum}")

    return finalSum, period, periodStart, shapePeriod, shapePeriodStart

def runTests():
    for test in TESTS:
        startTime = getTimeInMillis()
        N = test.N
        numIters = test.numIters
        expected = test.expected
        logInfo(f"Running against N = {N}")

        ansBeforeMod, period, periodStart, shapePeriod, shapePeriodStart = runFactorShuffle(N, numIters)
        # logInfo(f"period(n = {N:7d}) = {period:7} (starts at {periodStart:7}) (final sum after {numIters} rounds: {ansBeforeMod}")
        ans = ansBeforeMod % MOD
        result = TestCase(N, numIters, ans, period, periodStart, shapePeriod, shapePeriodStart)
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
