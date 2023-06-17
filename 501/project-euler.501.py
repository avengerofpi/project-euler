#!/usr/bin/python3

# Imports
from math import log, log10, prod, sqrt
from collections import defaultdict

# Constants
debug = True
class TestCase:
    def __init__(self, N, expected):
        self.N = N
        self.expected = expected

TESTS = [
    TestCase(100, 10),
    TestCase(1000, 180),
    #TestCase(10 ** 6, 224427),
    #TestCase(10 ** 12, "UNKNOWN"),
]

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

# Main logic
def main():
    for test in TESTS:
        N = test.N
        expected = test.expected

        print(f"Running against N = {N}", flush=True)
        primeBound = N // 2
        primes = computePrimesUpToN(primeBound)
        logDebug(f"  Computing primes up to {primeBound} - found {len(primes)} from {primes[0]} to {primes[-1]}")

        #numP = len(primes)
        #for ip in range(nP):
        #    p = primes[ip]
        p7List = []
        p3qList = []
        pqrList = []
        for p in primes:
            p7 = p ** 7
            if p7 <= N:
                p7List.append((p, p7))
            p3 = p ** 3
            for q in primes:
                if p == q:
                    continue
                p3q = p3 * q
                if p3q <= N:
                    p3qList.append((p,q,p3q))
                #else:
                #    break

                if p < q:
                    pq = p * q
                    for r in primes:
                        if q < r:
                            pqr = pq * r
                            if pqr <= N:
                                pqrList.append((p,q,r, pqr))
                            #else:
                            #    break

        logDebug(f"  Found {len(p7List)} numbers of the form p**7")
        #for (p,p7) in p7List:
        #    logDebug(f"    {p:4}**7= {p7:8}")
        logDebug(f"  Found {len(p3qList)} numbers of the form p**3 * q")
        #for (p,q,p3q) in p3qList:
        #    logDebug(f"    {p:4}**3 * {q:4} = {p3q:8}")
        logDebug(f"  Found {len(pqrList)} numbers of the form p * q * r")
        #for (p,q,r, pqr) in pqrList:
        #    logDebug(f"    {p:4} * {q:4} * {r:4} = {pqr:8}")
        ans = len(p7List) + len(p3qList) + len(pqrList)
        successStr = "SUCCESS" if (ans == expected) else f"FAILURE (expected {expected})"
        print(f"{N}: {ans} - {successStr}", flush=True)
        print("", flush=True)


# Main logic
if __name__ == '__main__':
    main()
