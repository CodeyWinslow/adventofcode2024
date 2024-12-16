from dataclasses import dataclass
from enum import Enum
import time
import os

def parse_input(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            data = file.readlines()
    except(Exception):
        print('failed to open file: ', filename)

    return data

def solve(input):
    print('fill me out!')

def main():
    input = parse_input('test')
    time_begin = time.perf_counter()
    solve(input)
    time_end = time.perf_counter()
    print("Total time taken: ", str(time_end - time_begin), ' seconds')

main()