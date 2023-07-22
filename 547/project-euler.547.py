#!/usr/bin/python3

# Imports
from math import log, log2, log10, sqrt, gcd
import scipy
from datetime import timedelta
import time
from collections import defaultdict
import itertools

# Constants
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    TestCase(3, "1.6514"),
    TestCase(4, "19.6564"),
    #TestCase(5, "97.81334558787319"),
    #TestCase(6, "325.0072365326804"),
    #TestCase(7, "851.1947929255208"),
    #TestCase(8, "1903.386686792866"),
    #TestCase(9, "3801.6289566334553"),
    #TestCase(10, "6974.983978268594"),
    #TestCase(11, "11977.511213075131"),
    #TestCase(12, "19504.24783880133"),
    #TestCase(13, "30407.189289768656"),
    #TestCase(14, "45711.269791541185"),
    #TestCase(16, "94583.16151446037"),
    #TestCase(15, "66630.34280795284"),
    #TestCase(17, "131209.3592441513"),
    #TestCase(18, "178385.4299324293"),
    #TestCase(19, "238240.70852004984"),
    #TestCase(20, "313173.3514525104"),
    #TestCase(21, "405866.3169928597"),
    #TestCase(22, "519303.34561997105"),
    #TestCase(23, "656784.940706292"),

    #TestCase(40, "UNKNOWN"),
]

PARTIALS_TESTS = [
    TestCase(((0, 1), (0, 1), (0, 1), (0, 1)), "0.5214"), # unit square to itself
    TestCase(((1, 2), (1, 2), (1, 2), (1, 2)), "0.5214"), # unit square (shifted)
    TestCase(((0, 1), (0, 1), (1, 2), (0, 1)), "UNKNOWN"), # unit square to adjacent unit square (right)
    TestCase(((0, 1), (0, 1), (0, 1), (1, 2)), "UNKNOWN"), # unit square to adjacent unit square (up)
    TestCase(((0, 1), (0, 1), (1, 3), (0, 1)), "UNKNOWN"), # unit square to adjacent 2x square (right)
]

# Logging
info = True
debug = False
verbose = False
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

# Functions
def dist(x1, y1, x2, y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2 )

def ONE(a, b, c, d):
    return 1

# n = 3
# Use inclusion exclusion.
#   Include entire square
#     But this include cases where one or both points are in the void!
#             scipy.integrate.nquad(dist, [[0,3]    for i in range(4)])[0]
#   Exclude cases where one point is in the void for sure, other point is anywhere
#     But this removes the case of both points being in the void two times
#        -2 * scipy.integrate.nquad(dist, [[0,3], [0,3], [1,2], [1,2]])[0]
#   So add one copy of the case where both points are in the void back in
#           + scipy.integrate.nquad(dist, [[1,2]    for i in range(4)])[0]
# scipy.integrate.nquad(dist, [[0,3] for i in range(4)])[0] - 2 * scipy.integrate.nquad(dist, [[0,3], [0,3], [1,2], [1,2]])[0] + scipy.integrate.nquad(dist, [[1,2] for i in range(4)])[0]
# 105.68651664234636
# 105.68651664234636 / 64
# 1.651351822536662
# 1.6514 (Target)

def manualCaseFor3():
    expected3 = (\
          scipy.integrate.nquad(dist, [[0,3] for i in range(4)])[0] \
     -2 * scipy.integrate.nquad(dist, [[0,3], [0,3], [1,2], [1,2]])[0] \
        + scipy.integrate.nquad(dist, [[1,2] for i in range(4)])[0] \
    ) / 64
    logDebug(f"n = 3 (manual): {expected3}")

