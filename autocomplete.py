from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def autocomplete(driver):
    # Step 4: Read lines from a file (for example, "filtered_words.txt")
    with open('filtered_words.txt', 'r') as file:
        lines = file.readlines()

    # Step 5: Input each line and handle guesses
    input_box = driver.find_element(By.XPATH, '//*[@id="input"]')  # Replace with the actual input field locator

    passes = 0
    while(len(lines)!=0 or passes < 9):
        # Loop over each line in the file and process it
        for i, line in enumerate(lines):
            line = line.strip()  # Remove any leading/trailing whitespace

            # Input the line into the input box
            input_box.send_keys(line)

            # Submit by pressing Enter
            input_box.send_keys(Keys.RETURN)

            # After the toast disappears or after some delay, check if input is wrong
            # (Assuming you have a way to wait for the toast or some other indication of success/failure)
            # For example, you might need to wait for a toast or use an explicit wait here

            # Wait a little or check some element to confirm if input was valid or not
            if input_box.get_attribute("value") != line:
                # If the input is wrong and needs to be cleared, press Backspace to clear (if necessary)
                input_box.send_keys(Keys.BACKSPACE * len(input_box.get_attribute("value")))  # Clears the input field
            else:
                # Remove the line from the list if it's wrong
                lines.pop(i)  # Remove the line from the list based on its index
            passes += 1