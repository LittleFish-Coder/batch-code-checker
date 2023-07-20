from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

counter = 0


def highlight(row):
    print(row["Website1"], row["Website2"])
    if row["Website1"] != row["Website2"]:
        return ["background-color: yellow"] * len(row)
    else:
        return ["background-color: white"] * len(row)


def check_from_website_1(desired_brand, desired_batch, counter):
    if counter == 0:
        website_url = "https://cosmetic.momoko.hk/zh"
        safari.get(website_url)
        time.sleep(3)
    # locate the brand element
    brand = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input-select")))
    brand.click()
    time.sleep(0.5)
    # select the brand from the dropdown list with desired brand name
    brand_list = safari.find_elements(By.CSS_SELECTOR, "[data-selectable]")
    for element in brand_list:
        brand_name = element.find_element(By.CLASS_NAME, "name")
        brand_name = brand_name.text
        if brand_name.lower() == desired_brand.lower():
            element.click()
            break
    # locate the product S/N input element and input the desired S/N batch code
    code = safari.find_element(By.ID, "code")
    code.clear()
    code.send_keys(desired_batch)
    # locate the check button and click it
    check = safari.find_element(By.ID, "btn-check")
    check.click()
    time.sleep(3)
    # get the result
    result = safari.find_element(By.ID, "msg")
    result = result.text
    print(result)
    # close the result window
    close = safari.find_element(By.CLASS_NAME, "fancybox-button.fancybox-close-small")
    close.click()
    time.sleep(1)

    return result


def check_from_website_2(desired_brand, desired_batch, counter):
    if counter == 0:
        website_url = "https://www.checkfresh.com/cerave.html?lang=en"
        safari.get(website_url)
        time.sleep(3)
    # locate the brand element
    brand = wait.until(EC.element_to_be_clickable((By.ID, "brandButton")))
    brand.click()
    time.sleep(0.5)
    # select the brand from the dropdown list with desired brand name
    brand_list = safari.find_element(By.ID, "brandScroll").find_elements(
        By.TAG_NAME, "a"
    )
    for element in brand_list:
        brand_name = element.text
        if brand_name.lower() == desired_brand.lower():
            element.click()
            break
    time.sleep(2)
    # locate the product S/N input element and input the desired S/N batch code
    code = safari.find_element(By.ID, "frmBatch")
    code.clear()
    code.send_keys(desired_batch)
    # locate the check button and click it
    check = safari.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    check.click()
    time.sleep(2)
    # get the result
    result = safari.find_element(By.ID, "results")
    result = result.text
    print(result)

    return result


def check_product():
    global counter
    df = pd.read_excel("products.xlsx")
    results_from_website_1 = []
    results_from_website_2 = []
    for i in range(len(df)):
        desired_brand = df["Brand"][i]
        desired_batch = df["Batch"][i]
        # print(desired_brand, desired_batch)
        result = check_from_website_1(desired_brand, desired_batch, counter)
        results_from_website_1.append(result)
        counter += 1
    counter = 0
    for i in range(len(df)):
        desired_brand = df["Brand"][i]
        desired_batch = df["Batch"][i]
        # print(desired_brand, desired_batch)
        result = check_from_website_2(desired_brand, desired_batch, counter)
        results_from_website_2.append(result)
        counter += 1

    results = df.copy()
    results["Website1"] = results_from_website_1
    results["Website2"] = results_from_website_2
    print(results)
    results = results.style.apply(highlight, axis=1)
    results.to_excel("results.xlsx")
    return None


safari = webdriver.Safari()
safari.maximize_window()
wait = WebDriverWait(safari, 20)
check_product()

safari.quit()
