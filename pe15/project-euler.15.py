#!/usr/bin/env python3

from collections import defaultdict

memo = defaultdict(int)
def paths(a, b):
    n = 0
    if a == 0 or b == 0:
        return 1
    for k in [(a-1, b), (a, b-1)]:
        if memo[k]:
            n += memo[k]
        else:
            n += paths(*k)
    memo[(a, b)] = n
    memo[(b, a)] = n
    return n

print(paths(20,20))
