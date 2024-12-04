import re 

data = ''
with open('input', 'r') as file:
    data = file.read()
hor_lines = data.splitlines()
dim = len(hor_lines[0])


def hasPattern(x, y):
    # don't check center because it must be A
    if x == 0 or x == dim - 1:
        return False
    if y == 0 or y == dim - 1:
        return False
    
    TL = hor_lines[y-1][x-1]
    TR = hor_lines[y-1][x+1]
    BL = hor_lines[y+1][x-1]
    BR = hor_lines[y+1][x+1]

    hasDiag1 = False
    hasDiag2 = False
    if TL == 'M' and BR == 'S' or TL == 'S' and BR == 'M':
        hasDiag1 = True
    if TR == 'M' and BL == 'S' or TR == 'S' and BL == 'M':
        hasDiag2 = True

    return hasDiag1 and hasDiag2

numPatterns = 0
for y in range(dim):
    for x in range(dim):
        char = hor_lines[y][x]
        if char == 'A' and hasPattern(x, y):
            numPatterns += 1

print(numPatterns)