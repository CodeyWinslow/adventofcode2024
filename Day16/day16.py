from enum import Enum
from dataclasses import dataclass

data = []
with open('test', 'r') as file:
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
    PrevPosition = None
    Dir = None
    Score = 0

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

def get_num_best(scoreMap):
    visited = set()
    end = (WIDTH - 2, 1)
    num = 1
    visited.add(end)
    queue = [end]
    while len(queue) > 0:
        curPos = queue.pop(0)
        cur = scoreMap[curPos]
        num += 1

        if cur[1] == None:
            continue

        for pos in cur[1]:
            if pos not in visited and pos is not None:
                visited.add(pos)
                queue.append(pos)

    print(visited)
    return num

def count_best(endPos, scoreMap, score, visited):
    if endPos == None:
        return score+1

    if endPos in visited:
        return score
    
    visited.add(endPos)
    prevs = scoreMap[endPos][1]
    score += 1
    for prev in prevs:
        score = count_best(prev, scoreMap, score, visited)

    return score

def print_best(pathSet):
    for y,line in enumerate(data):
        outStr = ''
        for x,char in enumerate(line):
            if (x,y) in pathSet:
                outStr += 'O'
            else:
                outStr += char
        print(outStr)

def enumerate_paths(startPos, startDir, scores):
    bestScorePositions = {}

    stack = []
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

        # bail if we're somewhere where a better score has already been
        if walker.Position in bestScorePositions.keys():
            if walker.Score > bestScorePositions[walker.Position][0]:
                continue
            
            if bestScorePositions[walker.Position][0] == walker.Score:
                bestScorePositions[walker.Position][1].append(walker.PrevPosition)
            else:
                bestScorePositions[walker.Position] = (walker.Score, [walker.PrevPosition])
        else:
            bestScorePositions[walker.Position] = (walker.Score, [walker.PrevPosition])

        if char == 'E':
            scores.clear()
            scores.append(walker.Score)
            continue

        walker.Score += 1

        leftWalker = Walker()
        leftWalker.Dir = turn_left(walker.Dir)
        leftWalker.Score = walker.Score + 1000
        leftWalker.Position = get_forward(walker.Position, leftWalker.Dir)
        leftWalker.PrevPosition = walker.Position

        rightWalker = Walker()
        rightWalker.Dir = turn_right(walker.Dir)
        rightWalker.Score = walker.Score + 1000
        rightWalker.Position = get_forward(walker.Position, rightWalker.Dir)
        rightWalker.PrevPosition = walker.Position

        walker.PrevPosition = walker.Position
        walker.Position = get_forward(walker.Position, walker.Dir)

        queue.append(rightWalker)
        queue.append(walker)
        queue.append(leftWalker)

    bestPaths = set()
    print(count_best((WIDTH-2, 1), bestScorePositions, 0, bestPaths))
    print_best(bestPaths)

def main():
    start = (1, HEIGHT - 2)
    startDir = Direction.RIGHT
    scores = []
    enumerate_paths(start, startDir, scores)
    lowest = get_best_score(scores)
    print(lowest)

main()