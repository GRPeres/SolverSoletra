from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Modulos.dictmaker import update_dictionary
from Modulos.lastResort import lastResort
from Modulos.autocomplete import autocomplete
from Modulos.solver import solve
from Modulos.letterScraping import letters
from Modulos.final_result import final_result
import asyncio
import os

# Step 1: Set up Firefox options
options = Options()

# Step 2: Initialize the WebDriver
driver = webdriver.Firefox(options=options)

# Open the webpage
url = 'https://g1.globo.com/jogos/soletra/'  # Replace with your target URL
driver.get(url)

# Step 3: Wait for the "Iniciar" button to be clickable
start_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Botão responsável por começar o jogo"]'))
)
start_button.click()

# Step 4: Wait for the close popup button to be clickable
close_popup_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@title="Botão responsável por fechar o drawer"]'))
)
close_popup_button.click()

# Step 6: Call the solve function with the letter scrapping as letters variable to obtain letters from site
letras = asyncio.run(solve(letters(driver)))
with open('filtered_words.txt', 'r') as file:
    lines = file.readlines()
autocomplete(driver,lines)

# Step 7: Confirmation step for brute force
confirmation = input("Gostaria de tentar encontrar as palavras restantes por meio de força bruta?(Warning:isso pode demorar horas) (Y/n): ").strip()
if confirmation == 'Y':
    lastResort(driver, letras)
    
    with open('last_resort.txt', 'r') as file:
        brutelines = file.readlines()
    autocomplete(driver, brutelines)
else:
    print("Skipping brute-force step.")

# Step 8: Save correct to a file
final_result(driver)

# Update the dictionary
update_dictionary('br-sem-acentos.txt', 'final_words.txt')

# Deletes Aux Files
if os.path.exists('last_resort.txt'):
    os.remove('last_resort.txt')
    print(f"File '{'last_resort.txt'}' has been deleted.")
else:
    print(f"File '{'last_resort.txt'}' does not exist.")

if os.path.exists('filtered_words.txt'):
    os.remove('filtered_words.txt')
    print(f"File '{'filtered_words.txt'}' has been deleted.")
else:
    print(f"File '{'filtered_words.txt'}' does not exist.")