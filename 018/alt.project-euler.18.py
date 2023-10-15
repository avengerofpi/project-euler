#!/usr/bin/python3

# Imports
from copy import deepcopy
from colorama import Fore, Back, Style
#print(f"{Fore.GREEN}hello{Fore.RED}World{ansi.Style.RESET_ALL}")

# Constants
T = [
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
PATH_IGNORE_CHAR = '-'

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

def printTriangleWithColor(t, pathT):
    PATH_COLOR = Fore.RED
    RESET_COLOR = Style.RESET_ALL

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
            if pathT[rowI][colI] != PATH_IGNORE_CHAR:
                s += PATH_COLOR
            s += f"{entry:{w}}" + emptyEntry
            s += RESET_COLOR
        # Last entry
        if pathT[rowI][-1] != PATH_IGNORE_CHAR:
            s += PATH_COLOR
        s += f"{row[-1]}"
        s += RESET_COLOR
        # End padding
        s += padding
        print(s)

def findMaximalPath(inputT):
    t = deepcopy(inputT)
    n = len(t)
    orderT = list(list(0 for j in range(i+1)) for i in range(n))
    for rowI in range(n-2, -1, -1):
        row = t[rowI]
        rowBelow = t[rowI + 1]
        orderRow = list()
        for colI in range(len(row)):
            v = row[colI]
            vLeft = rowBelow[colI]
            vRight = rowBelow[colI + 1]
            if vLeft >= vRight:
                row[colI] = v + vLeft
                orderRow.append(0)
            else:
                row[colI] = v + vRight
                orderRow.append(1)
        orderT[rowI] = orderRow
    printTriangle(t)
    printTriangle(orderT)
    # Construct the triangle with the maximal path highlighted
    pathT = deepcopy(inputT)
    i = orderT[0][0]
    for rowI in range(1, n):
        pathRow = [PATH_IGNORE_CHAR for j in range(rowI + 1)]
        orderRow = orderT[rowI]
        #print(f"i: {i}")
        #print(f"rowI: {rowI}")
        pathRow[i] = inputT[rowI][i]
        pathT[rowI] = pathRow
        i += orderRow[i]
    printTriangle(pathT)
    printTriangleWithColor(inputT, pathT)


def main():
    # Main logic
    printTriangle(T)
    findMaximalPath(T)

if __name__ == "__main__":
    main()
