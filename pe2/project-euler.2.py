#!/usr/bin/env python3

# Imports

# Constants
N = 4 * 1000 * 1000

# Functions

# Main logic
def main():
    a = 1
    b = 1
    s = 0
    while b < N:
        if b % 2 == 0:
            print(b)
            s += b
        tmp = b
        b += a
        a = tmp
    print(s)

if __name__ == "__main__":
    main()
