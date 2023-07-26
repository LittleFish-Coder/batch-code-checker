from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Official brand names
brand_name_list = pd.read_excel("./data/cosmetic_calculator_brand.xlsx")[
    "Brand"
].tolist()
# lowercase the brand names
brand_name_list = [brand_name.lower() for brand_name in brand_name_list]


def check_if_brand_in_cosmetic_calculator(desired_brand):
    # Check if the brand name is in the official brand name list
    if desired_brand.lower() not in brand_name_list:
        print(desired_brand, "is not in the list")
        return False
    else:
        return True


def datetime_parser(date_string):
    months = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12",
    }

    # format type: yyyy-mm-dd
    date_string = date_string.split(",")
    if len(date_string) == 2:  # i.e. "14 of September, 2021"
        day = date_string[0].split(" ")[0]
        month = date_string[0].split(" ")[2]
        # convert month to number
        month = months[month]
        year = date_string[1].strip()
        return f"{year}-{month}-{day}"
    else:
        date_string = date_string[0].split(" ")
        if len(date_string) == 2:  # i.e. "September 2021"
            month = date_string[0]
            # convert month to number
            month = months[month]
            year = date_string[1].strip()
            return f"{year}-{month}"
        else:
            year = date_string[0].strip()
            return year


def check_from_cosmetic_calculator(webdriver, df):
    website_url = "https://checkcosmetic.net"

    # Check if the website is already open in the browser
    if webdriver.current_url != website_url:
        webdriver.get(website_url)
        time.sleep(3)

    results = []

    # iterate through the dataframe
    for index, row in df.iterrows():
        desired_brand = str(row["品牌"])
        desired_code = row["批號"]
        print(f"Brand: {desired_brand}, Batch: {desired_code}")
        result = ""

        # Check if the brand name is in the official brand name list
        if not check_if_brand_in_cosmetic_calculator(desired_brand):
            results.append(result)
            continue

        # Wait for the brand select element to be populated
        wait = WebDriverWait(webdriver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "brandid")))

        # Clear the form fields
        webdriver.find_element(By.ID, "codeinput").clear()
        # Fill in the form fields and submit
        webdriver.find_element(By.ID, "quicksearch").send_keys(desired_brand)
        webdriver.find_element(By.ID, "codeinput").send_keys(desired_code)
        time.sleep(1.5)
        # Wait until the submit button is clickable
        wait.until(EC.element_to_be_clickable((By.ID, "codesubmit")))
        webdriver.find_element(By.ID, "codesubmit").click()

        # Wait for the dynamic content to be populated
        time.sleep(3)
        # Get the content of the "checkResult" element
        check_result_element = webdriver.find_element(By.ID, "checkResult")
        # print(check_result_element.text)

        try:
            # get the span element
            span_element = check_result_element.find_element(By.TAG_NAME, "span")
            date_of_manufacture = span_element.text
            result = datetime_parser(date_of_manufacture)
            print(result)
        except:
            result = ""
            print("No date of manufacture found")

        results.append(result)

    # Export the results to a new column in the dataframe
    df["Cosmetic Calculator"] = results

    return df


# Uncomment the following lines to test the function

# # create a dataframe
# df = pd.DataFrame(
#     {
#         "品牌": ["LANCOME", "Gucci", "NARS"],
#         "批號": ["40UN00", "1326", "2062"],
#     }
# )

# safari = webdriver.Safari()
# safari.maximize_window()

# # Gucci 1326 -> 22 of November, 2021 (2021-11-22)
# # LANCOME 40UN00 -> November 2021 (2021-11)
# # NARS 2062 -> 2022 (2022)
# df = check_from_cosmetic_calculator(safari, df)
# print(df)

# # # Close the browser
# safari.quit()
