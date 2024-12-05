from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def autocomplete(driver):
    # Step 4: Read lines from a file (for example, "filtered_words.txt")
    with open('filtered_words.txt', 'r') as file:
        lines = file.readlines()

    input_box = driver.find_element(By.XPATH, '//*[@id="input"]')
    lista_correta = []  # This should be a list to store correct words
    passes = 0

    while len(lines) > 0 and passes < 9:
        # Loop over each line in the file and process it
        for i, line in enumerate(lines):
            line = line.strip()  # Remove any leading/trailing whitespace

            # Clear the input field before entering a new word
            input_box.clear()

            # Input the line into the input box
            input_box.send_keys(line)

            # Submit by pressing Enter
            input_box.send_keys(Keys.RETURN)

            # Check if the input is valid (if the value in the input box is the same as the word entered)
            if input_box.get_attribute("value") == line:
                lista_correta.append(line)  # Add correct word to the list
                lines.pop(i)  # Remove the line from the list based on its index
            else:
                # If the input is incorrect, clear the input field
                input_box.clear()

            passes += 1
        return lista_correta
