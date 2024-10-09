import os
import itertools
from unidecode import unidecode

# Function to load and process words from a file
def load_and_process_words(filename, wordsize):
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        words = {unidecode(word.strip().lower()) for word in file.readlines() if len(word.strip()) == wordsize}
    return words

def filter_words(base_letters, valid_words, wordsize):
    # Create a set of allowed letters for fast lookup
    allowed_letters = set(base_letters)

    # Filter words based on wordsize and allowed letters
    filtered_words = [
        word for word in valid_words
        if len(word) == wordsize and all(letter in allowed_letters for letter in word)
    ]

    return filtered_words

# Function to filter words based on the main letter
def filter_by_main_letter(words, main_letter):
    return {word for word in words if main_letter in word}

# Main function
def main():
    output_file = 'filtered_words.txt'
    
    # Delete the output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    wordsize = int(input("Enter max word size: "))
    # Get input letters from the user
    base_letters = input("Enter 7 letters (no spaces): ").strip().lower()
    # Get the main letter from the user
    main_letter = input("Enter the main letter to filter by: ").strip().lower()
    
    for x in range(4, wordsize + 1):
        # Load and process original Portuguese words
        valid_words = load_and_process_words('wordsList', x)
    
        # Filter words based on the provided letters
        found_words = filter_words(base_letters, valid_words, x)
        
        # Further filter words by the main letter
        filtered_by_main_letter = filter_by_main_letter(found_words, main_letter)
    
        # Output the results
        with open(output_file, 'a', encoding='utf-8') as f:
            for word in filtered_by_main_letter:
                f.write(word + '\n')
    
        print(f"Found {len(filtered_by_main_letter)} valid {x}-letter words using the letters '{base_letters}' containing '{main_letter}' and saved to {output_file}")

# Run the main function
if __name__ == "__main__":
    main()
