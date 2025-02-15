import os
import unicodedata

# Function to normalize and remove accent marks
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# Function to read words from a file and normalize them
def read_words(file_path):
    words = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()  # Remove extra spaces
            word = remove_accents(word)  # Normalize the word
            words.add(word)
    return words

# Function to write words to a file, grouped by length and sorted alphabetically
def write_words(file_path, words):
    # Group words by length
    words_by_length = {}
    for word in words:
        length = len(word)
        if length not in words_by_length:
            words_by_length[length] = []
        words_by_length[length].append(word)
    
    # Sort words by length and then alphabetically
    with open(file_path, 'w', encoding='utf-8') as file:
        for length in sorted(words_by_length.keys()):
            for word in sorted(words_by_length[length]):
                file.write(word + '\n')

# Function to update the dictionary with new words
def update_dictionary(dictionary_file, new_words_file):
    # Read existing dictionary words
    if os.path.exists(dictionary_file):
        dictionary_words = read_words(dictionary_file)
    else:
        dictionary_words = set()
    
    # Read new words from the final result file
    new_words = read_words(new_words_file)
    
    # Merge and deduplicate
    updated_words = dictionary_words.union(new_words)
    
    # Write back to the dictionary file
    write_words(dictionary_file, updated_words)

    print("Dictionary updated successfully.")