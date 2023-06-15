#!/usr/bin/python3

# Imports
from math import log, log2, log10, sqrt, gcd
import scipy

# Constants
debug = True
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    TestCase(3, "1.6514"),
    TestCase(4, "19.6564"),
    #TestCase(5, "UNKNOWN"),
    #TestCase(40, "UNKNOWN"),
]


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

    k = (a, b, c, d)
    v = 0
    logDebug(f"Computing partial for {k}")
    if k in memoizedPartials.keys():
        logDebug(f"  Partial HAS been previously computed")
        v = memoizedPartials[k]
    else:
        logDebug(f"  Partial has NOT been previously computed")
        v = scipy.integrate.nquad(dist, k, opts=options)[0]
        memoizedPartials[k] = v
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
    # Check if lamina is a scaled copy of a smaller lamina
    scale = gcd(n, gcd(a, gcd(b, gcd(w, h))))
    kScaled = (v//2 for v in [n, a, b, w, h])
    if kScaled in memoizedExpectedDistForSquareLamina.keys():
        expectedDist = memoizedExpectedDistForSquareLamina[kScaled]
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

    printLamina(n, a, b, w, h)
    print(f"expectedDistForSquareLamina({n}, {a}, {b}, {w}, {h}): {expectedDist}")
    baseK = (n, a, b, w, h)
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
        print(f"The following keys are quivalent:")
        for k in equivalentKeys:
            print(f"  {k}")
            printLamina(*k)
            memoizedExpectedDistForSquareLamina[k] = expectedDist
    print()
    return expectedDist

def sumExpectedDistForSquareLaminaeOfSizeN(n):
    print(f"sumExpectedDistForSquareLaminaeOfSizeN({n})")
    total = 0
    for a in range(1, n-1):
        for w in range(1, n-a):
            for b in range(1, n-1):
                for h in range(1, n-b):
                    total += expectedDistForSquareLamina(n, a, b, w, h)
    print(f"SubTotal for N = {n:>2}: {total}")
    testCase = None
    for t in TESTS:
        if t.N == n:
            testCase = t
            break
    if testCase:
        expected = testCase.expected
        ansStr = f"{total:.4f}"
        successStr = "SUCCESS" if (ansStr == expected) else f"FAILURE (expected {expected})"
        print(f"{n}: {ansStr} - {successStr}", flush=True)
    print()
    print('-' * 50)
    print()
    return total

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

def main():
    total = 0
    minN = 3
    maxN = 6
    for n in range(minN, maxN + 1):
        total += sumExpectedDistForSquareLaminaeOfSizeN(n)
    print()
    print(f"Grand total for n from {minN} to {maxN}: {total}")

    #doSomeExperimentation2()

# Main logic
if __name__ == '__main__':
    main()

