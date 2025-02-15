from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import asyncio
from unidecode import unidecode
from concurrent.futures import ProcessPoolExecutor

def letters(driver):
    
    letters_elements = driver.execute_script("""
    var elements = document.querySelectorAll('.cell-letter');
    var textContentArray = [];
    elements.forEach(function(element) {
        textContentArray.push(element.textContent);
    });
    return textContentArray;
    """)

    base_letters =  [letter for letter in letters_elements]
    return base_letters