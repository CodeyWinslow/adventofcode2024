from dataclasses import dataclass

data = []
with open('test2', 'r') as file:
    data = file.readlines()
height = len(data)
width = len(data[1].strip())

def in_range(pos):
    x = pos[0]
    y = pos[1]
    return x >= 0 and x < width and y >= 0 and y < height

def floodRegion(pos, flower, visited, region, edges, edgePositions):
    if pos in visited:
        if data[pos[1]][pos[0]] == flower:
            return edges
        return edges + 1

    if not in_range(pos):
        return edges + 1

    thisFlower = data[pos[1]][pos[0]]
    if thisFlower is not flower:
        return edges + 1

    visited.add(pos)
    region.append(pos)

    up = (pos[0], pos[1]-1)
    down = (pos[0], pos[1]+1)
    left = (pos[0]-1, pos[1])
    right = (pos[0]+1, pos[1])

    dirs = [up, right, down, left]

    prevEdges = edges
    for dir in dirs:
        edges = floodRegion(dir, flower, visited, region, edges, edgePositions)
    
    if prevEdges != edges:
        edgePositions.add(pos)
    
    return edges

def get_bounds(points):
    p1 = (1000000, 1000000)
    p2 = (-1, -1)

    # bounds
    for pos in points:
        x = pos[0]
        y = pos[1]
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        if x < x1:
            p1 = (x, p1[1])
        elif x > x2:
            p2 = (x, p2[1])
        
        if y < y1:
            p1 = (p1[0], y)
        elif y > y2:
            p2 = (p2[0], y)

    return (p1, p2)

def is_adjacent(pos, otherPos):
    x1 = pos[0]
    y1 = pos[1]
    x2 = otherPos[0]
    y2 = otherPos[1]
    return (
        x1 - 1 == x2
        or x1 + 1 == x2
        or y1 - 1 == y2
        or y1 + 1 == y2
    )

def get_cell_to_right(pos, dir):
    match dir:
        case 0:#right
            return (pos[0], pos[1] + 1)
        case 1:#down
            return (pos[0] - 1, pos[1])
        case 2:#left
            return (pos[0], pos[1] - 1)
        case 3:#up
            return (pos[0] + 1, pos[1])

def get_next_cell(pos, dir):
    match dir:
        case 0:#right
            return (pos[0] + 1, pos[1])
        case 1:#down
            return (pos[0], pos[1] + 1)
        case 2:#left
            return (pos[0] - 1, pos[1])
        case 3:#up
            return (pos[0], pos[1] - 1)

def turn_left(dir):
    if dir == 0:
        return 3
    return dir - 1

def turn_right(dir):
    return (dir + 1) % 4

def generate_sides(startPos, region):
    sides = []
    #start above starting position
    startPos = (startPos[0], startPos[1]-1)
    currentSide = [startPos]
    dir = 0 # right, clockwise 4 directions

    curPos = get_next_cell(startPos, dir)

    # surrounding
    while curPos != startPos:
        nextPos = get_next_cell(curPos, dir)
        rightPos = get_cell_to_right(curPos, dir)
        # if cell is to the right, record
        if rightPos in region:
            currentSide.append(curPos)

            # if cell is in front, turn left
            # commit side, start new one
            if nextPos in region:
                sides.append(currentSide)
                currentSide = []
                dir = turn_left(dir)
            # otherwise, move forward
            else:
                curPos = nextPos

        # otherwise, turn right
        # move forward
        # commit side, start new one
        else:
            sides.append(currentSide)
            currentSide = []
            dir = turn_right(dir)
            curPos = get_next_cell(curPos, dir)
            
    # find holes
    
    return len(sides)


def main():
    visited = set()
    regions = []
    perimeters = []
    while True:
        anyUnvisited = False
        for y in range(height):
            for x in range(width):
                if (x,y) not in visited:
                    anyUnvisited = True
                    newRegion = []
                    newFlower = data[y][x]
                    edges = floodRegion((x,y), newFlower, visited, newRegion, 0)
                    regions.append(newRegion)
                    perimeters.append(edges)

        if not anyUnvisited:
            break

    areas = []
    for region in regions:
        areas.append(len(region))

    cost = 0
    for i in range(len(areas)):
        area = areas[i]
        perim = perimeters[i]
        cost += area * perim
    print(cost)

def main2():
    visited = set()
    regions = []
    perimeters = []
    sides = []
    while True:
        anyUnvisited = False
        for y in range(height):
            for x in range(width):
                if (x,y) not in visited:
                    anyUnvisited = True
                    newRegion = []
                    newFlower = data[y][x]
                    edgePositions = set()
                    edges = floodRegion((x,y), newFlower, visited, newRegion, 0, edgePositions)
                    sides.append(generate_sides((x,y), newRegion))
                    regions.append(newRegion)
                    perimeters.append(edges)

        if not anyUnvisited:
            break

    areas = []
    for region in regions:
        areas.append(len(region))
    
    cost = 0
    for i in range(len(areas)):
        area = areas[i]
        side = sides[i]
        cost += area * side
    print(cost)

main2()