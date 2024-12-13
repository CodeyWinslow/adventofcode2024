from dataclasses import dataclass
from enum import Enum

data = []
with open('input', 'r') as file:
    data = file.readlines()
height = len(data)
width = len(data[1].strip())

class WallDirection(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

@dataclass
class RegionWall:
    Direction = WallDirection.TOP
    Position = None

def in_range(pos):
    x = pos[0]
    y = pos[1]
    return x >= 0 and x < width and y >= 0 and y < height

def is_wall_at_position(pos, walls):
    for wall in walls:
        if wall.Position == pos:
            return True
    return False

haveOutput = False
def debug_output_walls(walls):
    if haveOutput:
        return
    
    with open('output', 'w') as file:
        for y in range(height):
            line = ''
            for x in range(width):
                if is_wall_at_position((x,y),walls):
                    line += 'X'
                else:
                    line += ' '
            line += '\n'
            file.write(line)

def floodRegion(pos, flower, visited, region, edges):
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

    for dir in dirs:
        edges = floodRegion(dir, flower, visited, region, edges)

    return edges

def floodRegion2(pos, flower, visited, region, edges):
    if pos in visited:
        if data[pos[1]][pos[0]] == flower:
            return False
        return True

    if not in_range(pos):
        return True

    thisFlower = data[pos[1]][pos[0]]
    if thisFlower is not flower:
        return True

    visited.add(pos)
    region.append(pos)

    up = (pos[0], pos[1]-1)
    down = (pos[0], pos[1]+1)
    left = (pos[0]-1, pos[1])
    right = (pos[0]+1, pos[1])

    dirs = [up, right, down, left]

    for dir in dirs:
        if floodRegion2(dir, flower, visited, region, edges):
            # we ran into an edge
            direction = WallDirection.TOP
            if dir == right:
                direction = WallDirection.RIGHT
            elif dir == down:
                direction = WallDirection.BOTTOM
            elif dir == left:
                direction = WallDirection.LEFT
            wall = RegionWall()
            wall.Direction = direction
            wall.Position = pos
            edges.append(wall)

    
    return False

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

def sort_by_x(item):
    return item.Position[0]

def sort_by_y(item):
    return item.Position[1]

def count_sides_horizontal(walls):
    wallsByY = []
    for y in range(height):
        line = []
        for wall in walls:
            if wall.Position[1] == y:
                line.append(wall)

        if len(line) > 0:
            wallsByY.append(line)

    for line in wallsByY:
        line.sort(key=sort_by_x)

    sides = 0
    for line in wallsByY:
        gap = 0
        for i in range(len(line)):
            if i == 0:
                continue
            gap = line[i].Position[0] - line[i-1].Position[0]

            # we've got a gap. count the previous side
            if gap > 1:
                sides += 1

        # always count the last side
        sides += 1

    return sides
        
def count_sides_vertical(walls):
    wallsByX = []
    for x in range(height):
        line = []
        for wall in walls:
            if wall.Position[0] == x:
                line.append(wall)

        if len(line) > 0:
            wallsByX.append(line)

    for line in wallsByX:
        line.sort(key=sort_by_y)

    sides = 0
    for line in wallsByX:
        gap = 0
        for i in range(len(line)):
            if i == 0:
                continue
            gap = line[i].Position[1] - line[i-1].Position[1]

            # we've got a gap. count the previous side
            if gap > 1:
                sides += 1

        # always count the last side
        sides += 1

    return sides
        
def count_sides(walls):
    numWalls = 0
    # separate by orientation
    left = list(wall for wall in walls if wall.Direction == WallDirection.LEFT)
    right = list(wall for wall in walls if wall.Direction == WallDirection.RIGHT)
    top = list(wall for wall in walls if wall.Direction == WallDirection.TOP)
    bottom = list(wall for wall in walls if wall.Direction == WallDirection.BOTTOM)

    numWalls += count_sides_horizontal(top)
    numWalls += count_sides_horizontal(bottom)
    numWalls += count_sides_vertical(left)
    numWalls += count_sides_vertical(right)

    return numWalls

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
    sides = []
    while True:
        anyUnvisited = False
        for y in range(height):
            for x in range(width):
                if (x,y) not in visited:
                    anyUnvisited = True
                    newRegion = []
                    newFlower = data[y][x]
                    edgePositions = []
                    floodRegion2((x,y), newFlower, visited, newRegion, edgePositions)
                    sides.append(count_sides(edgePositions))
                    regions.append(newRegion)

                    print(newFlower, ': ', str(sides[len(sides)-1]))

        if not anyUnvisited:
            break

    areas = []

    for region in regions:
        areas.append(len(region))

    cost = 0
    for i in range(len(areas)):
        area = areas[i]
        sideCount = sides[i]
        cost += area * sideCount
    print(cost)

main2()