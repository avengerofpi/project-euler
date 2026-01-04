#!/usr/bin/env python3

# Imports

# Constants
N = 1000
a = 3
b = 5

# Functions

# Main logic
def main():
    #s = sum(i for i in range(N) if ((i % a == 0) or (i % b == 0)))
    s = sum(range(0,N,a)) + sum(range(0,N,b)) - sum(range(0,N,a*b))
    print(s)

if __name__ == "__main__":
    main()
