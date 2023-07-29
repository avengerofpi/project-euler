#!/usr/bin/python3

# Imports
from math import log, log2, log10, sqrt, gcd
import scipy
from datetime import timedelta
import time
from collections import defaultdict
import itertools
from colorama import Fore, Back, Style

# Constants
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

UNKNOWN = "UNKNOWN"
TESTS = [
TestCase( 3,      "1.6514"),
TestCase( 4,     "19.6564"),
TestCase( 5,     "97.8133"), #     "97.81334558787319"
TestCase( 6,    "325.0072"), #    "325.0072365326804"
TestCase( 7,    "851.1948"), #    "851.1947929255208"
TestCase( 8,   "1903.3867"), #   "1903.386686792866"
TestCase( 9,   "3801.6290"), #   "3801.6289566334553"
TestCase(10,   "6974.9840"), #   "6974.983978268594"
TestCase(11,  "11977.5112"), #  "11977.511213075131"
TestCase(12,  "19504.2478"), #  "19504.24783880133"
TestCase(13,  "30407.1893"), #  "30407.189289768656"
TestCase(14,  "45711.2698"), #  "45711.269791541185"
TestCase(16,  "94583.1615"), #  "94583.16151446037"
TestCase(15,  "66630.3428"), #  "66630.34280795284"
TestCase(17, "131209.3592"), # "131209.3592441513"
TestCase(18, "178385.4299"), # "178385.4299324293"
TestCase(19, "238240.7085"), # "238240.70852004984"
TestCase(20, "313173.3515"), # "313173.3514525104"
TestCase(21, "405866.3170"), # "405866.3169928597"
TestCase(22, "519303.3456"), # "519303.34561997105"
TestCase(23, "656784.9407"), # "656784.940706292"
#TestCase(40, UNKNOWN),
]

# Logging
info = True
debug = False
verbose = False
laminaFlag = False
colorFlag = True
def logInfo(msg = ""):
    if info:
        print(msg, flush=True)
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)
def logVerbose(msg = ""):
    if verbose:
        print(msg, flush=True)

def getTimeInMillis():
    return int(time.time() * 1000)

def printLamina(n, a, b, w, h):
    if not laminaFlag:
        return

    debugWas = debug
    debug = True

    INDENT = '  '
    X = 'x'
    VOID = ' '
    FULL_LINE = X*n
    VOID_LINE = X*a + VOID*w + X*(n-a-w)
    # Top rows until void starts
    for r in range(n, b+h, -1):
        logDebug(INDENT + FULL_LINE)
    # Print rows with void portion
    for r in range(b+h, b, -1):
        logDebug(INDENT + VOID_LINE)
    # Bottom rows after void
    for r in range(b, 0, -1):
        logDebug(INDENT + FULL_LINE)

    debug = debugWas

def printTestResult(tc, result):
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

    if not colorFlag:
        b = ""
        c = ""
        RESET_COLOR = ""
    logInfo(f"{c}{b} Result for {tc.N}: {successStr} {RESET_COLOR}")
    logInfo(f"  Expected: {tc.expected:10}")
    logInfo(f"  Actual:   {result.expected:10}")

# Functions
def dist(x1, y1, x2, y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2 )

def ONE(a, b, c, d):
    return 1

memoizedPartials = dict()
def getPartial(a, b, c, d):
    options = {
        "limit": 100,
        "epsabs": 1.49e-10
    }

    bounds = (a, b, c, d)
    v = 0
    logVerbose(f"Computing partial for {bounds}")
    if bounds in memoizedPartials.keys():
        logVerbose(f"  Partial HAS been previously computed")
        v = memoizedPartials[bounds]
    else:
        logVerbose(f"  Partial has NOT been previously computed")
        #v = scipy.integrate.nquad(ONE, bounds, opts=options)[0]
        v = scipy.integrate.nquad(dist, bounds, opts=options)[0]
        memoizedPartials[bounds] = v
    logVerbose(f"Partial for {bounds}: value: {v}")

    return v

