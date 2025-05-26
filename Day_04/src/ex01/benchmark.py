#!/usr/bin/env python3
import timeit

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

if __name__ == '__main__':
    emails = [
        'john@gmail.com',
        'james@gmail.com',
        'alice@yahoo.com',
        'anna@live.com',
        'philipp@gmail.com'
    ]
    emails *= 5

    try:
        loop_time = timeit.timeit(lambda: loop(emails), number=900000)
        comprehension_time = timeit.timeit(lambda: list_comp(emails), number=900000)
        map_time = timeit.timeit(lambda: mapping(emails), number=900000)

        times = {
            'loop': loop_time,
            'list comprehension': comprehension_time,
            'map': map_time
        }
        
        fastest_method = min(times, key=times.get)

        if fastest_method == 'loop':
            print("it is better to use a loop")
        elif fastest_method == 'list comprehension':
            print("it is better to use a list comprehension")
        else:
            print("it is better to use a map")

        sorted_times = sorted(times.values())
        print(f"{sorted_times[0]} vs {sorted_times[1]} vs {sorted_times[2]}")
    except Exception as e:
        print(f"Error {e}")