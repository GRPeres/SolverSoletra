from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time

def autocomplete(driver):
    # Step 4: Read lines from a file (for example, "input_lines.txt")
    with open('filtered_words.txt', 'r') as file:
        lines = file.readlines()

    # Step 5: Input each line and handle guesses
    input_box = driver.find_element(By.XPATH, '//*[@id="input"]') # Replace with the actual input field locator

    for line in lines:
        line = line.strip()  # Remove any leading/trailing whitespace
    
        # Input the line into the input box
        input_box.send_keys(line)
    
        # Submit by pressing Enter
        input_box.send_keys(Keys.RETURN)
    
        # Wait for some time for the response (adjust this as necessary)
        time.sleep(.15)

        # If the input is wrong and needs to be cleared, press Backspace to clear
        # (This part depends on your website's behavior — modify if necessary)
        input_box.send_keys(Keys.BACKSPACE * len(line))  # Clears the input field

        # Wait for some time for the response (adjust this as necessary)
        time.sleep(.01)


