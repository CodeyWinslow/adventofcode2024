from enum import Enum
import pygame
from pygame import *
import time

data = []
with open('input', 'r') as file:
    data = file.readlines()

SCREEN_SCALE = 5

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class Sim():

    # PUBLIC
    def __init__(self, world_width, world_height, obstacle_positions, starting_position):
        self.width = world_width
        self.height = world_height
        self.obstacles = obstacle_positions
        self.starting_pos = starting_position

        self.position = self.starting_pos
        self.direction = Direction.UP
        self.visited = set()
        self.fakeObstacles = set()
        self.Finished = not self.is_in_map(self.position)

        self.trap_mode = False
        self.trap_position = self.starting_pos
        self.trap_direction = Direction.UP
        self.trap_new_obstacle = None
        self.trap_visited = set()
        self.trap_obstacles = []
        self.trap_result = False

    def tick(self):
        if self.trap_mode:
            self.tick_could_be_trapped()
            if not self.trap_mode:
                if self.trap_result:
                    self.fakeObstacles.add(self.position) # we already moved into the fake obstacle position
                self.reset_could_be_trapped()

            return

        self.visited.add(self.position)
        nextPos = look_forward(self.position, self.direction)

        # only turn if we're running into an obstacle
        if self.is_in_map(nextPos) and self.is_obstructed(nextPos):
            self.direction = self.rotate(self.direction)
            return

        # test if we could be trapped by a new obstacle in nextPos
        if self.is_in_map(nextPos) \
            and nextPos != self.starting_pos \
            and nextPos not in self.fakeObstacles:

            self.init_could_be_trapped(self.starting_pos, Direction.UP, nextPos)
        
        # move forward
        self.position = nextPos

        # check if we left map
        if not self.is_in_map(self.position):
            self.Finished = True

    # PRIVATE
    def is_obstructed(self, pos):
        x = pos[0]
        y = pos[1]
        matching = list(ob for ob in self.obstacles if (ob[0] == x and ob[1] == y))
        return len(matching) > 0

    def is_in_map(self, pos):
        x = pos[0]
        y = pos[1]
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def look_forward(self, pos, dir):
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

    def rotate(self, direction):

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

    def make_obstacle(self, obstacle_pos, my_pos):
        return ((obstacle_pos), (my_pos))

    def remember_obstacle(self, obstacle_pos, my_pos, obstacles):
        obstacles.append(self.make_obstacle(obstacle_pos,my_pos))
        
    def is_obstacle_visited(self, obstacle_pos, my_pos, obstacles):
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

    def init_could_be_trapped(self, pos, dir, obstacle_pos):
        self.trap_mode = True
        self.trap_position = pos
        self.trap_direction = dir
        self.trap_new_obstacle = make_obstacle(obstacle_pos, pos)

    def reset_could_be_trapped(self):
        self.trap_mode = False
        self.trap_position = self.starting_pos
        self.trap_direction = Direction.UP
        self.trap_new_obstacle = None
        self.trap_visited = set()
        self.trap_obstacles = []
        self.trap_result = False

    def tick_could_be_trapped(self):
        if not self.is_in_map(self.trap_position):
            self.trap_result = False
            self.trap_mode = False

        self.trap_visited.add(self.trap_position)
        nextPos = self.look_forward(self.trap_position, self.trap_direction)

        # turn as long as we're running into an obstacle
        # unless we've hit a loop
        if self.is_in_map(self.trap_position) \
            and (self.is_obstructed(nextPos) or self.trap_new_obstacle[0] == nextPos):

            if self.is_obstacle_visited(nextPos, self.trap_position, self.trap_obstacles):
                self.trap_result = True
                self.trap_mode = False
                return
            
            self.remember_obstacle(nextPos, self.trap_position, self.trap_obstacles)
            self.trap_direction = self.rotate(self.trap_direction)
        else:
            # move forward
            self.trap_position = nextPos

    def could_be_trapped(self, pos, direction):
        newObstaclePos = self.look_forward(pos, direction)
        newObstacle = self.make_obstacle(newObstaclePos, pos)
        prevObstacles = [ newObstacle ]

        newDir = self.rotate(direction)

        projectedPos = pos
        while self.is_in_map(projectedPos):
            nextPos = self.look_forward(projectedPos, newDir)

            # turn as long as we're running into an obstacle
            # unless we've hit a loop
            while self.is_in_map(nextPos) \
                and (self.is_obstructed(nextPos) or newObstaclePos == nextPos):

                if self.is_obstacle_visited(nextPos, projectedPos, prevObstacles):
                    return True
                
                self.remember_obstacle(nextPos, projectedPos, prevObstacles)
                newDir = self.rotate(newDir)
                nextPos = self.look_forward(projectedPos, newDir)
            
            # move forward
            projectedPos = nextPos

        return False


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

def gather_all_obstacles():
    obstacles = []
    y = 0
    for line in data:
        x = 0
        for char in line:
            if char == '#':
                obstacles.append((x,y))
            x += 1
        y += 1

    return obstacles

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

def could_be_trapped(pos, direction, width, height):
    newObstaclePos = look_forward(pos, direction)
    newObstacle = make_obstacle(newObstaclePos, pos)
    prevObstacles = [ newObstacle ]

    newDir = rotate(direction)

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

def point_to_rect(point):
    return Rect(point[0] * SCREEN_SCALE, point[1] * SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE)

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

        # test if we could be trapped by a new obstacle in nextPos
        if nextPos != start_pos \
            and nextPos not in fakeObstacles \
            and could_be_trapped(position, direction, width, height):

            fakeObstacles.add(nextPos)
        
        # move forward
        position = nextPos

    print(len(fakeObstacles))

    #output_new_map(visited, fakeObstacles)

def main3():
    show_viz = True
    obstacles = gather_all_obstacles()
    sim = Sim(len(data[0]), len(data), obstacles, find_guard())

    if show_viz:
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        screen = pygame.display.set_mode((len(data[0])*SCREEN_SCALE, len(data)*SCREEN_SCALE))
        pygame.display.set_caption("Algorithm Visualization")
        guard_color = Color(255, 165, 0)
        obstacle_color = Color(200, 50, 50)
        visited_color = Color(200, 200, 200)
        visited_trap_color = Color(255,255,0)
        trap_obstacle_color = Color(0,255,0)


        should_quit = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
            
            if should_quit:
                break

            screen.fill((20, 20, 20))  # background
            
            # Draw state
            for space in sim.visited:
                pygame.draw.rect(screen, visited_color, point_to_rect(space))
            for ob in sim.obstacles:
                pygame.draw.rect(screen, obstacle_color, point_to_rect(ob))

            if sim.trap_mode:
                for visit in sim.trap_visited:
                    pygame.draw.rect(screen, visited_trap_color, point_to_rect(visit))
            
            for ob in sim.fakeObstacles:
                pygame.draw.rect(screen, trap_obstacle_color, point_to_rect(ob))

            pygame.draw.rect(screen, guard_color, point_to_rect(sim.position))

            
            pygame.display.flip()  # Update the screen
            #time.sleep(.16)  # Slow down the animation for demonstration

            if not sim.Finished:
                sim.tick()

        pygame.quit()
    else:
        while not sim.Finished:
            sim.tick()

    print("visited: " + str(len(sim.visited)))
    print("traps: " + str(len(sim.fakeObstacles)))


main3()