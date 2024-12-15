from dataclasses import dataclass
from enum import Enum
import msvcrt
import os

data = []
with open('input', 'r') as file:
    data = file.read()
parts = data.split('\n\n')
mapInput = list(line.strip() for line in (parts[0].split('\n')))
movesInput = parts[1].strip()

class CellType(Enum):
    Empty = 1
    Wall = 2
    Box = 3

@dataclass
class CellState:
    Type : CellType = CellType.Empty

@dataclass
class Object:
    Position = None
    CanMove = False
    def __init__(self, pos):
        self.Position = pos

    def __eq__(left, right):
        if left is None or right is None:
            return left is None and right is None
        if not isinstance(left, Object) or not isinstance(right, Object):
            return False
        return left.Position == right.Position
    
    def __ne__(left, right):
        return not left == right

class MoveDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def direction_from_char(char):
    match char:
        case '^':
            return MoveDirection.UP
        case '>':
            return MoveDirection.RIGHT
        case 'v':
            return MoveDirection.DOWN
        case '<':
            return MoveDirection.LEFT

class Sim:
    def __init__(self, input):
        self.height = len(input)
        self.width = 0 if self.height == 0 else len(input[0])
        self.robot = (0,0)
        self.grid = []
        for y,line in enumerate(input):
            row = []
            for x,char in enumerate(line):
                cell = CellState()
                if char == '#':
                    cell.Type = CellType.Wall
                elif char == 'O':
                    cell.Type = CellType.Box
                elif char == '@':
                    self.robot = (x,y)
                row.append(cell)
            self.grid.append(row)

    def get_next_position(position, move):
        posx = position[0]
        posy = position[1]

        match move:
            case MoveDirection.UP:
                posy -= 1
            case MoveDirection.RIGHT:
                posx += 1
            case MoveDirection.DOWN:
                posy += 1
            case MoveDirection.LEFT:
                posx -= 1

        return (posx,posy)

    def get_cell(self, pos)->CellState:
        x = pos[0]
        y = pos[1]
        return self.grid[y][x]

    def try_move(self, pos, move):
        cell = self.get_cell(pos)
        if cell.Type == CellType.Empty:
            return True
        elif cell.Type == CellType.Wall:
            return False
        
        next = Sim.get_next_position(pos, move)
        couldMove = self.try_move(next, move)
        if couldMove:
            nextCell = self.get_cell(next)
            nextCell.Type = cell.Type
        
        return couldMove

    def execute(self, move : MoveDirection):
        curPos = self.robot
        nextPos = Sim.get_next_position(curPos, move)
        
        if self.try_move(nextPos, move):
            cell = self.get_cell(nextPos)
            cell.Type = CellType.Empty
            self.robot = nextPos

    def execute_multi(self, moves):
        for move in moves:
            self.execute(move)

    def score(self):
        score = 0

        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell((x,y))
                if cell.Type == CellType.Box:
                    score += (100 * y + x)

        return score

    def print(self):
        for y,line in enumerate(self.grid):
            outStr = ''
            for x,cell in enumerate(line):
                if cell.Type == CellType.Box:
                    outStr += 'O'
                elif cell.Type == CellType.Wall:
                    outStr += '#'
                else:
                    if self.robot[0] == x and self.robot[1] == y:
                        outStr += '@'
                    else:
                        outStr += '.'
            print(outStr)

