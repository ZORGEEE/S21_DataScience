#!/usr/bin/env python3
import sys
import resource
import time

def read_file_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line

def main():
    if len(sys.argv) != 2:
        print("Usage: python generator.py <filename>")
        sys.exit(1)
    
    start_time = time.time()
    lines = read_file_generator(sys.argv[1])
    
    # Iterate through lines (doing nothing)
    for line in lines:
        pass
    
    end_time = time.time()
    
    # Memory usage in GB
    peak_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3)
    # Time in seconds (user + system)
    user_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    system_time = resource.getrusage(resource.RUSAGE_SELF).ru_stime
    
    print(f"Peak Memory Usage = {peak_mem:.3f} GB")
    print(f"User Mode Time + System Mode Time = {user_time + system_time:.2f}s")

if __name__ == "__main__":
    main()