from enum import Enum
from dataclasses import dataclass

data = []
with open('input', 'r') as file:
    data = list(line.strip() for line in file.readlines())

HEIGHT = len(data)
WIDTH = len(data[0])

class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

@dataclass
class Walker:
    Position = None
    Dir = None
    Score = 0
    Path = []

def get_char(pos):
    return data[pos[1]][pos[0]]

def in_range(pos):
    x = pos[0]
    y = pos[1]
    return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT

def turn_left(dir):
    match (dir.value - 2) % 4 + 1:
        case 1:
            return Direction.RIGHT
        case 2:
            return Direction.DOWN
        case 3:
            return Direction.LEFT
        case 4:
            return Direction.UP

def turn_right(dir):
    match dir.value % 4 + 1:
        case 1:
            return Direction.RIGHT
        case 2:
            return Direction.DOWN
        case 3:
            return Direction.LEFT
        case 4:
            return Direction.UP

def get_forward(pos, dir):
    x = pos[0]
    y = pos[1]
    match dir:
        case Direction.RIGHT:
            x += 1
        case Direction.DOWN:
            y += 1
        case Direction.LEFT:
            x -= 1
        case Direction.UP:
            y -= 1
    return (x,y)

def get_best_score(scores):
    lowest = scores[0]
    for score in scores:
        if score < lowest:
            lowest = score
    return lowest

def generate_best_positions(paths, bestScore):
    positions = set()
    for path in paths:
        score,pathList = path
        if score == bestScore:
            for pos in pathList:
                positions.add(pos)

    return positions

def print_best(pathSet):
    for y,line in enumerate(data):
        outStr = ''
        for x,char in enumerate(line):
            if (x,y) in pathSet:
                outStr += 'O'
            else:
                outStr += char
        print(outStr)

def enumerate_paths(startPos, startDir, paths, scores):
    bestScorePositions = {}

    queue = []

    walker = Walker()
    walker.Position = startPos
    walker.Dir = startDir
    walker.Score = 0

    queue.append(walker)

    while len(queue) > 0:
        walker = queue.pop(0)
        char = get_char(walker.Position)
        if char == '#':
            continue

        # if walker.Position in walker.Path:
        #     continue

        # bail if we're somewhere where a better score has already been
        if walker.Position in bestScorePositions.keys():
            diff = walker.Score - bestScorePositions[walker.Position]
            if diff > 1000:
                continue
            
            if bestScorePositions[walker.Position] > walker.Score:
                bestScorePositions[walker.Position] = walker.Score
        else:
            bestScorePositions[walker.Position] = walker.Score

        if char == 'E':
            #scores.clear()
            walker.Path.append(walker.Position)
            paths.append((walker.Score,walker.Path))
            scores.append(walker.Score)
            continue

        walker.Score += 1
        walker.Path.append(walker.Position)

        leftWalker = Walker()
        leftWalker.Dir = turn_left(walker.Dir)
        leftWalker.Score = walker.Score + 1000
        leftWalker.Position = get_forward(walker.Position, leftWalker.Dir)
        leftWalker.Path = walker.Path.copy()

        rightWalker = Walker()
        rightWalker.Dir = turn_right(walker.Dir)
        rightWalker.Score = walker.Score + 1000
        rightWalker.Position = get_forward(walker.Position, rightWalker.Dir)
        rightWalker.Path = walker.Path.copy()

        walker.Position = get_forward(walker.Position, walker.Dir)

        queue.append(rightWalker)
        queue.append(walker)
        queue.append(leftWalker)


def main():
    start = (1, HEIGHT - 2)
    startDir = Direction.RIGHT
    scores = []
    paths = []
    enumerate_paths(start, startDir, paths, scores)
    lowest = get_best_score(scores)
    print(lowest)
    print(len(generate_best_positions(paths, get_best_score(scores))))

main()