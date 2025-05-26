#!/usr/bin/env python3
import timeit

def loop(emails):
    new_list = []
    for email in emails:
        if email.endswith('@gmail.com'):
            new_list.append(email)
    return new_list

def list_comp(emails):
    new_list = [email for email in emails if email.endswith('@gmail.com')]
    return new_list

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
        loop_time = timeit.timeit(lambda: loop(emails), number=90_000_00)
        comprehension_time = timeit.timeit(lambda: list_comp(emails), number=90_000_00)

        # Determine which is better and print the result
        if comprehension_time <= loop_time:
            print("it is better to use a list comprehension")
        else:
            print("it is better to use a loop")

        # Print the times in ascending order
        if comprehension_time < loop_time:
            print(f"{comprehension_time} vs {loop_time}")
        else:
            print(f"{loop_time} vs {comprehension_time}")

        print(loop(emails))
        print(list_comp(emails))
    except Exception as e:
        print(f"Error {e}")