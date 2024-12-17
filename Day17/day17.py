from dataclasses import dataclass
from enum import Enum
import time
import os

def parse_input(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            data = list(line.strip() for line in file.readlines())
    except(Exception):
        print('failed to open file: ', filename)

    return data

@dataclass
class CPU:
    registers = []
    iptr = 0
    jumped = False

def get_operand(cpu, operand):
    realOperand = operand
    if realOperand > 3:
        realOperand = cpu.registers[realOperand - 4]

    return realOperand

def op_adv(operand, cpu, output):
    # A register
    numerator = cpu.registers[0]
    # convert operand
    combo = get_operand(cpu, operand)
    # perform operation
    denom = pow(2,combo)
    result = numerator // denom
    # write to A register
    cpu.registers[0] = result

def op_bxl(operand, cpu, output):
    # B register
    B = cpu.registers[1]
    # perform operation
    result = B ^ operand
    # write to B register
    cpu.registers[1] = result

def op_bst(operand, cpu, output):
    combo = get_operand(cpu, operand)
    result = combo % 8
    cpu.registers[1] = result

def op_jnz(operand, cpu, output):
    A = cpu.registers[0]
    if A != 0:
        cpu.iptr = operand
        cpu.jumped = True

def op_bxc(operand, cpu, output):
    # B register
    B = cpu.registers[1]
    # C register
    C = cpu.registers[2]
    # perform operation
    result = B ^ C
    # write to B register
    cpu.registers[1] = result

def op_out(operand, cpu, output):
    combo = get_operand(cpu, operand)
    output.append(str(combo % 8))

def op_bdv(operand, cpu, output):
    # A register
    numerator = cpu.registers[0]
    # convert operand
    combo = get_operand(cpu, operand)
    # perform operation
    denom = pow(2,combo)
    result = numerator // denom
    # write to B register
    cpu.registers[1] = result

def op_cdv(operand, cpu, output):
    # A register
    numerator = cpu.registers[0]
    # convert operand
    combo = get_operand(cpu, operand)
    # perform operation
    denom = pow(2,combo)
    result = numerator // denom
    # write to C register
    cpu.registers[2] = result

def solve(input):
    A = int(input[0][12:])
    B = int(input[1][12:])
    C = int(input[2][12:])
    program = list(int(num) for num in input[4][9:].split(','))
    ops = [op_adv, op_bxl, op_bst, op_jnz, op_bxc, op_out, op_bdv, op_cdv]
    out = []

    print(A)
    print(B)
    print(C)

    print(program)

    cpu = CPU()
    cpu.registers = [A,B,C]
    while cpu.iptr < len(program):
        opcode = program[cpu.iptr]
        operand = program[cpu.iptr + 1]
        ops[opcode](operand, cpu, out)
        if not cpu.jumped:
            cpu.iptr += 2
        cpu.jumped = False
    print('REG DUMP: ', str(cpu.registers))
    print('OUT: ',','.join(out) if len(out) > 0 else "<NO OUTPUT>")

def doesMatch(program, output, exact = False):
    if len(output) > len(program):
        return False
    if exact and len(output) != len(program):
        return False
    end = min(len(program), len(output))
    for i in range(end):
        if program[i] != int(output[i]):
            return False
        
    return True

def solve2(input):
    A = int(input[0][12:])
    B = int(input[1][12:])
    C = int(input[2][12:])
    program = list(int(num) for num in input[4][9:].split(','))
    ops = [op_adv, op_bxl, op_bst, op_jnz, op_bxc, op_out, op_bdv, op_cdv]

    counter = 0
    while True:
        # try a value for A
        A = counter

        out = []
        lastOutLen = 0

        programMismatch = False
        cpu = CPU()
        cpu.registers = [A,B,C]
        while cpu.iptr < len(program):
            opcode = program[cpu.iptr]
            operand = program[cpu.iptr + 1]
            ops[opcode](operand, cpu, out)

            if not cpu.jumped:
                cpu.iptr += 2
            cpu.jumped = False
            
            newLen = len(out)
            if newLen != lastOutLen:
                if not doesMatch(program, out):
                    programMismatch = True
                    break
                lastOutLen = newLen

        if not programMismatch and doesMatch(program, out, True):
            break

        counter += 1
        
    print('A: ',str(counter))

def main():
    input = parse_input('input')
    time_begin = time.perf_counter()
    solve2(input)
    time_end = time.perf_counter()
    print("Total time taken: ", str(time_end - time_begin), ' seconds')

main()