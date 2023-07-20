from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

safari = webdriver.Safari()
safari.maximize_window()

url = "https://checkcosmetic.net"

# Navigate to the page
safari.get(url)

# Wait for the brand select element to be populated
wait = WebDriverWait(safari, 10)
wait.until(EC.presence_of_element_located((By.ID, "brandid")))

# brand info
brandid = "NARS"
code = "2062"
brandid = "ORIGINS"
code = "DB1"

# Fill in the form fields and submit
safari.find_element(By.ID, "quicksearch").send_keys(brandid)
safari.find_element(By.ID, "codeinput").send_keys(code)
safari.find_element(By.ID, "codesubmit").click()

# Wait for the checkResult element to be populated
time.sleep(0.5)
wait.until(EC.presence_of_element_located((By.ID, "checkResult")))

# Get the content of the "checkResult" element
check_result_element = safari.find_element(By.ID, "checkResult")
print(check_result_element.text)

# Close the browser
safari.quit()
