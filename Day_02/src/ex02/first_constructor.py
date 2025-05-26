import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("File not found")

        with open('data.csv', 'r') as file:
            return file.read()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <file_path>", file=sys.stderr)
        sys.exit(1)

    try:
        research = Research(sys.argv[1])
        print(research.file_reader(), end='')
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)