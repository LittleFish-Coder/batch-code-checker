from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import pandas as pd
import time

# Official brand names
brand_name_list = pd.read_excel("./data/cosmetic_calculator_brand.xlsx")[
    "Brand"
].tolist()
# lowercase the brand names
brand_name_list = [unidecode(brand_name).lower() for brand_name in brand_name_list]

brand_dict = {
    "品木宣言": "Origins",
    "DIOR": "Christian Dior",
    "赫蓮娜": "Helena Rubinstein",
    "YSL": "Yves Saint Laurent",
}


def brand_mapping(deired_brand):
    # return the mapped brand name if the brand name is in the dictionary
    # otherwise, return the original brand name
    return brand_dict.get(deired_brand, deired_brand)


def check_if_brand_in_cosmetic_calculator(desired_brand):
    # Check if the brand name is in the official brand name list
    if unidecode(desired_brand).lower() not in brand_name_list:
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
        day = date_string[0].split(" ")[0].zfill(2)  # Ensure 2 digits for day i.e. 01
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
    print("Checking from Cosmetic Calculator")
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
        # Convert the brand name to the official brand name
        desired_brand = brand_mapping(desired_brand)
        print(f"Brand: {desired_brand}, Batch: {desired_code}")
        result = ""

        # Check if the brand name is in the official brand name list
        if not check_if_brand_in_cosmetic_calculator(desired_brand):
            results.append(result)
            continue

        try:
            # Wait for the brand select element to be populated
            wait = WebDriverWait(webdriver, 20)
            wait.until(EC.presence_of_element_located((By.ID, "brandid")))

            # Clear the form fields
            webdriver.find_element(By.ID, "codeinput").clear()
            # Fill in the form fields and submit
            webdriver.find_element(By.ID, "quicksearch").send_keys(desired_brand)
            webdriver.find_element(By.ID, "codeinput").send_keys(desired_code)
            time.sleep(1)
            # Wait until the submit button is clickable
            wait.until(EC.element_to_be_clickable((By.ID, "codesubmit")))
            webdriver.find_element(By.ID, "codesubmit").click()
            # Wait for the dynamic content to be populated
            time.sleep(2)

            # Get the content of the "checkResult" element
            check_result_element = webdriver.find_element(By.ID, "checkResult")
            # print(check_result_element.text)

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

# # for safari user
# # safari = webdriver.Safari()
# # safari.maximize_window()

# # for edge user
# edge_options = webdriver.EdgeOptions()
# edge_options.use_chromium = True
# # set the browser screen size as 1920x1080
# edge_options.add_argument("window-size=1920,1080")
# edge_options.add_argument("--headless")  # hide the browser in the background
# edge = webdriver.Edge(options=edge_options)

# # LANCOME 40UN00 -> November 2021 (2021-11)
# # Gucci 1326 -> 22 of November, 2021 (2021-11-22)
# # NARS 2062 -> 2022 (2022)
# df = check_from_cosmetic_calculator(edge, df)
# print(df)

# # Close the browser
# edge.quit()