"""
There are three partials per lamina, three integrals to compute as part of an
inclusion-exclusion process to find the desired 'lamina-punctured integral.' They
are computed and combined as follows, where (a,b) is the coordinate of the lower
left corner of the removed rectangle, and (w,h) are the width and height of the
removed rectangle (respectively).
    valueToDivideBy = (\
          scipy.integrate.nquad(ONE, [[0,n]            for i in range(4)], opts=options)[0] \
     -2 * scipy.integrate.nquad(ONE, [[0,n],     [0,n], [a,a+w], [b,b+h]], opts=options)[0] \
        + scipy.integrate.nquad(ONE, [[a,a+w], [b,b+h], [a,a+w], [b,b+h]], opts=options)[0] \
    )

The memoizedPartials and getPartial method help to avoid duplicate computations.
"""
memoizedPartials = dict()
def getPartial(a, b, c, d):
    options = {
        "limit": 100,
        "epsabs": 1.49e-10
    }

    bounds = (a, b, c, d)
    v = 0
    logDebug(f"Computing partial for {bounds}")
    if bounds in memoizedPartials.keys():
        logVerbose(f"  Partial HAS been previously computed")
        v = memoizedPartials[bounds]
    else:
        logVerbose(f"  Partial has NOT been previously computed")
        #v = scipy.integrate.nquad(ONE, bounds, opts=options)[0]
        v = scipy.integrate.nquad(dist, bounds, opts=options)[0]
        memoizedPartials[bounds] = v
    logDebug(f"  Value: {v}")

    return v

