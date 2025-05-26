import sys

def process_emails(input_file_path):
    try:
        with open(input_file_path, 'r') as file:
            emails = file.read().splitlines()
        
        entries = []
        for email in emails:
            if not email.endswith('@corp.com'):
                continue
            
            # Extract name and surname
            name_part = email.split('@')[0]
            parts = name_part.split('.')
            if len(parts) != 2:
                continue
            
            name, surname = parts
            # Capitalize first letter and make rest lowercase
            name = name.capitalize()
            surname = surname.capitalize()
            
            entries.append(f"{name}\t{surname}\t{email}")
        
        # Write to employees.tsv
        with open('employees.tsv', 'w') as out_file:
            out_file.write("Name\tSurname\tE-mail\n")
            out_file.write('\n'.join(entries))
            
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_emails.py <input_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    process_emails(input_file)