import pandas as pd


peiyi = pd.read_excel("./data/peiyi_brand.xlsx")
cosmetic_calculator_brand = pd.read_excel("./data/cosmetic_calculator_brand.xlsx")

peiyi_brand = peiyi["Brand"].tolist()
cosmetic_calculator_brand = cosmetic_calculator_brand["Brand"].tolist()

# make the elements in the list lowercase
peiyi_brand = [x.lower() for x in peiyi_brand]
cosmetic_calculator_brand = [x.lower() for x in cosmetic_calculator_brand]

# print(peiyi_brand)
# print(cosmetic_calculator_brand)

# find the difference between two lists
# https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
diff = list(set(peiyi_brand) - set(cosmetic_calculator_brand))
print(diff)

# find the intersection between two lists
# https://stackoverflow.com/questions/2864842/common-elements-comparison-between-2-lists
# intersection = list(set(peiyi_brand) & set(cosmetic_calculator_brand))
# print(intersection)

# export the difference to excel
df = pd.DataFrame(diff, columns=["Brand"])
df.to_excel("./data/brand_diff.xlsx", index=False)
