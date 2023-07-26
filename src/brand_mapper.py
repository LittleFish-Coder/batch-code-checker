brand_dict = {
    "品木宣言": ["Origins"],
    "Dior": ["Christian Dior"],
    "赫蓮娜": ["Helena Rubinstein", "HR"],
}


def brand_mapping(brand):
    try:
        return brand_dict[brand]
    except:
        return None


# print(brand_mapping("Dior"))
