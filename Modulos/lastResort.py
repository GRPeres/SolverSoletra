from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools
import json
import re

def lastResort(driver,letters):
    print('Known words have been exhausted, starting brute forcing procedure...')
    # Get ALL word-box elements (in order)
    all_elements = driver.find_elements(By.CSS_SELECTOR, 'div.word-box')
    possibilities = {}
    
    for idx, element in enumerate(all_elements):
        if 'found' not in element.get_attribute('class').split():
            # Extract any number from the text
            length_text = element.find_element(By.CLASS_NAME, 'length').text
            numbers_in_text = re.findall(r'\d+', length_text)

            if numbers_in_text:
                word_size = int(numbers_in_text[0])  # Take the first match and convert to int
            else:
                word_size = None  # Handle cases where no number is found
            # Find nearest found neighbors
            lower, upper = find_nearest_found_neighbors(all_elements, idx)
            
            # Filter based on neighbors
            find_combinations(letters,word_size,lower,upper)
            
            
        
def find_nearest_found_neighbors(all_elements, current_index):
    # Search upwards for the LOWER alphabetical bound
    lower = None
    for i in range(current_index - 1, -1, -1):
        if 'found' in all_elements[i].get_attribute('class').split():
            lower = all_elements[i].find_element(By.CLASS_NAME, 'word').text
            break
    
    # Search downwards for the UPPER alphabetical bound
    upper = None
    for i in range(current_index + 1, len(all_elements)):
        if 'found' in all_elements[i].get_attribute('class').split():
            upper = all_elements[i].find_element(By.CLASS_NAME, 'word').text
            break

    return lower, upper 

def is_valid_portuguese_word(word):
    """
    Checks if a word follows Portuguese-specific rules.
    """
    # Rule 1: No three identical letters in succession
    for i in range(len(word) - 2):
        if word[i] == word[i + 1] == word[i + 2]:
            return False
    
    # Rule 2: No two repeated consonants unless they are 'rr' or 'ss'
    consonants = set('bcdfghjklmnpqrstvwxyz')
    for i in range(len(word) - 1):
        if word[i] == word[i + 1] and word[i] in consonants:
            if word[i:i + 2] not in {'rr', 'ss'}:
                return False
    
    # Rule 3: No invalid consonant clusters
    invalid_consonant_clusters = {'bt', 'gd', 'pk', 'qt', 'tm', 'vn'}
    for i in range(len(word) - 1):
        cluster = word[i:i + 2]
        if cluster in invalid_consonant_clusters:
            return False
        
    # Rule 5: No words ending with certain letters
    invalid_endings = {'k', 'w', 'y', 'z'}
    if word[-1] in invalid_endings:
        return False
    
     # Rule 6: No words starting with certain letters
    invalid_starters = {'x'}
    if word[0] in invalid_starters:
        return False
    
    # Rule 7: No words with 'q' not followed by 'u'
    if 'q' in word:
        for i in range(len(word) - 1):
            if word[i] == 'q' and word[i + 1] != 'u':
                return False
    
     # Rule 10: No words with 'h' at the end
    if word[-1] == 'h':
        return False
    
     # Rule 11: No words with invalid syllable structures
    invalid_syllables = {'tl', 'nm'}
    for i in range(len(word) - 1):
        if word[i:i + 2] in invalid_syllables:
            return False
    
    # Rule 12: No words with invalid prefixes or suffixes
    invalid_prefixes_suffixes = {'xk', 'zt'}
    for prefix_suffix in invalid_prefixes_suffixes:
        if word.startswith(prefix_suffix) or word.endswith(prefix_suffix):
            return False
    # If all checks pass, the word is valid
    return True

def find_combinations(letters, word_size, lower_bound, upper_bound):
    if word_size > 5:
        return
    
    # Ensure the first letter in the list is obligatory
    obligatory_letter = letters[0]  # First letter is obligatory
    
    # Normalize bounds to lowercase (if they exist)
    lower_bound = lower_bound.lower() if lower_bound and len(lower_bound) == word_size else None
    upper_bound = upper_bound.lower() if upper_bound and len(upper_bound) == word_size else None
    
    # Generate combinations and filter during creation
    filtered_words = []
    for combination in itertools.product(letters, repeat=word_size):
        word = ''.join(combination).lower()
        
        # Check if the word contains at least one obligatory letter
        if obligatory_letter not in word:
            continue  # Skip words that don't contain the obligatory letter
        
        # Check lower bound
        if lower_bound is not None and word < lower_bound:
            continue  # Skip words below the lower bound
        
        # Check upper bound
        if upper_bound is not None and word > upper_bound:
            continue  # Skip words above the upper bound
        
        # Check if the word follows Portuguese-specific rules
        if not is_valid_portuguese_word(word):
            continue  # Skip words that violate Portuguese rules
        
        # If all checks pass, add the word to the filtered list
        filtered_words.append(word)
    
    # Append the filtered words to the file
    with open('last_resort.txt', 'a', encoding='utf-8') as file:
        for word in filtered_words:
            file.write(word + '\n')
    
    print(f"Added {len(filtered_words)} words to 'last_resort.txt'")