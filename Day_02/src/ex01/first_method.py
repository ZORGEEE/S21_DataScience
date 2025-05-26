class Research:
    def file_reader(self):
        with open('data.csv', 'r') as file:
            return file.read()

if __name__ == '__main__':
    research = Research()
    print(research.file_reader(), end='')