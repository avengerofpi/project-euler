#!/usr/bin/python3

# Imports
from math import log, log2, log10, sqrt
import scipy

# Constants
debug = True
SCIPY_INT_OPTS = {
    "limit": 100,
    "epsabs": 1.49e-10
}

# Functions
def logDebug(msg = ""):
    if debug:
        print(msg)

def printLamina(n, a, b, w, h):
    INDENT = '  '
    X = 'x'
    VOID = ' '
    FULL_LINE = X*n
    VOID_LINE = X*a + VOID*w + X*(n-a-w)
    # Top rows until void starts
    for r in range(n, b+h, -1):
        print(INDENT + FULL_LINE)
    # Print rows with void portion
    for r in range(b+h, b, -1):
        print(INDENT + VOID_LINE)
    # Bottom rows after void
    for r in range(b, 0, -1):
        print(INDENT + FULL_LINE)

def dist(x1, y1, x2, y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2 )

def ONE(a, b, c, d):
    return 1

#def expectedDist(w, h):
#    return (v / ((w * h) ** 2) for v in scipy.integrate.nquad(dist, [[0, w], [0, h], [0, w], [0, h]]))

#def expectedDist(w, h):
#    return tuple(v / ((w * h) ** 2) for v in scipy.integrate.nquad(dist, [[0, w], [0, h], [0, w], [0, h]]))

# expectedDist(1, 1)
#  (0.5214054334820506, 1.4893564525019662e-08)

# expectedDist(2, 3)
# (1.317067450706075, 1.7435003632186453e-08)

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

# 1.651351822536662
# 1.6513518225368988

def manualCaseFor3():
    expected3 = (\
          scipy.integrate.nquad(dist, [[0,3] for i in range(4)])[0] \
     -2 * scipy.integrate.nquad(dist, [[0,3], [0,3], [1,2], [1,2]])[0] \
        + scipy.integrate.nquad(dist, [[1,2] for i in range(4)])[0] \
    ) / 64
    print(f"n = 3 (manual): {expected3}")


def expectedDistForSquareLamina(n, a, b, w, h):
    areaSquare = n ** 2
    areaVoid = w * h
    valueToDivideBy = (areaSquare - areaVoid) ** 2

    """
    valueToDivideBy = (\
          scipy.integrate.nquad(ONE, [[0,n]            for i in range(4)], opts=SCIPY_INT_OPTS)[0] \
     -2 * scipy.integrate.nquad(ONE, [[0,n],     [0,n], [a,a+w], [b,b+h]], opts=SCIPY_INT_OPTS)[0] \
        + scipy.integrate.nquad(ONE, [[a,a+w], [b,b+h], [a,a+w], [b,b+h]], opts=SCIPY_INT_OPTS)[0] \
    )
    """

    expectedDist = (\
          scipy.integrate.nquad(dist, [[0,n]            for i in range(4)], opts=SCIPY_INT_OPTS)[0] \
     -2 * scipy.integrate.nquad(dist, [[0,n],     [0,n], [a,a+w], [b,b+h]], opts=SCIPY_INT_OPTS)[0] \
        + scipy.integrate.nquad(dist, [[a,a+w], [b,b+h], [a,a+w], [b,b+h]], opts=SCIPY_INT_OPTS)[0] \
    ) / valueToDivideBy

    print(f"expectedDistForSquareLamina({n}, {a}, {b}, {w}, {h}):")
    #print(f"  valueToDivideBy:     {valueToDivideBy}")
    printLamina(n, a, b, w, h)
    print(f"{expectedDist}")
    print()
    return expectedDist

def computeFullSquarePart(n):
    return scipy.integrate.nquad(dist, [[0,n] for i in range(4)], opts=SCIPY_INT_OPTS)[0]

def computeBaseDict(n):
    logDebug(f"computeBaseDict({n})")
    baseDict = dict()
    for a in range(1, n-1):
        for b in range(1, n-1):
            v = scipy.integrate.nquad(dist, [[0,n], [0,n], [a,a+1], [b,b+1]], opts=SCIPY_INT_OPTS)[0]
            baseDict[(a, b)] = v
            logDebug(f"  ({a}, {b}) = {v:10.6f}")
    return baseDict
    
def expectedDistForSquareLaminaUsingBaseDict(baseDict, fullSquare, n, a, b, w, h):
    areaSquare = n ** 2
    areaVoid = w * h
    valueToDivideBy = (areaSquare - areaVoid) ** 2

    logDebug(f"expectedDistForSquareLaminaUsingBaseDict(baseDict, fullSquare, {n}, {a}, {b}, {w}, {h}):")
    logDebug(f"  fullSquare:      {fullSquare:10.6f}")

    voidPart = sum(baseDict[(a+ai, b+bi)] for ai in range(w) for bi in range(h))
    expectedDist = (fullSquare - voidPart) / valueToDivideBy

    logDebug(f"  voidPart:        {voidPart}")
    logDebug(f"  valueToDivideBy: {valueToDivideBy}")
    printLamina(n, a, b, w, h)
    logDebug(f"{expectedDist:10.6f} = ({fullSquare:10.6f} - {voidPart:10.6f}) / {valueToDivideBy})")
    logDebug()
    return expectedDist

def sumExpectedDistForSquareLaminaeOfSizeN(n):
    print(f"sumExpectedDistForSquareLaminaeOfSizeN({n})")
    # Compute non-normalized contributions to expected distance for the entire
    # square and for each 1x1 (single-block) lamina. Then the expected distance
    # for the larger lamina can be computed from these without needing to
    # perform the computationally intensive integrals again and again
    # (memoization/dynamic programming).
    fullSquare = computeFullSquarePart(n)
    baseDict = computeBaseDict(n)
    total = 0
    for a in range(1, n-1):
        for w in range(1, n-a):
            for b in range(1, n-1):
                for h in range(1, n-b):
                    #total += expectedDistForSquareLamina(n, a, b, w, h, baseDict)
                    total += expectedDistForSquareLaminaUsingBaseDict(baseDict, fullSquare, n, a, b, w, h)
    print(f"SubTotal: {total}")
    print()
    print('-' * 50)
    print()
    return total

def main():
    total = 0
    minN = 3
    maxN = 4
    for n in range(minN, maxN + 1):
        total += sumExpectedDistForSquareLaminaeOfSizeN(n)
    print(f"Grand total for n from {minN} to {maxN}: {total}")

# Main logic
if __name__ == '__main__':
    main()

