import sys

def check_cyrillic(text):
    """Check if the text contains Cyrillic characters."""
    for char in text:
        if '\u0400' <= char <= '\u04FF':
            return True
    return False

def caesar_cipher(text, shift, mode):
    """Perform Caesar cipher encoding or decoding on the text."""
    result = []
    shift = shift % 26  # Normalize the shift
    
    if mode == 'decode':
        shift = -shift
    
    for char in text:
        if 'a' <= char <= 'z':
            new_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            result.append(new_char)
        elif 'A' <= char <= 'Z':
            new_char = chr(((ord(char) - ord('A') + shift) % 26 + ord('A')))
            result.append(new_char)
        elif '0' <= char <= '9':
            new_char = chr(((ord(char) - ord('0') + shift) % 10 + ord('0')))
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)

def main():
    try:
        if len(sys.argv) != 4:
            raise ValueError("Usage: python3 caesar.py [encode|decode] [text] [shift]")
        
        mode = sys.argv[1]
        text = sys.argv[2]
        
        if mode not in ['encode', 'decode']:
            raise ValueError("First argument must be either 'encode' or 'decode'")
        
        try:
            shift = int(sys.argv[3])
        except ValueError:
            raise ValueError("Shift must be an integer")
        
        if check_cyrillic(text):
            raise ValueError("The script does not support your language yet")
        
        result = caesar_cipher(text, shift, mode)
        print(result)
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()