import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("File not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        data = []
        start_index = 1 if has_header else 0
        
        for line in lines[start_index:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            
            first, second = int(parts[0]), int(parts[1])
            
            data.append([first, second])
        
        return data

    class Calculations:
        @staticmethod
        def counts(data):
            heads = sum(1 for item in data if item[0] == 1)
            tails = sum(1 for item in data if item[1] == 1)
            return heads, tails

        @staticmethod
        def fractions(heads, tails):
            total = heads + tails
            if total == 0:
                return 0.0, 0.0
            head_percent = (heads / total) * 100
            tail_percent = (tails / total) * 100
            return head_percent, tail_percent

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_nest.py <file_path>", file=sys.stderr)
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)
        
        calculations = research.Calculations()
        heads, tails = calculations.counts(data)
        print(heads, tails)
        
        head_percent, tail_percent = calculations.fractions(heads, tails)
        print(head_percent, tail_percent)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)