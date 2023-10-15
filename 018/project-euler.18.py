#!/usr/bin/python3

# Imports
t = [
    [75],
    [95, 64],
    [17, 47, 82],
    [18, 35, 87, 10],
    [20,  4, 82, 47, 65],
    [19,  1, 23, 75,  3, 34],
    [88,  2, 77, 73,  7, 63, 67],
    [99, 65,  4, 28,  6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
    [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
    [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
    [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
    [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
    [ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23]
]

# Functions
def printTriangle(t):
    n = len(t)
    w = max(len(str(v)) for row in t for v in row)
    nn = 2*n - 1
    ww = w + 0
    emptyEntry = " " * ww
    for rowI in range(n):
        row = t[rowI]
        padding = emptyEntry * (n - rowI - 1)
        s = str(padding)
        # All but last entry for current row
        for colI in range(rowI):
            entry = row[colI]
            s += f"{entry:{w}}" + emptyEntry
        # Last entry
        s += f"{row[-1]}"
        # End padding
        s += padding
        print(s)

# Main logic
for rowIndex in range(1, len(t)):
    prevRow = t[rowIndex - 1]
    currRow = t[rowIndex]
    # Left entry
    currRow[0] += prevRow[0]
    # Middle entries
    for colIndex in range(1,len(currRow)-1):
        currRow[colIndex] += max(prevRow[colIndex-1], prevRow[colIndex])
        #print(currRow)
    # Last entry
    currRow[-1] += prevRow[-1]

printTriangle(t)
print(max(t[-1]))
