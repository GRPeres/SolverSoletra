from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time

# Path to your Firefox profile (make sure to replace with your actual path)
profile_path = r'C:\Users\Gabriel\AppData\Roaming\Mozilla\Firefox\Profiles\y7m5im1a.default-release'

# Step 1: Set up Firefox options to use the profile
options = Options()
#profile = FirefoxProfile(profile_path)

# You can add additional options to run headlessly if you prefer
#options.headless = True  # Uncomment if you don't want the UI to show

# Step 2: Initialize the WebDriver with the profile
driver = webdriver.Firefox(options=options)

# Open the webpage
url = 'https://g1.globo.com/jogos/soletra/'  # Replace with your target URL
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Step 3: Click the "Iniciar" button to start the game
start_button = driver.find_element(By.XPATH, '//button[@class="button button--game-white intro-button svelte-1g6agin" and @title="Botão responsável por começar o jogo"]')
start_button.click()

# Wait for the game to start (you may need to adjust the wait time based on the page behavior)
time.sleep(.1)

close_popup_button = driver.find_element(By.XPATH, '//*[@title="Botão responsável por fechar o drawer"]')
close_popup_button.click()
# Wait for the game to start (you may need to adjust the wait time based on the page behavior)
time.sleep(.1)

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

# Step 6: Close the browser after completing the task
#driver.quit()
