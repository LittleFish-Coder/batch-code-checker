import pandas as pd

df = pd.read_excel("./data/批號日期.xlsx")


def fill_brand(df):
    # Forward-fill the "Brand" column with the previous non-blank value, but only when "Batch" is not empty
    for index, row in df.iterrows():
        if pd.isna(row["品牌"]) and pd.notna(row["批號"]):
            previous_brand = df.at[index - 1, "品牌"]
            if pd.notna(previous_brand):
                df.at[index, "品牌"] = previous_brand

    return df


df = fill_brand(df)
print(df)
