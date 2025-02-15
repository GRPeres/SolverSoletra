from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Asynchronous function to process all tasks concurrently
async def process_words_for_size(base_letters, main_letter, x, filename):
    valid_words = await load_and_process_words(filename, x)
    
    found_words = await filter_words(base_letters, valid_words, x)
    filtered_by_main_letter = await filter_by_main_letter(found_words, main_letter)
    
    return filtered_by_main_letter

# Function to save words to files
def save_words_to_file(words, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

# Main function
async def solve(base_letters):

    WORDSIZE = 17

    output_file = 'filtered_words.txt'

    # Delete the output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Print out the extracted letters
    print("Extracted letters:", base_letters)
    main_letter = base_letters[0]
    # Print out the extracted letters
    print("Main letters:", main_letter)

    # Use ProcessPoolExecutor to distribute the work of filtering across multiple processes
    with ProcessPoolExecutor() as executor:
        tasks = []
        for x in range(4, WORDSIZE + 1):
            # Schedule processing of words for each word size
            task = asyncio.ensure_future(process_words_for_size(base_letters, main_letter, x, 'br-sem-acentos.txt'))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)

        # Process each word size result
        all_filtered_words = []
        for filtered_words in results:
            all_filtered_words.extend(filtered_words)

        # Save all filtered words to the output file
        save_words_to_file(sorted(all_filtered_words), output_file)

        print(f"Found {len(all_filtered_words)} valid words, saved to {output_file}")

    return base_letters
