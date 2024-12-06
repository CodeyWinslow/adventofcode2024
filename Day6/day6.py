from enum import Enum
data = []
with open('test', 'r') as file:
    data = file.readlines()

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

def find_guard():
    x = 0
    y = 0
    for line in data:
        x = 0
        for char in line:
            if char == "^":
                return (x, y)
            x += 1
        y += 1

def is_obstructed(pos):
    x = pos[0]
    y = pos[1]
    return data[y][x] == '#'

def is_in_map(pos, width, height):
    x = pos[0]
    y = pos[1]
    return x >= 0 and x < width and y >= 0 and y < height

def look_forward(pos, dir):
    match dir:
        case Direction.UP:
            pos = (pos[0], pos[1]-1)
        case Direction.DOWN:
            pos = (pos[0], pos[1]+1)
        case Direction.LEFT:
            pos = (pos[0]-1, pos[1])
        case Direction.RIGHT:
            pos = (pos[0]+1, pos[1])
    
    return pos

def rotate(direction):

    match direction:
        case Direction.UP:
            direction = Direction.RIGHT
        case Direction.DOWN:
            direction = Direction.LEFT
        case Direction.LEFT:
            direction = Direction.UP
        case Direction.RIGHT:
            direction = Direction.DOWN
    
    return direction

def make_obstacle(obstacle_pos, my_pos):
    return ((obstacle_pos), (my_pos))

def remember_obstacle(obstacle_pos, my_pos, obstacles):
    obstacles.append(make_obstacle(obstacle_pos,my_pos))
    
def is_obstacle_visited(obstacle_pos, my_pos, obstacles):
    ob_x = obstacle_pos[0]
    ob_y = obstacle_pos[1]
    my_x = my_pos[0]
    my_y = my_pos[1]
    for obstacle in obstacles:
        if obstacle[0][0] == ob_x \
            and obstacle[0][1] == ob_y \
            and obstacle[1][0] == my_x \
            and obstacle[1][1] == my_y:

            return True
        
    return False

def could_be_trapped(pos, direction, width, height, newObstacle):
    newDir = rotate(direction)

    prevObstacles = [ newObstacle ]
    newObstaclePos = newObstacle[0]
    projectedPos = pos
    while is_in_map(projectedPos, width, height):
        nextPos = look_forward(projectedPos, newDir)

        # turn as long as we're running into an obstacle
        # unless we've hit a loop
        while is_in_map(nextPos, width, height) \
            and (is_obstructed(nextPos) or newObstaclePos == nextPos):

            if is_obstacle_visited(nextPos, projectedPos, prevObstacles):
                return True
            
            remember_obstacle(nextPos, projectedPos, prevObstacles)
            newDir = rotate(newDir)
            nextPos = look_forward(projectedPos, newDir)
        
        # move forward
        projectedPos = nextPos

    return False

def output_new_map(visited, allObstacles):
    newData = data.copy()

    for pos in visited:
        x = pos[0]
        y = pos[1]
        prev = newData[y]
        newData[y] = prev[:x] + ' ' + prev[x+1:]

    for obstacle in allObstacles:
        x = obstacle[0]
        y = obstacle[1]
        prev = newData[y]
        newData[y] = prev[:x] + 'O' + prev[x+1:]

    with open('out', 'w') as file:
        file.writelines(newData)

def main():
    width = len(data[0])
    height = len(data)

    visited = set()
    direction = Direction.UP
    position = find_guard()
    while (is_in_map(position, width, height)):
        visited.add(position)
        nextPos = look_forward(position, direction)
        while is_obstructed(nextPos):
            direction = rotate(direction)
            nextPos = look_forward(position, direction)
        
        position = nextPos

    print(len(visited))

def main2():
    width = len(data[0])
    height = len(data)

    visited = set()
    direction = Direction.UP
    position = find_guard()
    start_pos = position
    allObstacles = []
    fakeObstacles = set()
    emptySet = set()
    while (is_in_map(position, width, height)):
        visited.add(position)
        nextPos = look_forward(position, direction)

        # turn as long as we're running into an obstacle
        while is_in_map(nextPos, width, height) and is_obstructed(nextPos):
            remember_obstacle(nextPos, position, allObstacles)
            direction = rotate(direction)
            nextPos = look_forward(position, direction)

        # test if a new obstacle could trap us here
        newObstacle = make_obstacle(nextPos, position)
        if nextPos != start_pos \
            and nextPos not in fakeObstacles \
            and could_be_trapped(position, direction, width, height, newObstacle):

            fakeObstacles.add(nextPos)
        
        # move forward
        position = nextPos

    print(len(fakeObstacles))

    #output_new_map(visited, fakeObstacles)

main2()