memoizedExpectedDistForSquareLamina = dict()
def expectedDistForSquareLamina(n, a, b, w, h):
    lamina = (n, a, b, w, h)
    logVerbose(f"computing expectedDistForSquareLamina({lamina})")
    printLamina(n, a, b, w, h)
    if lamina in memoizedExpectedDistForSquareLamina.keys():
        expectedDist = memoizedExpectedDistForSquareLamina[lamina]
        logVerbose(f"The value for {lamina} is known from previous computations")
    else:
        #expectedDist = 1

        logVerbose(f"lamina {lamina}")
        boundsToFreqMap = defaultdict(int)
        n, a, b, w, h = lamina
        for t in itertools.product(*itertools.repeat(range(n), 4)):
            x1, y1, x2, y2 = t
            if ((a <= x1 and x1 <  a+w) and (b <= y1 and y1 <  b+h)) or ((a <= x2 and x2 <  a+w) and (b <= y2 and y2 <  b+h)):
                logVerbose(f"Skipping coors {(x1, y1), (x2, y2)}")
                continue
            dx, dy = sorted([abs(x2-x1), abs(y2-y1)])
            bounds = ((0,1), (0,1), (dx, dx+1), (dy, dy+1))
            boundsToFreqMap[bounds] += 1

        e = 0
        for bounds, freq in sorted(boundsToFreqMap.items()):
            area = getPartial(*bounds)
            areaMultiplied = area * freq
            logVerbose(f"lamina {lamina}: {bounds} occurs {freq:>2} times -> {area:10.6f} -> {areaMultiplied:10.6f}")
            e += areaMultiplied

        areaSquare = n ** 2
        areaVoid = w * h
        valueToDivideBy = (areaSquare - areaVoid) ** 2
        expectedDist  = e / valueToDivideBy
        logVerbose(f"  lamina {lamina} -> {expectedDist  :10.6f}")

    logDebug(f"expectedDistForSquareLamina({lamina}): {expectedDist}")
    if lamina not in memoizedExpectedDistForSquareLamina.keys():
        equivalentKeys = [
            (n,     a,     b, w, h),
            (n,     a, n-b-h, w, h),
            (n, n-a-w,     b, w, h),
            (n, n-a-w, n-b-h, w, h),

            (n,     b,     a, h, w),
            (n, n-b-h,     a, h, w),
            (n,     b, n-a-w, h, w),
            (n, n-b-h, n-a-w, h, w),
        ]
        equivalentKeys = sorted(set(equivalentKeys))
        logVerbose(f"The following keys are quivalent:")
        for k in equivalentKeys:
            logVerbose(f"  {k}")
            #printLamina(*k)
            memoizedExpectedDistForSquareLamina[k] = expectedDist
    logVerbose()
    return expectedDist

def sumExpectedDistForSquareLaminaeOfSizeN(n):
    logDebug(f"sumExpectedDistForSquareLaminaeOfSizeN({n})")
    total = 0
    startTime = getTimeInMillis()
    for a in range(1, n-1):
        for w in range(1, n-a):
            for b in range(1, n-1):
                for h in range(1, n-b):
                    total += expectedDistForSquareLamina(n, a, b, w, h)
    logDebug(f"SubTotal for N = {n:>2}: {total}")
    testCase = None
    for t in TESTS:
        if t.N == n:
            testCase = t
            break
    if testCase:
        expected = testCase.expected
        ansStr = f"{total:.4f}"
        result = TestCase(n, ansStr)
        printTestResult(testCase, result)
        #logDebug(f"{n}: {ansStr} - {successStr}")
    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logDebug(f"  Time spent: {timedelta(milliseconds=logTimeDiff)} (for N = {n:>2})")
    return total

def runMain():
    total = 0
    minN = 3
    maxN = 40
    #for n in [3]:
    grandTotal = 0
    startTime = getTimeInMillis()
    for n in range(minN, maxN + 1):

        laminae = []
        for a in range(1, n-1):
            for w in range(1, n-a):
                for b in range(1, n-1):
                    for h in range(1, n-b):
                        laminae.append((n, a, b, w, h))
        total = sumExpectedDistForSquareLaminaeOfSizeN(n)
        grandTotal += total
        logDebug()
        logInfo(f"N={n} -> {total:18.6f} -> {grandTotal:18.6f}")
        #logInfo(f"Running total for n from {minN} to {n}: {total}")
        logDebug()
        logDebug('-' * 50)
        logDebug()

    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logDebug(f"  Time spent: {timedelta(milliseconds=logTimeDiff)}")

    logDebug()
    logDebug('-' * 50)
    logDebug('-' * 50)
    logDebug()
    print(f"Grand total for n from {minN} to {maxN}: {total}")
    logDebug()

