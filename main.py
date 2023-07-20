from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Read the excel file
df = pd.read_excel("products.xlsx")

# Official brand names
brand_name_list = pd.read_excel("./data/cosmetic_calculator_brand.xlsx")[
    "Brand"
].tolist()
# lowercase the brand names
brand_name_list = [brand_name.lower() for brand_name in brand_name_list]

# Create a list to store the results
results = []

# Create a browser instance
safari = webdriver.Safari()
safari.maximize_window()
url = "https://checkcosmetic.net"
# Navigate to the page
safari.get(url)
time.sleep(3)
# Wait for the brand select element to be populated
wait = WebDriverWait(safari, 10)
wait.until(EC.presence_of_element_located((By.ID, "brandid")))

# iterate through the dataframe
for index, row in df.iterrows():
    brandid = row["Brand"]
    code = row["Batch"]
    # print(brandid, code)

    # Check if the brand name is in the official brand name list
    if brandid.lower() not in brand_name_list:
        print(f"{brandid} is not in the official brand name list")
        results.append("N/A")
        continue

    # Fill in the form fields and submit
    safari.find_element(By.ID, "quicksearch").send_keys(brandid)
    safari.find_element(By.ID, "codeinput").send_keys(code)
    time.sleep(1)
    safari.find_element(By.ID, "codesubmit").click()
    # Clear the form fields
    safari.find_element(By.ID, "codeinput").clear()

    # Wait for the dynamic content to be populated
    time.sleep(3)
    # Get the content of the "checkResult" element
    check_result_element = safari.find_element(By.ID, "checkResult")
    # print(check_result_element.text)

    try:
        # get the span element
        span_element = check_result_element.find_element(By.TAG_NAME, "span")
        date_of_manufacture = span_element.text
        print(date_of_manufacture)
        results.append(date_of_manufacture)
    except:
        print("No date of manufacture found")
        results.append("N/A")


# Close the browser
safari.quit()

# Export the results to a new column in the dataframe
df["Date of Manufacture"] = results

# Save the dataframe to a new excel file
df.to_excel("products_with_date_of_manufacture.xlsx", index=False)
