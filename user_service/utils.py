def validate_form(brand, prod, alc, net, file):

    fail_str = ""
    brand_nm_list = []
    prod_nm_list = []

    if not brand:

        fail_str = fail_str + " Brand Name cannot be empty."

    else:

        for b in brand.split(" "):

            brand_nm_list.append(b)

    if not prod:

        fail_str = fail_str + " Product Type cannot be empty."

    else:

        for p in prod.split(" "):

            prod_nm_list.append(p)

    if not alc:

        fail_str = fail_str + " Alcohol Percentage cannot be empty."

    if not net:

        fail_str = fail_str + " Net Contents cannot be empty."

    if not file:

        fail_str = fail_str + " An image file must be uploaded."

    return fail_str, brand_nm_list, prod_nm_list


def validate_labels(brand_nm_list, prod_nm_list, alc, net, text):

    flag = False

    for b_nm in brand_nm_list:

        if b_nm not in text:

            flag = True

    if flag:

        fail_str = fail_str + " Brand name is not in image."

    flag = False

    for p_nm in prod_nm_list:

        if p_nm not in text:

            flag = True

    if flag:

        fail_str = fail_str + " Product type is not in image."

    if alc not in text:

        fail_str = fail_str + " Alcohol content is not in image."

    if net not in text:

        fail_str = fail_str + " Net contents is not in image."



    if not fail_str:

        fail_str = "success!"


    fail_str = fail_str + " File must be in appropriate format"

    return fail_str


