from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def final_result(driver):
    # Locate all <div> elements with class 'word-box' and 'found'
    found_elements = driver.find_elements(By.CSS_SELECTOR, 'div.word-box.found')
    # Extract the text from these elements
    found_texts = [element.text for element in found_elements]

    # Save the extracted texts to a file
    with open('final_words.txt', 'w', encoding='utf-8') as file:
        for text in found_texts:
            file.write(text + '\n')

    # Close the WebDriver
    driver.quit()

    print(f"Saved {len(found_texts)} found words to 'final_words.txt'.")