class Sim2:
    def __init__(self, input):
        self.height = len(input)
        self.width = 0 if self.height == 0 else 2*len(input[0])
        self.robot = (0,0)
        self.objects = []
        for y,line in enumerate(input):
            for x,char in enumerate(line):
                if char == '#':
                    self.objects.append(Object((2*x,y)))
                elif char == 'O':
                    box = Object((2*x,y))
                    box.CanMove = True
                    self.objects.append(box)
                elif char == '@':
                    self.robot = (2*x,y)

    def get_next_position(position, move):
        posx = position[0]
        posy = position[1]

        match move:
            case MoveDirection.UP:
                posy -= 1
            case MoveDirection.RIGHT:
                posx += 1
            case MoveDirection.DOWN:
                posy += 1
            case MoveDirection.LEFT:
                posx -= 1

        return (posx,posy)

    def find_object(self, pos):
        for obj in self.objects:
            x = obj.Position[0]
            y = obj.Position[1]
            if y == pos[1] and \
                (x == pos[0] or x == pos[0] - 1):
                return obj
        return None
    
    def propose_moves(self, obj, move, proposed):
        if not obj.CanMove:
            return False
        
        next = Sim.get_next_position(obj.Position, move)
        checkNext = next
        if move == MoveDirection.RIGHT:
            checkNext = (next[0] + 1, next[1])
        nextObj = self.find_object(checkNext)
        # potentially get a second obstacle on the right side if this object
        nextObj2 = nextObj
        if move == MoveDirection.UP or move == MoveDirection.DOWN:
            checkNext = (next[0] + 1, next[1])
            nextObj2 = self.find_object(checkNext)
        
        canmove = True
        
        newProposed = []
        if nextObj != None:
            canmove = self.propose_moves(nextObj, move, newProposed)

        if canmove and nextObj2 and nextObj != nextObj2:
            canmove = self.propose_moves(nextObj2, move, newProposed)


        proposed += newProposed
        if canmove:
            proposed += [(obj, next)]
        return canmove

    def try_move(self, pos, move):
        obj = self.find_object(pos)
        if obj:
            proposedMoves = []
            canMove = self.propose_moves(obj, move, proposedMoves)
            if canMove:
                for pm in proposedMoves:
                    obj = pm[0]
                    newpos = pm[1]
                    obj.Position = newpos
            return canMove
        return True
        
    def execute(self, move : MoveDirection):
        curPos = self.robot
        nextPos = Sim.get_next_position(curPos, move)
        
        if self.try_move(nextPos, move):
            self.robot = nextPos

    def execute_multi(self, moves):
        for move in moves:
            self.execute(move)

    def score(self):
        score = 0

        for obj in self.objects:
            if obj.CanMove:
                score += (100 * obj.Position[1] + obj.Position[0])

        return score

    def print(self):
        grid = list('.' * self.width for i in range(self.height))

        for obj in self.objects:
            x = obj.Position[0]
            y = obj.Position[1]
            line = grid[y]
            if obj.CanMove:
                grid[y] = line[:x] + '[]' + line[x+2:]
            else:
                grid[y] = line[:x] + '##' + line[x+2:]

        line1 = '  '
        line2 = '  '
        tens = list(i//10 for i in range(self.width))
        ones = list(i%10 for i in range(self.width))
        for i in tens:
            line1 += str(i) if i > 0 else ' '
        for i in ones:
            line2 += str(i)
        print(line1)
        print(line2)
        
        for y,line in enumerate(grid):
            outStr = ' ' * (2 - len(str(y))) + str(y)
            for x,char in enumerate(line):
                if self.robot[0] == x and self.robot[1] == y:
                    outStr += '@'
                else:
                    outStr += char
            print(outStr)


def generate_moves(inputStr):
    moves = [None] * len(inputStr)
    
    for i,char in enumerate(inputStr):
        moves[i] = direction_from_char(char)

    return moves

def move_from_key(key):
    match key:
        case b'w':
            return MoveDirection.UP
        case b'a':
            return MoveDirection.LEFT
        case b's':
            return MoveDirection.DOWN
        case b'd':
            return MoveDirection.RIGHT

def main():
    sim = Sim(mapInput)
    sim.print()
    print('...')
    sim.execute_multi(generate_moves(movesInput))
    sim.print()
    print(sim.score())

def interactMain():
    sim = Sim2(mapInput)
    while True:
        os.system('cls')
        print('press "q" to exit')
        print('use "wasd" to move\n')
        sim.print()
        lastch = msvcrt.getch()
        if lastch == b'q':
            break
        else:
            move = move_from_key(lastch)
            sim.execute(move)

def main2():
    sim = Sim2(mapInput)
    sim.print()
    print('...')
    sim.execute_multi(generate_moves(movesInput))
    sim.print()
    print(sim.score())

main2()