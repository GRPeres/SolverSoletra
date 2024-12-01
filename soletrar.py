import os
import asyncio
from unidecode import unidecode
from concurrent.futures import ProcessPoolExecutor

# Function to load and process words from a file
async def load_and_process_words(filename, wordsize):
    loop = asyncio.get_event_loop()
    # Read the file in an asynchronous manner (non-blocking IO)
    with open(filename, 'r', encoding='UTF-8') as file:
        lines = await loop.run_in_executor(None, file.readlines)
    
    # Process the lines and filter words based on word size
    words = {unidecode(word.strip().lower()) for word in lines if len(word.strip()) == wordsize}
    return words

# Function to filter words based on the base letters and word size
async def filter_words(base_letters, valid_words, wordsize):
    allowed_letters = set(base_letters)
    filtered_words = [
        word for word in valid_words
        if len(word) == wordsize and all(letter in allowed_letters for letter in word)
    ]
    return filtered_words

# Function to filter words by main letter
async def filter_by_main_letter(words, main_letter):
    return {word for word in words if main_letter in word}

# Function to check if a word is plural or a verb (for rejection)
def maybe_plural(word):
    verb_endings = ['s', 'ei', 'iu', 'ndo']
    return any(word.endswith(ending) for ending in verb_endings)

# Asynchronous function to process all tasks concurrently
async def process_words_for_size(base_letters, main_letter, x, filename):
    valid_words = await load_and_process_words(filename, x)
    
    found_words = await filter_words(base_letters, valid_words, x)
    filtered_by_main_letter = await filter_by_main_letter(found_words, main_letter)
    
    return filtered_by_main_letter

# Function to process and separate accepted and rejected words
def separate_accepted_and_rejected(filtered_words):
    rejected_words = [word for word in filtered_words if maybe_plural(word)]
    accepted_words = [word for word in filtered_words if not maybe_plural(word)]
    return accepted_words, rejected_words

# Function to save words to files
def save_words_to_file(words, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

# Main function
async def main():
    output_file = 'filtered_words.txt'
    rejected_file = 'rejected_words.txt'

    # Delete the output files if they exist
    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(rejected_file):
        os.remove(rejected_file)

    wordsize = 17
    base_letters = input("Enter 7 letters (no spaces): ").strip().lower()
    main_letter = input("Enter the main letter to filter by: ").strip().lower()

    # Use ProcessPoolExecutor to distribute the work of filtering across multiple processes
    with ProcessPoolExecutor() as executor:
        tasks = []
        for x in range(4, wordsize + 1):
            # Schedule processing of words for each word size
            task = asyncio.ensure_future(process_words_for_size(base_letters, main_letter, x, 'br-sem-acentos.txt'))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)

        # Process each word size result
        for filtered_words in results:
            filtered_words = sorted(filtered_words)

            accepted_words, rejected_words = separate_accepted_and_rejected(filtered_words)

            # Save accepted and rejected words to files
            save_words_to_file(accepted_words, output_file)
            save_words_to_file(rejected_words, rejected_file)

            print(f"Found {len(accepted_words)} valid words, saved to {output_file}")
            print(f"Rejected {len(rejected_words)} words (likely verbs or plurals), saved to {rejected_file}")

# Run the main function with asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
