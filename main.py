from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autocomplete import autocomplete
from solver import solve
from letterScraping import letters
import asyncio


# Path to your Firefox profile (make sure to replace with your actual path)
#profile_path = r'your_profile path'

# Step 1: Set up Firefox options to use the profile
options = Options()

# Step 2: Initialize the WebDriver with the profile
driver = webdriver.Firefox(options=options)

# Open the webpage
url = 'https://g1.globo.com/jogos/soletra/'  # Replace with your target URL
driver.get(url)

# Step 3: Wait for the "Iniciar" button to be clickable
start_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@class="button button--game-white intro-button svelte-1g6agin" and @title="Botão responsável por começar o jogo"]'))
)
start_button.click()

# Step 4: Wait for the close popup button to be clickable
close_popup_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@title="Botão responsável por fechar o drawer"]'))
)
close_popup_button.click()

# Step 6: Call the solve function with the letter scrapping as letters variable to obtain letters from site
asyncio.run(solve(letters(driver)))

# Step 7: Call autocomplete function
autocomplete(driver)
