import pandas as pd
from unidecode import unidecode

peiyi = pd.read_excel("./data/peiyi_brand.xlsx")
cosmetic_momoko_brand = pd.read_excel("./data/cosmetic_momoko_brand.xlsx")
check_fresh_brand = pd.read_excel("./data/check_fresh_brand.xlsx")
cosmetic_calculator_brand = pd.read_excel("./data/cosmetic_calculator_brand.xlsx")

peiyi_brand = peiyi["Brand"].tolist()
cosmetic_momoko_brand = cosmetic_momoko_brand["Brand"].tolist()
check_fresh_brand = check_fresh_brand["Brand"].tolist()
cosmetic_calculator_brand = cosmetic_calculator_brand["Brand"].tolist()

# make the elements in the list lowercase
peiyi_brand = [x.lower() for x in peiyi_brand]
cosmetic_momoko_brand = [x.lower() for x in cosmetic_momoko_brand]
check_fresh_brand = [x.lower() for x in check_fresh_brand]
cosmetic_calculator_brand = [x.lower() for x in cosmetic_calculator_brand]

# print(peiyi_brand)
# print(cosmetic_momoko_brand)
# print(check_fresh_brand)
# print(cosmetic_calculator_brand)

# find the difference between two lists
# https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
peiyi_minus_cosmetic_momoko = list(set(peiyi_brand) - set(cosmetic_momoko_brand))
peiyi_minus_check_fresh = list(set(peiyi_brand) - set(check_fresh_brand))
peiyi_minus_cosmetic_calculator = list(
    set(peiyi_brand) - set(cosmetic_calculator_brand)
)

# Find the maximum length of all lists
max_length = max(
    len(peiyi_minus_cosmetic_momoko),
    len(peiyi_minus_check_fresh),
    len(peiyi_minus_cosmetic_calculator),
)

# Extend lists to match the maximum length by filling with None or np.nan
peiyi_minus_cosmetic_momoko.extend(
    [None] * (max_length - len(peiyi_minus_cosmetic_momoko))
)
peiyi_minus_check_fresh.extend([None] * (max_length - len(peiyi_minus_check_fresh)))
peiyi_minus_cosmetic_calculator.extend(
    [None] * (max_length - len(peiyi_minus_cosmetic_calculator))
)

# find the intersection between two lists
# https://stackoverflow.com/questions/2864842/common-elements-comparison-between-2-lists
# intersection = list(set(peiyi_brand) & set(cosmetic_calculator_brand))
# print(intersection)

# export the difference to excel
df = pd.DataFrame(
    {
        "peiyi與cosmetic_momoko的差集": peiyi_minus_cosmetic_momoko,
        "peiyi與check_fresh的差集": peiyi_minus_check_fresh,
        "peiyi與cosmetic_calculator的差集": peiyi_minus_cosmetic_calculator,
    }
)

df.to_excel("./data/brand_diff.xlsx", index=False)
