from dataclasses import dataclass
from enum import Enum
import msvcrt
import os

data = []
with open('test', 'r') as file:
    data = file.read()
parts = data.split('\n\n')
mapInput = list(line.strip() for line in (parts[0].split('\n')))
movesInput = parts[1].strip()

class CellType(Enum):
    Empty = 1
    Wall = 2
    Box = 3
    BoxLeft = 4
    BoxRight = 5

@dataclass
class CellState:
    Type : CellType = CellType.Empty

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
        self.grid = []
        for y,line in enumerate(input):
            row = []
            for x,char in enumerate(line):
                cell = CellState()
                if char == '#':
                    cell.Type = CellType.Wall
                elif char == 'O':
                    cell.Type = CellType.BoxLeft
                elif char == '@':
                    self.robot = (2*x,y)
                row.append(cell)
                
                extraCell = CellState()
                extraCell.Type = cell.Type
                if extraCell.Type == CellType.BoxLeft:
                    extraCell.Type = CellType.BoxRight
                row.append(extraCell)

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
                if cell.Type == CellType.BoxLeft:
                    score += (100 * y + x)

        return score

    def print(self):
        for y,line in enumerate(self.grid):
            outStr = ''
            for x,cell in enumerate(line):
                if cell.Type == CellType.BoxLeft:
                    outStr += '['
                elif cell.Type == CellType.BoxRight:
                    outStr += ']'
                elif cell.Type == CellType.Wall:
                    outStr += '#'
                else:
                    if self.robot[0] == x and self.robot[1] == y:
                        outStr += '@'
                    else:
                        outStr += '.'
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

interactMain()