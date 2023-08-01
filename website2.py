from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import pandas as pd
import time

# Official brand names
brand_name_list = pd.read_excel("./data/check_fresh_brand.xlsx")["Brand"].tolist()
# lowercase the brand names
brand_name_list = [unidecode(brand_name).lower() for brand_name in brand_name_list]

brand_dict = {
    "品木宣言": "Origins",
    "DIOR": "Christian Dior",
    "MAISON MARGIELA": "Maison Margiela Fragrances",
    "赫蓮娜": "Helena Rubinstein",
    "YSL": "Yves Saint Laurent",
}


def brand_mapping(deired_brand):
    # return the mapped brand name if the brand name is in the dictionary
    # otherwise, return the original brand name
    return brand_dict.get(deired_brand, deired_brand)


def check_if_brand_in_check_fresh(desired_brand):
    # Check if the brand name is in the official brand name list
    if unidecode(desired_brand).lower() not in brand_name_list:
        print(desired_brand, "is not in the list")
        return False
    else:
        return True


def check_from_check_fresh(webdriver, df):
    print("Checking from Check Fresh")
    website_url = "https://www.checkfresh.com/cerave.html"

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
        if not check_if_brand_in_check_fresh(desired_brand):
            results.append(result)
            continue

        try:
            # locate the brand element
            wait = WebDriverWait(webdriver, 20)
            brand = wait.until(EC.element_to_be_clickable((By.ID, "brandButton")))
            brand.click()
            time.sleep(0.5)

            # select the brand from the dropdown list with desired brand name
            brand_list = webdriver.find_element(By.ID, "brandScroll").find_elements(
                By.TAG_NAME, "a"
            )
            for element in brand_list:
                brand_name = element.text
                if unidecode(brand_name).lower() == desired_brand.lower():
                    element.click()
                    time.sleep(0.5)
                    break
            # wait for the page to load
            time.sleep(2)

            # locate the product S/N input element and input the desired S/N code
            code = webdriver.find_element(By.ID, "frmBatch")
            code.clear()
            code.send_keys(desired_code)
            # locate the check button and click it
            check = webdriver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            check.click()
            # wait for the page to load
            time.sleep(2)

            # Get the content of the "results" element
            results_element = webdriver.find_element(By.ID, "results")
            # print(results_element.text)

            # if the result is correct, there will be a table, if there are more than one table, get the first one
            results_table = results_element.find_element(By.TAG_NAME, "table")
            # then get the second td of the thrid tr
            td_element = results_table.find_elements(By.TAG_NAME, "tr")[
                2
            ].find_elements(By.TAG_NAME, "td")[1]
            date_of_manufacture = td_element.text
            result = date_of_manufacture
            print(result)
        except:
            result = ""
            print("No date of manufacture found")

        results.append(result)

    # Export the results to a new column in the dataframe
    df["Check Fresh"] = results

    return df


# Uncomment the following lines to test the function

# # create a dataframe
# df = pd.DataFrame(
#     {
#         "品牌": ["LANCOME", "Gucci", "NARS"],
#         "批號": ["40UN00", "2062", "2062"],
#     }
# )

# safari = webdriver.Safari()
# safari.maximize_window()

# # LANCOME 40UN00 -> 2021-11
# # Gucci 1326 -> 2021-11-22
# # NARS 2062 -> 2022-03-03
# df = check_from_check_fresh(safari, df)
# print(df)

# # Close the browser
# safari.quit()
