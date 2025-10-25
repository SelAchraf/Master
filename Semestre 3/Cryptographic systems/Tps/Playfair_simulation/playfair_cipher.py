def generate_key_matrix(key):
    # Use a set for efficient tracking of used characters
    key_chars = set()
    matrix = []
    
    # Sanitize the key: uppercase, replace 'J' with 'I'
    key = key.upper().replace("J", "I")
    
    # Process the key first
    for char in key:
        if char not in key_chars and char.isalpha():
            matrix.append(char)
            key_chars.add(char)
            
    # Process the rest of the alphabet
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in key_chars:
            matrix.append(char)
            key_chars.add(char)
            
    # Reshape the flat list into a 5x5 matrix
    key_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return key_matrix

def find_char_position(matrix, char):
    for r_idx, row in enumerate(matrix):
        for c_idx, col_char in enumerate(row):
            if col_char == char:
                return r_idx, c_idx
    return None, None

def prepare_text(text, filler='X'):
    # Sanitize text
    text = text.upper().replace("J", "I")
    text = "".join(filter(str.isalpha, text))
    
    digraphs = []
    i = 0
    while i < len(text):
        char1 = text[i]
        # End of string: append filler if odd length
        if i + 1 == len(text):
            digraphs.append(char1 + filler)
            break
        
        char2 = text[i+1]
        
        # If characters are the same, insert filler
        if char1 == char2:
            digraphs.append(char1 + filler)
            i += 1 # Move one step forward
        else:
            digraphs.append(char1 + char2)
            i += 2 # Move two steps forward
            
    return digraphs

def crypt(text, key, mode='encrypt'):
    if not key:
        raise ValueError("A key is required.")
    if not text:
        raise ValueError("Input text is required.")

    matrix = generate_key_matrix(key)
    prepared_digraphs = prepare_text(text)
    
    result_text = ""
    
    # Set the direction for shifting based on mode
    shift = 1 if mode == 'encrypt' else -1

    for pair in prepared_digraphs:
        char1, char2 = pair[0], pair[1]
        row1, col1 = find_char_position(matrix, char1)
        row2, col2 = find_char_position(matrix, char2)

        if row1 is None or row2 is None:
            # Should not happen with prepared text, but as a safeguard
            continue

        if row1 == row2: # Same row
            result_text += matrix[row1][(col1 + shift) % 5]
            result_text += matrix[row2][(col2 + shift) % 5]
        elif col1 == col2: # Same column
            result_text += matrix[(row1 + shift) % 5][col1]
            result_text += matrix[(row2 + shift) % 5][col2]
        else: # Rectangle
            result_text += matrix[row1][col2]
            result_text += matrix[row2][col1]
            
    return result_text, matrix