from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Modulos.lastResort import find_nearest_found_neighbors
import time

INPUT_DELAY = .3
def autocomplete(driver, lines):
    input_box = driver.find_element(By.ID, 'input')
    lista_correta = []  # List to store correct words

    # Get all word-box elements
    all_elements = driver.find_elements(By.CSS_SELECTOR, 'div.word-box')

    # Loop over each line in the file and process it
    for i, line in enumerate(lines):
        line = line.strip()  # Remove any leading/trailing whitespace

        # Input the line into the input box
        input_box.send_keys(line)
        input_box.send_keys(Keys.RETURN)

        time.sleep(INPUT_DELAY)  # Wait for the game to process the input

        # Check if the word is marked as "found"
        for element in all_elements:
            if line.lower() == element.find_element(By.CLASS_NAME, 'word').text.lower() and 'found' in element.get_attribute('class').split():
                lista_correta.append(line)  # Add correct word to the list
                lines.pop(i)  # Remove the word from the list
                break  # Exit the loop once the word is found

    # After the first pass, filter words to only include those between bounds
    while  len(lines) > 0:
        # Get the indices of unfound words
        unfound_indices = [idx for idx, element in enumerate(all_elements) if 'found' not in element.get_attribute('class').split()]
        if unfound_indices:
            # For each unfound word, find its nearest alphabetical bounds
            filtered_words = []
            for idx in unfound_indices:
                lower, upper = find_nearest_found_neighbors(all_elements, idx)
                # Filter words that fall within the alphabetical bounds
                for word in lines:
                    if (lower is None or word.lower() > lower.lower()) and (upper is None or word.lower() < upper.lower()):
                        filtered_words.append(word)
            # Deduplicate and update the list of words to try
            lines = list(set(filtered_words))

    return lista_correta