def doSomeExperimentation_equivalentKeys():
    n = 9
    (a, b) = (1, 2)
    (w, h) = (2, 3)
    equivalentLaminaKeys = [
        (n,     a,     b, w, h),
        (n,     a, n-b-h, w, h),
        (n, n-a-w,     b, w, h),
        (n, n-a-w, n-b-h, w, h),

        (n,     b,     a, h, w),
        (n, n-b-h,     a, h, w),
        (n,     b, n-a-w, h, w),
        (n, n-b-h, n-a-w, h, w),
    ]
    dd = dict()
    for k in equivalentLaminaKeys:
        dd[k] = expectedDistForSquareLamina(*k)
        print()

    for k in equivalentLaminaKeys:
        v = dd[k]
        print(f"{k} = {v}")

def doSomeExperimentation_breakIntoUnitSquares():
    """
    boundsToFreqMap = {
        ((0,1), (0,1), (0,1), (0,1)):  8,
        ((0,1), (0,1), (0,1), (1,2)): 16,
        ((0,1), (0,1), (0,1), (2,3)): 12,
        ((0,1), (0,1), (1,2), (1,2)):  8,
        ((0,1), (0,1), (1,2), (2,3)): 16,
        ((0,1), (0,1), (2,3), (2,3)):  4,
    }
    """

    grandTotal = 0
    for n in range(3, 40+1):
        laminae = []
        for a in range(1, n-1):
            for w in range(1, n-a):
                for b in range(1, n-1):
                    for h in range(1, n-b):
                        laminae.append((n, a, b, w, h))
        total = 0
        for lamina in laminae:
            logVerbose(f"lamina {lamina}")
            printLamina(*lamina)
            boundsToFreqMap = defaultdict(int)
            n, a, b, w, h = lamina
            for t in itertools.product(*itertools.repeat(range(n), 4)):
                x1, y1, x2, y2 = t
                if ((a <= x1 and x1 <  a+w) and (b <= y1 and y1 <  b+h)) or ((a <= x2 and x2 <  a+w) and (b <= y2 and y2 <  b+h)):
                    logVerbose(f"Skipping coors {(x1, y1), (x2, y2)}")
                    continue
                dx, dy = sorted([abs(x2-x1), abs(y2-y1)])
                bounds = ((0,1), (0,1), (dx, dx+1), (dy, dy+1))
                boundsToFreqMap[bounds] += 1

            e = 0
            for bounds, freq in sorted(boundsToFreqMap.items()):
                area = getPartial(*bounds)
                areaMultiplied = area * freq
                logVerbose(f"lamina {lamina}: {bounds} occurs {freq:>2} times -> {area:10.6f} -> {areaMultiplied:10.6f}")
                e += areaMultiplied

            areaSquare = n ** 2
            areaVoid = w * h
            valueToDivideBy = (areaSquare - areaVoid) ** 2
            inc = e / valueToDivideBy
            logVerbose(f"  lamina {lamina} -> {inc:10.6f}")
            total += inc

        testCase = None
        for t in TESTS:
            if t.N == n:
                testCase = t
                break
        if testCase:
            expected = testCase.expected
            ansStr = f"{total:.4f}"
            successStr = "SUCCESS" if (ansStr == expected) else f"FAILURE (expected {expected})"
            #logDebug(f"{n}: {ansStr} - {successStr}")
            logInfo(f"{n}: {ansStr} - {successStr}")

        grandTotal += total
        logInfo(f"N={n} -> {total:10.6f} -> {grandTotal:10.6f}")

    logInfo(f"Grand total: {grandTotal:10.6f}")

    return

def main():
    runMain()

    #doSomeExperimentation_equivalentKeys()
    #doSomeExperimentation_breakIntoUnitSquares()

# Main logic
if __name__ == '__main__':
    main()

