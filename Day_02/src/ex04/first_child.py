import sys
from random import randint

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True):
        if not hasattr(sys, 'argv'):
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
    def __init__(self, data):
        self.data = data

    def counts(self):
        heads = sum(1 for item in data if item[0] == 1)
        tails = sum(1 for item in data if item[1] == 1)
        return heads, tails
    
    def fractions(self, heads, tails):
        total = heads + tails
        if total == 0:
            return 0.0, 0.0
        head_percent = (heads / total) * 100
        tail_percent = (tails / total) * 100
        return head_percent, tail_percent

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            if randint(0, 1) == 1:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        return predictions
    
    def predict_last(self):
        return self.data[-1]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_nest.py <file_path>", file=sys.stderr)
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)
        
        analytics = Analytics(data)
        heads, tails = analytics.counts()
        print(heads, tails)
        
        head_percent, tail_percent = analytics.fractions(heads, tails)
        print(head_percent, tail_percent)

        random_predictions = analytics.predict_random(3)
        print(random_predictions)

        last_prediction = analytics.predict_last()
        print(last_prediction)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)