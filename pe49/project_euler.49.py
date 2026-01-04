#!/usr/bin/env python3

# Imports

# Functions

# Main logic
from collections import defaultdict
from ..primes.generate_primes import primes_up_to_10k

primes = primes_up_to_10k()
primes = [p for p in primes if p > 1000 and p < 10000]

freq = defaultdict(list)
for p in primes:
    freq[''.join(sorted(c for c in str(p)))].append(p)
for s, pp in freq.items():
    if len(pp) >= 3:
        for p1 in pp:
            for p2 in pp:
                if p1 >= p2:
                    continue
                if (diff := p2 - p1) and (p3 := p2 + diff) and p3 in pp:
                    print(f"{p1}, {p2}, {p3} (diff={diff}-> {p1}{p2}{p3}")
