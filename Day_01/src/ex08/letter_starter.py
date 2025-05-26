import sys

def find_employee(email):
    try:
        with open('employees.tsv', 'r') as file:
            # Skip header
            next(file)
            for line in file:
                name, surname, emp_email = line.strip().split('\t')
                if emp_email == email:
                    return name
        return None
    except FileNotFoundError:
        print("Error: employees.tsv file not found. Please run the first script first.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def generate_welcome_letter(email):
    name = find_employee(email)
    if not name:
        print(f"Error: Email '{email}' not found in records.", file=sys.stderr)
        sys.exit(1)
    
    letter = f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That's a precondition for the professionals that our company hires."
    print(letter)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_welcome.py <email>", file=sys.stderr)
        sys.exit(1)
    
    email = sys.argv[1]
    generate_welcome_letter(email)