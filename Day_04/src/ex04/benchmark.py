#!/usr/bin/env python3

import timeit
import random
from collections import Counter

def generator():
    return [random.randint(0, 100) for _ in range(1000000)]

def create_count_dict(numbers):
    count_dict = {i: 0 for i in range(101)}
    for n in numbers:
        count_dict[n] += 1
    return count_dict

def top10_with_dict(numbers):
    count_dict = {}
    for num in numbers:
        count_dict[num] = count_dict.get(num, 0) + 1
    return dict(sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:10])

def count_with_counter(numbers):
    return Counter(numbers)

def top10_with_counter(numbers):
    return dict(Counter(numbers).most_common(10))

def benchmark():
    custom_count_time = timeit.timeit(
        lambda: create_count_dict(rand_list),
        globals=globals(),
        number=10
    )

    counter_count_time = timeit.timeit(
        lambda: count_with_counter(rand_list),
        globals=globals(),
        number=10
    )

    custom_top_time = timeit.timeit(
        lambda: top10_with_dict(rand_list),
        globals=globals(),
        number=10
    )

    counter_top_time = timeit.timeit(
        lambda: top10_with_counter(rand_list),
        globals=globals(),
        number=10
    )
    
    print(f"my function: {custom_count_time / 10:.7f}")
    print(f"Counter: {counter_count_time / 10:.7f}")
    print(f"my top: {custom_top_time / 10:.7f}")
    print(f"Counter's top: {counter_top_time / 10:.7f}")

    print(f"{create_count_dict(rand_list)}\n")
    print(f"{top10_with_dict(rand_list)}\n")

    print(f"{count_with_counter(rand_list)}\n")
    print(f"{top10_with_counter(rand_list)}\n")

if __name__ == '__main__':
    
    try:
        rand_list = generator()
        benchmark()
    except Exception as e:
        print(f"Error {e}")