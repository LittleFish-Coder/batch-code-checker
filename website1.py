from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from unidecode import unidecode

# Official brand names
brand_name_df = pd.read_excel("./data/cosmetic_momoko_brand.xlsx")
brand_name_list = brand_name_df["Brand"].tolist()
brand_name_chinese_list = brand_name_df["Brand Chinese"].tolist()
# lowercase the brand names
brand_name_list = [unidecode(brand_name).lower() for brand_name in brand_name_list]


def check_if_brand_in_cosmetic_momoko(desired_brand):
    # Check if the brand name is in the official brand name list
    if (
        unidecode(desired_brand).lower() in brand_name_list
        or desired_brand in brand_name_chinese_list
    ):
        return True
    else:
        print(desired_brand, "is not in the list")
        return False


def datetime_parser(date_string):
    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    # format type: yyyy-mm-dd
    date_string = date_string.strip().split(" ")
    if len(date_string) == 3:  # i.e. "22 Nov 2021"
        day = date_string[0]
        month = date_string[1]
        # convert month to number
        month = months[month]
        year = date_string[2]
        return f"{year}-{month}-{day}"
    elif len(date_string) == 2:  # i.e. "Nov 2021"
        month = date_string[0]
        # convert month to number
        month = months[month]
        year = date_string[1]
        return f"{year}-{month}"
    else:  # i.e. "2022"
        year = date_string[0]
        return year


def check_from_cosmetic_momoko(webdriver, df):
    print("Checking from Cosmetic Momoko")
    website_url = "https://cosmetic.momoko.hk/zh"

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
        if not check_if_brand_in_cosmetic_momoko(desired_brand):
            results.append(result)
            continue

        # locate the brand element
        wait = WebDriverWait(webdriver, 20)
        brand = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input-select")))
        brand.click()
        time.sleep(0.5)

        # select the brand from the dropdown list with desired brand name
        brand_list = webdriver.find_elements(By.CSS_SELECTOR, "[data-selectable]")
        for element in brand_list:
            brand_name = element.find_element(By.CLASS_NAME, "name").text  # for English
            brand_name_long = element.find_element(
                By.CLASS_NAME, "long-name"
            ).text  # for Chinese
            # print(brand_name)
            if (
                unidecode(brand_name).lower() == unidecode(desired_brand).lower()
                or brand_name_long == desired_brand
            ):
                element.click()
                break

        # locate the product S/N input element and input the desired S/N batch code
        code = webdriver.find_element(By.ID, "code")
        code.clear()
        code.send_keys(desired_code)

        # locate the check button and click it
        check = webdriver.find_element(By.ID, "btn-check")
        check.click()
        time.sleep(3)

        # get the result
        check_result_element = webdriver.find_element(By.ID, "msg")
        # print(check_result_element.text)

        try:
            # if the result is correct, there will be a strong element
            strong_tag = check_result_element.find_element(By.TAG_NAME, "strong")
            date_of_manufacture = strong_tag.text
            # print(date_of_manufacture)
            result = datetime_parser(date_of_manufacture)
            print(result)
        except:
            result = ""
            print("No date of manufacture found")

        # close the msg window
        close = webdriver.find_element(
            By.CLASS_NAME, "fancybox-button.fancybox-close-small"
        )
        close.click()
        time.sleep(1)

        results.append(result)

    # Export the results to a new column in the dataframe
    df["Cosmetic Momoko"] = results

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

# # LANCOME 40UN00 -> Nov 2021 (2021-11)
# # Gucci 1326 -> 22 Nov 2021 (2021-11-22)
# # NARS 2062 -> 2022 (2022)
# df = check_from_cosmetic_momoko(safari, df)
# print(df)

# # Close the browser
# safari.quit()
