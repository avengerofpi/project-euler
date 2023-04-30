#!/usr/bin/python3

# Imports

# Constants
N = 1 * 1000 * 1000 * 1000

# Functions
def computePrimesUpToN(N):
    """
    Inefficiently determine all primes up to (and including) the input
    value `N`, returning the collection as a numerically-sorted tuple.

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
                print(f"{candidateP}")
    return tuple(primes)

# Main logic
def main():
    computePrimesUpToN(N)

if __name__ == "__main__":
    main()
