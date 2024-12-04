import re 

data = ''
with open('input', 'r') as file:
    data = file.read()

hor_lines = data.splitlines()
ver_lines = []
diag_lines = []
diag2_lines = []
sidelength = len(hor_lines[0])
numXmas = 0

# create verticals
for x in range(sidelength):
    line = ''
    for y in range(sidelength):
        line += hor_lines[y][x]
    ver_lines.append(line)

# create diagonals

# this only works because it's a square
for n in range(2*sidelength):
    shouldFlip = False
    width = n
    if width > sidelength:
        width = 2*sidelength - width
        shouldFlip = True

    line = ''
    for i in range(width):
        b = i
        a = sidelength - width + i

        if (shouldFlip):
            line += hor_lines[a][b]
        else:   
            line += hor_lines[b][a]

    diag_lines.append(line)

for n in range(2*sidelength):
    shouldFlip = False
    width = n
    if width > sidelength:
        width = 2*sidelength - width
        shouldFlip = True

    line = ''
    for i in range(width):
        b = i
        a = width - 1 - i

        if (shouldFlip):
            offset = sidelength - width
            b = offset + i
            a = sidelength - 1 - i

        line += hor_lines[b][a]

    diag2_lines.append(line)

# horizontal forward
for line in hor_lines:
    finds = re.findall('XMAS', line)
    numXmas += len(finds)

# horizontal backward
for line in hor_lines:
    finds = re.findall('SAMX', line)
    numXmas += len(finds)

# vertical down
for line in ver_lines:
    finds = re.findall('XMAS', line)
    numXmas += len(finds)

# vertical up
for line in ver_lines:
    finds = re.findall('SAMX', line)
    numXmas += len(finds)

# diag 1 forward
for line in diag_lines:
    finds = re.findall('XMAS', line)
    numXmas += len(finds)

# diag 1 backward
for line in diag_lines:
    finds = re.findall('SAMX', line)
    numXmas += len(finds)

# diag 2 forward
for line in diag2_lines:
    finds = re.findall('XMAS', line)
    numXmas += len(finds)

# diag 2 backward
for line in diag2_lines:
    finds = re.findall('SAMX', line)
    numXmas += len(finds)

print(numXmas)