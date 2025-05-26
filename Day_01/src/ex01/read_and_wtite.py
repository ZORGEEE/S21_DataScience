def parse_csv_line(line):
    """Parses a CSV line into fields, handling quoted commas."""
    fields = []
    current_field = []
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i+1] == '"':
                # Handle escaped quote ("") inside quoted field
                current_field.append('"')
                i += 2
                continue
            else:
                in_quotes = not in_quotes
                current_field.append(char)
        elif char == ',' and not in_quotes:
            # End of field, add to fields list
            fields.append(''.join(current_field))
            current_field = []
        else:
            current_field.append(char)
        
        i += 1
    
    # Add the last field
    fields.append(''.join(current_field))
    
    return fields

def convert_csv_to_tsv(input_file, output_file):
    """Converts CSV to TSV without external modules."""
    with open(input_file, 'r', encoding='utf-8') as csv_file:
        with open(output_file, 'w', encoding='utf-8') as tsv_file:
            for line in csv_file:
                line = line.strip()
                if not line:
                    continue #Skip empty lines
                
                fields = parse_csv_line(line)
                tsv_line = '\t'.join(fields)
                tsv_file.write(tsv_line + '\n')

if __name__ == "__main__":
    input_csv = "ds.csv"
    output_tsv = "ds.tsv"
    convert_csv_to_tsv(input_csv, output_tsv)