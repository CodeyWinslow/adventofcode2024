from dataclasses import dataclass
import os
import time

data = []
with open('test', 'r') as file:
    data = list(line.strip() for line in file.readlines())

WIDTH = 101
HEIGHT = 103
testing = True
if testing:
    WIDTH = 11
    HEIGHT = 7

class Sandbox:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = list(list(list() for x in range(width)) for y in range(height))
        self.robots = []

    def parse_state(self, input):
        for line in input:
            parts = line.split()

            # start position
            xystring = parts[0][2:].split(',')
            x = int(xystring[0])
            y = int(xystring[1])

            position = (x,y)

            # velocity
            xystring = parts[1][2:].split(',')
            x = int(xystring[0])
            y = int(xystring[1])

            velocity = (x,y)

            index = len(self.robots)
            self.robots.append(velocity)
            self.grid[position[1]][position[0]].append(index)

    def score_quadrants(self):
        halfX = self.width // 2
        halfY = self.height // 2

        halfStartX = self.width - halfX
        halfStartY = self.height - halfY
        quad1 = list(list(line[:halfX]) for line in self.grid[:halfY])
        quad2 = list(list(line[halfStartX:]) for line in self.grid[:halfY])
        quad3 = list(list(line[:halfX]) for line in self.grid[halfStartY:])
        quad4 = list(list(line[halfStartX:]) for line in self.grid[halfStartY:])
        quads = [quad1, quad2, quad3, quad4]
        score = 1
        for quad in quads:
            sum = 0
            for line in quad:
                for robots in line:
                    sum += len(robots)

            if sum > 0:
                score *= sum

        return score

    def wrapx(self, x):
        while x < 0:
            x += self.width
        while x >= self.width:
            x -= self.width

        return x

    def wrapy(self, y):
        while y < 0:
            y += self.height
        while y >= self.height:
            y -= self.height

        return y

    def step(self):
        nextGrid = list(list([] for x in range(self.width)) for y in range(self.height))

        for y,line in enumerate(self.grid):
            for x,robots in enumerate(line):
                for index in robots:
                    vel = self.robots[index]
                    nextPositionX = x + vel[0]
                    nextPositionY = y + vel[1]

                    nextPositionX = self.wrapx(nextPositionX)
                    nextPositionY = self.wrapy(nextPositionY)

                    nextGrid[nextPositionY][nextPositionX].append(index)

        self.grid = nextGrid

    def is_christmas_tree(self):
        expected = 1
        for line in self.grid:
            num = 0
            for robots in line:
                num += len(robots)

                if num > expected:
                    return False
            expected += 2
        return True

    def print(self):
        for line in self.grid:
            outStr = ''
            for robots in line:
                numBots = len(robots)
                outStr += str(numBots) if numBots > 0 else '.'
            print(outStr)

def main():
    print()
    sb = Sandbox(WIDTH, HEIGHT)
    sb.parse_state(data)
    for seconds in range(100):
        sb.step()
    
    print(sb.score_quadrants())

def main2():
    print()
    sb = Sandbox(WIDTH, HEIGHT)
    sb.parse_state(data)
    while True:
        os.system('cls')
        sb.print()
        #input()
        time.sleep(0.5)
        sb.step()

main2()
