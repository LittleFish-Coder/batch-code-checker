from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from website3 import check_from_cosmetic_calculator
import pandas as pd
import time


def fill_brand(df):
    # Forward-fill the "Brand" column with the previous non-blank value, but only when "Batch" is not empty
    for index, row in df.iterrows():
        if pd.isna(row["品牌"]) and pd.notna(row["批號"]):
            previous_brand = df.at[index - 1, "品牌"]
            if pd.notna(previous_brand):
                df.at[index, "品牌"] = previous_brand

    return df


# Read the excel file
df = pd.read_excel("./批號日期.xlsx")
# Fill in the brand names
df = fill_brand(df)

safari = webdriver.Safari()
safari.maximize_window()

# website1
# on progress ...｀

# website2
# on progress ...

# website3
df = check_from_cosmetic_calculator(safari, df)

# Save the dataframe to a new excel file
df.to_excel("products_with_date_of_manufacture.xlsx", index=False)

# Close the browser
safari.quit()
