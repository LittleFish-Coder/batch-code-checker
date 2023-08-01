from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from website1 import check_from_cosmetic_momoko
from website2 import check_from_check_fresh
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

    try:
        # transform the first column's data type to str
        df["國際碼"] = df["國際碼"].fillna("").astype(str)
    except:
        pass

    return df


def highlight(df):
    # get the last three columns
    df_last_three_columns = df.iloc[:, -3:]
    # highlight the row if the last three columns are not the same
    df_last_three_columns = df_last_three_columns.style.apply(
        lambda x: ["background: yellow" for v in x]
        if x[0] != x[1] or x[1] != x[2]
        else ["background: white" for v in x],
        axis=1,
    )
    # apply the style to the dataframe
    df.iloc[:, -3:] = df_last_three_columns

    return df


# Read the excel file
df = pd.read_excel("./批號日期.xlsx")
# Fill in the brand names
df = fill_brand(df)

# Open the browser

# for safari user
# safari = webdriver.Safari()
# safari.maximize_window()

# for edge user
edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
# set the browser screen size as 1920x1080
edge_options.add_argument("window-size=1920,1080")
edge_options.add_argument("--headless")  # hide the browser in the background
edge = webdriver.Edge(options=edge_options)

# website1
# df = check_from_cosmetic_momoko(safari, df)
df = check_from_cosmetic_momoko(edge, df)

# website2
# df = check_from_check_fresh(safari, df)
df = check_from_check_fresh(edge, df)

# website3
# df = check_from_cosmetic_calculator(safari, df)
df = check_from_cosmetic_calculator(edge, df)

# Highlight the rows that have different results
# df = highlight(df)

# Save the dataframe to a new excel file
df.to_excel("products_with_date_of_manufacture.xlsx", index=False)

print("Done")

# Close the browser
# safari.quit()
edge.quit()
