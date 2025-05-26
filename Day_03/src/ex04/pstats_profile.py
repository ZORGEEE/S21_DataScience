import cProfile
import pstats
from financial import fetch_financials

def main():
    profiler = cProfile.Profile()
    profiler.enable()

    fetch_financials('AAPL', 'Total Revenue')

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(5)

if __name__ == '__main__':
    main()