from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import time

safari = webdriver.Safari()
safari.maximize_window()

website_url = "https://cosmetic.momoko.hk/zh"
safari.get(website_url)
time.sleep(3)

# locate the brand element
wait = WebDriverWait(safari, 20)
brand = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input-select")))
brand.click()
time.sleep(0.5)

# select the brand from the dropdown list with desired brand name
desired_brand = "Lancome"
brand_list = safari.find_elements(By.CSS_SELECTOR, "[data-selectable]")
for element in brand_list:
    brand_name = element.find_element(By.CLASS_NAME, "name").text  # for English
    brand_name_long = element.find_element(
        By.CLASS_NAME, "long-name"
    ).text  # for Chinese
    # print(brand_name)
    if (
        unidecode(brand_name).lower() == desired_brand.lower()
        or brand_name_long == desired_brand
    ):
        element.click()
        break

# locate the product S/N input element and input the desired S/N batch code
desired_batch = "40UN00"
code = safari.find_element(By.ID, "code")
code.clear()
code.send_keys(desired_batch)

# locate the check button and click it
check = safari.find_element(By.ID, "btn-check")
check.click()
time.sleep(3)

# get the result
result = safari.find_element(By.ID, "msg")
result = (
    result.text
)  # for brand_name = lancome and desired_code = 40UN00, the result is "NOV 2021"
print(result)
# close the result window
close = safari.find_element(By.CLASS_NAME, "fancybox-button.fancybox-close-small")
close.click()
time.sleep(1)


safari.quit()
