import unicodedata

# Function to normalize and remove accent marks
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

# Function to process a text file
def process_file(file_path, encoding='utf-8'):
    words = set()
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            for line in file:
                word = line.strip().lower()  # Convert to lowercase and remove extra spaces
                word = remove_accents(word)  # Remove accents
                words.add(word)
    except UnicodeDecodeError:
        print(f"Error reading {file_path} with encoding {encoding}.")
    return words

# Combine the words from both files
def combine_files(file1, encoding1, file2, encoding2, output_file):
    words1 = process_file(file1, encoding1)
    words2 = process_file(file2, encoding2)
    
    # Combine both sets (set automatically removes duplicates)
    combined_words = words1.union(words2)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in sorted(combined_words):  # Sort the words alphabetically
            outfile.write(word + '\n')

# Example usage
file1 = 'wordsList.txt'  # Replace with the path to your first file
encoding1 = 'ANSI'  # Replace with the encoding of your first file (e.g., 'utf-8', 'latin1')
file2 = 'br-sem-acentos.txt'  # Replace with the path to your second file
encoding2 = 'utf-8'  # Replace with the encoding of your second file (e.g., 'utf-8', 'latin1')
output_file = 'br-sem-acentos.txt'  # Path for the output file

combine_files(file1, encoding1, file2, encoding2, output_file)
