from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def check_from_cosmetic_calculator(webdriver, desired_brand, desired_code):
    website_url = "https://checkcosmetic.net"

    # Check if the website is already open in the browser
    if webdriver.current_url != website_url:
        webdriver.get(website_url)
        time.sleep(3)

    # Wait for the brand select element to be populated
    wait = WebDriverWait(webdriver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "brandid")))

    # Clear the form fields
    webdriver.find_element(By.ID, "codeinput").clear()
    # Fill in the form fields and submit
    webdriver.find_element(By.ID, "quicksearch").send_keys(desired_brand)
    webdriver.find_element(By.ID, "codeinput").send_keys(desired_code)
    time.sleep(1)
    # Click the submit button
    webdriver.find_element(By.ID, "codesubmit").click()

    # Wait for the dynamic content to be populated
    time.sleep(3)
    # Get the content of the "checkResult" element
    check_result_element = webdriver.find_element(By.ID, "checkResult")
    # print(check_result_element.text)

    result = ""

    try:
        # get the span element
        span_element = check_result_element.find_element(By.TAG_NAME, "span")
        date_of_manufacture = span_element.text
        print(date_of_manufacture)
        result = date_of_manufacture
    except:
        print("No date of manufacture found")
        result = ""

    return result


# Uncomment the following lines to test the function

# safari = webdriver.Safari()
# safari.maximize_window()

# check_from_cosmetic_calculator(safari, "ORIGINS", "DB1")
# check_from_cosmetic_calculator(safari, "NARS", "2062")

# # Close the browser
# safari.quit()
