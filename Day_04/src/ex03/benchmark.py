#!/usr/bin/env python3

import timeit
import sys
from functools import reduce

def looping(n):
    sum = 0
    for i in range(n + 1):
        sum += i*i
    return sum

def reducing(n):
    return reduce(lambda sum, i: sum + i*i, range(n+1))

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: ./benchmark.py <method> <number_of_calls> <number_of_squares>")
        sys.exit(1)
    
    method = sys.argv[1]
    number_of_calls = int(sys.argv[2])
    number_of_squares = int(sys.argv[3])

    approaches = {
        "loop": looping(number_of_squares),
        "reduce": reducing(number_of_squares)
    }

    try:
        time_spent = timeit.timeit(lambda: approaches[method], number=number_of_calls)
        print(time_spent)
        print(approaches[method])
    except Exception as e:
        print(f"Error {e}")