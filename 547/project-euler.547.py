#!/usr/bin/python3

# Imports
from math import log, log2, log10, sqrt
import scipy

# Constants
debug = True

# Functions
def logDebug(msg):
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

def manualCaseFor3():
    expected3 = (\
          scipy.integrate.nquad(dist, [[0,3] for i in range(4)])[0] \
     -2 * scipy.integrate.nquad(dist, [[0,3], [0,3], [1,2], [1,2]])[0] \
        + scipy.integrate.nquad(dist, [[1,2] for i in range(4)])[0] \
    ) / 64
    print(f"n = 3 (manual): {expected3}")

def expectedDistForSquareLamina(n, a, b, w, h):
    options = {
        "limit": 100,
        "epsabs": 1.49e-10
    }
    areaSquare = n ** 2
    areaVoid = w * h
    valueToDivideBy = (areaSquare - areaVoid) ** 2

    """
    valueToDivideBy = (\
          scipy.integrate.nquad(ONE, [[0,n]            for i in range(4)], opts=options)[0] \
     -2 * scipy.integrate.nquad(ONE, [[0,n],     [0,n], [a,a+w], [b,b+h]], opts=options)[0] \
        + scipy.integrate.nquad(ONE, [[a,a+w], [b,b+h], [a,a+w], [b,b+h]], opts=options)[0] \
    )
    """

    expected = (\
          scipy.integrate.nquad(dist, [[0,n]            for i in range(4)], opts=options)[0] \
     -2 * scipy.integrate.nquad(dist, [[0,n],     [0,n], [a,a+w], [b,b+h]], opts=options)[0] \
        + scipy.integrate.nquad(dist, [[a,a+w], [b,b+h], [a,a+w], [b,b+h]], opts=options)[0] \
    ) / valueToDivideBy

    print(f"expectedDistForSquareLamina({n}, {a}, {b}, {w}, {h}):")
    #print(f"  valueToDivideBy:     {valueToDivideBy}")
    printLamina(n, a, b, w, h)
    print(f"  {expected}")
    print()
    return expected

def sumExpectedDistForSquareLaminaeOfSizeN(n):
    total = 0
    for a in range(1, n-1):
        for w in range(1, n-a):
            for b in range(1, n-1):
                for h in range(1, n-b):
                    total += expectedDistForSquareLamina(n, a, b, w, h)
    print(f"Total for n = {n}: {total}")
    print()
    print('-' * 50)
    print()
    return total

def main():
    total = 0
    minN = 3
    maxN = 40
    for n in range(minN, maxN + 1):
        total += sumExpectedDistForSquareLaminaeOfSizeN(n)
    print(f"Grand total for n from {minN} to {maxN}: {total}")

# Main logic
if __name__ == '__main__':
    main()

