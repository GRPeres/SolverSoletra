import os
from unidecode import unidecode

# Function to load and process words from a file
def load_and_process_words(filename, wordsize):
    with open(filename, 'r', encoding='UTF-8') as file:
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

# Function to check if a word is a verb (infinitive or plural)
def maybe_plural(word):
    # Basic checks for verb endings (in Portuguese)
    verb_endings = ['s', 'ei', 'iu', 'ndo']
    return any(word.endswith(ending) for ending in verb_endings)

# Main function
def main():
    output_file = 'filtered_words.txt'
    rejected_file = 'rejected_words.txt'
    
    # Delete the output files if they exist
    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(rejected_file):
        os.remove(rejected_file)
    
    wordsize = int(input("Enter max word size: "))
    # Get input letters from the user
    base_letters = input("Enter 7 letters (no spaces): ").strip().lower()
    # Get the main letter from the user
    main_letter = input("Enter the main letter to filter by: ").strip().lower()
    
    for x in range(4, wordsize + 1):
        # Load and process original Portuguese words
        valid_words = load_and_process_words('br-sem-acentos.txt', x)
    
        # Filter words based on the provided letters
        found_words = filter_words(base_letters, valid_words, x)
        
        # Further filter words by the main letter
        filtered_by_main_letter = filter_by_main_letter(found_words, main_letter)
        
        # Sort the filtered words alphabetically
        sorted_words = sorted(filtered_by_main_letter)

        # Separate rejected words
        rejected_words = [word for word in sorted_words if maybe_plural(word)]
        accepted_words = [word for word in sorted_words if not maybe_plural(word)]
        
        # Output the accepted results
        with open(output_file, 'a', encoding='utf-8') as f:
            for word in accepted_words:
                f.write(word + '\n')
        
        # Output the rejected results
        with open(rejected_file, 'a', encoding='utf-8') as f:
            for word in rejected_words:
                f.write(word + '\n')

        print(f"Found {len(accepted_words)} valid {x}-letter words using the letters '{base_letters}' containing '{main_letter}' and saved to {output_file}")
        print(f"Rejected {len(rejected_words)} words (likely verbs or plurals) saved to {rejected_file}")

# Run the main function
if __name__ == "__main__":
    main()
