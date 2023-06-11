#!/usr/bin/python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict
import scipy
from numpy import array
from time import sleep

# Constants
debug = False
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    TestCase(2800, "715.019337")
] + [ TestCase(N, "UNKNOWN") for N in range(830000, 10 ** 6, 10000) ]

# Functions
def logDebug(msg = ""):
    if debug:
        print(msg, flush=True)

def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as some collection object.

    This is a simple seive generator, nothing fancy.
    """
    primes = []
    checkPrimesI = 0
    if N >= 2:
        primes.append(2)
        for candidateP in range(3, N+1, 2):
            while ((checkPrimesI < len(primes) - 1) and (primes[checkPrimesI + 1] ** 2 <= candidateP)):
                checkPrimesI += 1
            if all(candidateP % p != 0 for p in primes[0:checkPrimesI + 1]):
                primes.append(candidateP)
                #print(f"{candidateP}", flush=True)
    return tuple(primes)

def filterByUnitsDigitAndSort(arr, digit):
    return sorted(n for n in arr if n % 10 == digit)

def getPrimesToIncludeMap(primesA, primesB, N):
    modA = primesA[0] % 10
    width = int(log10(sqrt(N))) + 1

    logDebug(f"Checking primes ending in {modA}:")
    pAsToIncludeMap = dict()
    for pA in primesA:
        primesBCofactors = []
        for pB in primesB:
            if (pA < pB) and (pA * pB <= N):
                primesBCofactors.append(pB)
        pAsToIncludeMap[pA] = primesBCofactors

        # Logging
        if len(primesBCofactors) > 0:
            msg = f"  {pA:{width}} (because of "
            termsStart = 4
            termsEnd = 2
            if len(primesBCofactors) > termsStart + termsEnd:
                primesBprefix = primesBCofactors[0:termsStart]
                primesBsuffix = primesBCofactors[-termsEnd:]
                msg += f"{primesBprefix} ... {primesBsuffix}"
            else:
                msg += f"{primesBCofactors}"
            msg += f" ({len(primesBCofactors)}))"
            logDebug(msg)


    return pAsToIncludeMap

# Main logic
def main():
    #for N in (40, 2800, 10 ** 6):
    #for N in (40, 2800):
    for test in TESTS:
        #N = 40
        N = test.N
        expected = test.expected
        print(f"Running against N = {N}", flush=True)

        primes = computePrimesUpToN(N)
        p3s = filterByUnitsDigitAndSort(primes, 3)
        p7s = filterByUnitsDigitAndSort(primes, 7)
        p9s = filterByUnitsDigitAndSort(primes, 9)

        # All primes ending in 3 need to be factors
        valuesToMultiply = sorted(p3s)

        # All remaining factors end in either 7 or 9. In order for a prime `p7`
        # that ends in 7 to be included, it is necessary but not necessarily
        # sufficient for there to be prime `p9` that ends in 9 satisfying
        #   p7 * p9 <= N.
        # Similarly, in order for a prime `p9` that ends in 9 to be included,
        # it is necessary but not sufficient for there to be prime `p7` that
        # ends in 7 satisfying
        #   p7 * p9 <= N.
        p7sToIncludeMap = getPrimesToIncludeMap(p7s, p9s, N)
        p9sToIncludeMap = getPrimesToIncludeMap(p9s, p7s, N)

        # Setup linear program stuff
        primeLogs = { p: log(p) for p in primes }

        p79s = p7s + p9s
        primeIndices = { p79s[i]: i for i in range(len(p79s)) }

        cost = [log(p) for p in p79s]
        #cost = array([log(p) for p in p79s])
        #lowerBound = [0 for p79 in p79s]
        #upperBound = [1 for p79 in p79s]
        bounds = [[0,1] for p79 in p79s]
        #bounds = array([[0,1] for p79 in p79s])

        p79sToCofactorsMap = dict()
        p79sToCofactorsMap.update(p7sToIncludeMap)
        p79sToCofactorsMap.update(p9sToIncludeMap)

        A_ub = []
        b_ub = []
        logDebug(f"Building A_ub and b_ub")
        for p in p79s:
            pI = primeIndices[p]
            cofactors = p79sToCofactorsMap[p]
            if len(cofactors):
                logDebug(f"  Processing {p}: {cofactors}")
            for cofactor in cofactors:
                cofactorI = primeIndices[cofactor]
                A_ub_row = [0 for p79 in p79s]
                A_ub_row[pI] = -1
                A_ub_row[cofactorI] = -1
                A_ub.append(A_ub_row)
                b_ub.append(-1)
        #A_ub = array(A_ub)
        #b_ub = array(b_ub)

        # Logging
        print(f"A_ub is a {len(A_ub)} x {len(b_ub)} matrix", flush=True)
        logDebug(f"A_ub:")
        for row in A_ub:
          logDebug(f"  {row}")
        logDebug(f"b_ub: {b_ub}")

        sqrtN = sqrt(N)
        xInit = [1 if p79 < sqrt(N) else 0 for p79 in p79s]

        # Run linear program
        """
        scipy.optimize.linprog(
            c,
            A_ub=None, b_ub=None,
            A_eq=None, b_eq=None,
            bounds=None,
            method='highs',
            callback=None,
            options=None,
            x0=None,
            integrality=None
        )
        """
        #result = scipy.optimize.linprog(cost, A_ub=A_ub, b_ub=b_ub, bounds=bounds, integrality=1, method='revised simplex', x0=xInit)
        sleep(5)
        result = scipy.optimize.linprog(cost, A_ub=A_ub, b_ub=b_ub, bounds=bounds, integrality=1, method='highs')
        minCost = result.fun
        x = result.x
        print("Solution:", flush=True)
        xP7s = [p for p in p7s if x[primeIndices[p]]]
        xP9s = [p for p in p9s if x[primeIndices[p]]]
        print(f"  p3s: ALL", flush=True)
        print(f"  p7s: {xP7s}", flush=True)
        print(f"  p9s: {xP9s}", flush=True)


        # Finish calculating solution
        product = prod(valuesToMultiply)
        #ans = log(product)
        ans = minCost + log(product)
        ansStr = f"{ans:.6f}"
        successStr = "SUCCESS" if (ansStr == expected) else f"FAILURE (expected {expected})"
        print(f"{N}: {ansStr} - {successStr}", flush=True)
        print("", flush=True)
        #logDebug()

# Main logic
if __name__ == '__main__':
    main()
