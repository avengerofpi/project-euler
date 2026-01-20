#!/usr/bin/env python3

# Imports

# Functions

# Main logic
m = 0
for a in range(1, 100):
    for b in range(1, 100):
        n = a**b
        s = sum(int(c) for c in str(n))
        m = max(m, s)
print(f"max: {m}")
