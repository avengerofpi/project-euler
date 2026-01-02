#!/usr/bin/env python3

# Imports

# Functions

# Main logic
cont_frac = [2, 1]
k = 2
while len(cont_frac) < 100:
    cont_frac.extend([k, 1, 1])
    k += 2

print(cont_frac)
print(len(cont_frac))

convergents = [(2,1), (3,1)]
for v in cont_frac[2:]:
    n, d = v*convergents[-1][0] + convergents[-2][0], v*convergents[-1][1] + convergents[-2][1]
    convergents.append((n,d))
print(convergents[99])
print(sum(int(d) for d in str(convergents[99][0])))
