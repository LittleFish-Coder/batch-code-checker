from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import time

safari = webdriver.Safari()
safari.maximize_window()

website_url = "https://www.checkfresh.com/cerave.html"
safari.get(website_url)
time.sleep(3)

# locate the brand element
wait = WebDriverWait(safari, 20)
brand = wait.until(EC.element_to_be_clickable((By.ID, "brandButton")))
brand.click()
time.sleep(0.5)

# find the desired brand
desired_brand = "Lancome"
# select the brand from the dropdown list with desired brand name
brand_list = safari.find_element(By.ID, "brandScroll").find_elements(By.TAG_NAME, "a")
for element in brand_list:
    brand_name = element.text
    if unidecode(brand_name).lower() == desired_brand.lower():
        element.click()
        break

time.sleep(2)

# locate the product S/N input element and input the desired S/N code
desired_code = "40UN00"
code = safari.find_element(By.ID, "frmBatch")
code.clear()
code.send_keys(desired_code)

# locate the check button and click it
check = safari.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
check.click()

time.sleep(3)

# get the result
# for brand_name = lancome and desired_code = 40UN00, the result is "2021-11"
result = safari.find_element(By.ID, "results").text
print(result)

time.sleep(5)

safari.quit()