"""
If one square lamina is a pure scaling of another square lamina, the expected
distance scales in exactly the same way. For example,
  xxx
  x x
  xxx
is a 2x scaling of
  xxxxxx
  xxxxxx
  xx  xx
  xx  xx
  xxxxxx
  xxxxxx
and so we can compute
    expectedDistForSquareLamina(6,2,2,2,2) = 2 * a
where
    a = expectedDistForSquareLamina(3,1,1,1,1)
"""
memoizedExpectedDistForSquareLamina = dict()
def expectedDistForSquareLamina(n, a, b, w, h):
    baseK = (n, a, b, w, h)
    logDebug(f"computing expectedDistForSquareLamina{baseK}")
    # Check if lamina is a scaled copy of a smaller lamina
    scale = gcd(n, gcd(a, gcd(b, gcd(w, h))))
    kScaled = tuple(v//scale for v in [n, a, b, w, h])
    logDebug(f"Maximum scale is {scale} -> {kScaled}")
    usedK = baseK
    if baseK in memoizedExpectedDistForSquareLamina.keys():
        expectedDist = memoizedExpectedDistForSquareLamina[baseK]
        logDebug(f"The value for {baseK} is known from previous computations")
    elif (scale > 1) and (kScaled in memoizedExpectedDistForSquareLamina.keys()):
        usedK = kScaled
        expectedDist = memoizedExpectedDistForSquareLamina[kScaled]
        logDebug(f"The value for {baseK} is known from previous computation of {kScaled}")
    else:
        areaSquare = n ** 2
        areaVoid = w * h
        valueToDivideBy = (areaSquare - areaVoid) ** 2

        #expectedDist = 1
        #"""
        expectedDist = (\
              getPartial((0,n),     (0,n),   (0,n),   (0,n)) \
         -2 * getPartial((0,n),     (0,n), (a,a+w), (b,b+h)) \
            + getPartial((a,a+w), (b,b+h), (a,a+w), (b,b+h)) \
        ) / valueToDivideBy
        #"""

    #logDebug(f"    valueToDivideBy:     {valueToDivideBy}")
    printLamina(n, a, b, w, h)
    logDebug(f"expectedDistForSquareLamina{baseK}: {expectedDist}")
    if baseK not in memoizedExpectedDistForSquareLamina.keys():
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
        logDebug(f"The following keys are quivalent:")
        for k in equivalentKeys:
            logDebug(f"  {k}")
            #printLamina(*k)
            memoizedExpectedDistForSquareLamina[k] = expectedDist
    logDebug()
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
        successStr = "SUCCESS" if (ansStr == expected) else f"FAILURE (expected {expected})"
        logDebug(f"{n}: {ansStr} - {successStr}")
    endTime = getTimeInMillis()
    logTimeDiff = endTime - startTime
    logDebug(f"  Time spent: {timedelta(milliseconds=logTimeDiff)} (for N = {n:>2})")
    return total

def testPartials():
    for test in PARTIALS_TESTS:
        bounds = test.N
        expected = test.expected

        total = getPartial(*bounds)

        ansStr = f"{total:.4f}"
        successStr = "SUCCESS" if (ansStr == expected) else f"FAILURE (expected {expected})"
        logDebug(f"{bounds}: {ansStr} - {successStr}")

def runMain():
    total = 0
    minN = 3
    maxN = 40
    #for n in range(minN, maxN + 1):
    startTime = getTimeInMillis()
    for n in [3]:
        total += sumExpectedDistForSquareLaminaeOfSizeN(n)
        logDebug()
        print(f"Running total for n from {minN} to {n}: {total}")
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

def doSomeExperimentation():
    a = expectedDistForSquareLamina(3,1,1,1,1)
    print(f"a x 1 = {a * 1}")
    print(f"a x 2 = {a * 2}")
    print(f"a x 3 = {a * 3}")
    print(f"a x 4 = {a * 4}")
    print()
    b = expectedDistForSquareLamina(6,2,2,2,2)
    print(f"a x 2 = {a * 2}")
    print(f"b x 1 = {b * 1}")
    print()
    c = expectedDistForSquareLamina(9,3,3,3,3)
    print(f"a x 3 = {a * 3}")
    print(f"c x 1 = {c * 1}")
    print()
    d = expectedDistForSquareLamina(12,4,4,4,4)
    print(f"a x 4 = {a * 4}")
    print(f"d x 1 = {d * 1}")
    print()

def doSomeExperimentation2():
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

def doSomeExperimentation3():
    """
    unitSquareE = getPartial(*unitSquareBounds)
    e = unitSquareE
    e= 0.5214054334972098
    e3 =(8*(e+0) +
        16*(e+1) +
        12*(e+2) +
         8*(e+sqrt(2)) +
        16*(e+sqrt(5)) +
         4*(e+sqrt(8))) / 64
    """
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

    """
    boundsToFreqMap = defaultdict(int)
    N = 3
    for t in itertools.product(range(N), range(N), range(N), range(N)):
        (x1, y1, x2, y2) = t
        #logInfo((x1, y1, x2, y2))
        c1 = (x1, y1)
        c2 = (x2, y2)
        if c1 == (1,1) or c2 == (1,1):
            #logInfo("  skipping")
            continue
        dx, dy = sorted([abs(x2-x1), abs(y2-y1)])
        bounds = ((0,1), (0,1), (dx, dx+1), (dy, dy+1))
        boundsToFreqMap[bounds] += 1
    """
    laminae = []
    n = 4
    total = 0
    for a in range(1, n-1):
        for w in range(1, n-a):
            for b in range(1, n-1):
                for h in range(1, n-b):
                    laminae.append((n, a, b, w, h))
                    #laminanae.append(n, a, b, w, h)
    for lamina in laminae:
        logDebug(f"lamina {lamina}")
        printLamina(*lamina)
        boundsToFreqMap = defaultdict(int)
        n, a, b, w, h = lamina
        for t in itertools.product(*itertools.repeat(range(n), 4)):
            x1, y1, x2, y2 = t
            #logInfo((x1, y1, x2, y2))
            if ((a <= x1 and x1 <  a+w) and (b <= y1 and y1 <  b+h)) or ((a <= x2 and x2 <  a+w) and (b <= y2 and y2 <  b+h)):
                logDebug(f"Skipping coors {(x1, y1), (x2, y2)}")
                continue
            dx, dy = sorted([abs(x2-x1), abs(y2-y1)])
            bounds = ((0,1), (0,1), (dx, dx+1), (dy, dy+1))
            boundsToFreqMap[bounds] += 1
        #logDebug(f"

        e = 0
        for bounds, freq in sorted(boundsToFreqMap.items()):
            area = getPartial(*bounds)
            areaMultiplied = area * freq
            logDebug(f"{bounds} occurs {freq:>2} times -> {area:10.6f} -> {areaMultiplied:10.6f}")
            e += areaMultiplied

        areaSquare = n ** 2
        areaVoid = w * h
        valueToDivideBy = (areaSquare - areaVoid) ** 2
        inc = e / valueToDivideBy
        logDebug(f"  lamina {lamina} -> {inc:10.6f}")
        total += inc
    #"""


    logInfo(f"N=3:")
    logInfo(f"Actual:   {total:10.6f}")
    logInfo(f"Expected: {19.6564}")
    return

def main():
    #runMain()
    #testPartials()

    #doSomeExperimentation2()
    doSomeExperimentation3()

# Main logic
if __name__ == '__main__':
    main()

