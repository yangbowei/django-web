import hashlib
import re

import pandas as pd

from . import models

COLS = set(['品牌', '型号', '库存', '周期'])
COL_MODEL_NAME = {
    '品牌': 'brand',
    '型号': 'model',
    '库存': 'quantity',
    '周期': 'period'
}


def process_excel_file(file_name, size, file):
    checksum_value = hashlib.file_digest(file, "md5").hexdigest()
    valid_result = validate_file(file_name, size, checksum_value)
    if valid_result is not None:
        return valid_result

    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        df = pd.read_excel(file, header=None)
    elif file_name.endswith('.csv'):
        df = pd.read_csv(file, header=None)

    df = df.dropna(how='all')
    if len(df) <= 1:
        return 'No valid data found in file'
    is_first_row = True
    name_index_map = {}
    quantity_index = -1
    products = []
    for cols in df.itertuples(name=None):
        if is_first_row:
            for i, name in enumerate(cols):
                if name in COLS:
                    name_index_map[i] = name
                    if name == '库存':
                        quantity_index = i

            if len(name_index_map) == 0:
                # no matching columns
                return 'No valid column found in file'
            is_first_row = False
        else:
            product_dict = {}
            for i in name_index_map:
                if i == quantity_index:
                    value = extract_number(cols[i])
                else:
                    value = cols[i]
                product_dict[COL_MODEL_NAME[name_index_map[i]]] = value
            product_dict['source'] = file_name
            products.append(product_dict)

    # save obj
    success = 0
    failure = 0
    failure_messages = []
    for product in products:
        try:
            models.Product.objects.create(**product)
            success += 1
        except Exception as e:
            print(e)
            failure += 1

    file_item = models.ProductFile(name=file_name, size=size, checksum=checksum_value)
    file_item.save()

    return str.format('Succeed loading {} items. Failed to load {} items', success, failure)


def validate_file(file_name, size, checksum_value):
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls') or file_name.endswith('.csv')):
        return "File type not supported"
    if models.ProductFile.objects.filter(checksum=checksum_value).exists():
        return "File has been loaded"
    return None


def extract_number(quantity):
    if isinstance(quantity, int):
        return quantity
    qstring = str(quantity)
    qstring = str(re.search(r"^(\d+)", '123+').group())
    return int(qstring)
