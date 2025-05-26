#!/usr/bin/env python3
import timeit
import sys

def loop(emails):
    new_list = []
    for email in emails:
        if email.endswith('@gmail.com'):
            new_list.append(email)
    return new_list

def list_comp(emails):
    return [email for email in emails if email.endswith('@gmail.com')]

def mapping(emails):
    return list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))

def filter_approach(emails):
    return list(filter(lambda email: email.endswith('@gmail.com'), emails))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./benchmark.py <method> <number_of_calls>")
        sys.exit(1)
    
    method = sys.argv[1]
    number_of_calls = int(sys.argv[2])

    emails = [
        'john@gmail.com',
        'james@gmail.com',
        'alice@yahoo.com',
        'anna@live.com',
        'philipp@gmail.com'
    ]
    emails *= 5

    try:
        approaches = {
            'loop': loop(emails),
            'list_comprehension': list_comp(emails),
            'map': mapping(emails),
            'filter': filter_approach(emails)
        }
        
        if method not in approaches:
            print("Invalid method. Choose from: loop, list_comprehension, map, filter")
            sys.exit(1)

        time_spent = timeit.timeit(lambda: approaches[method], number=number_of_calls)
        print(time_spent)
    except Exception as e:
        print(f"Error {e}")