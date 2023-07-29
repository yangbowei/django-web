import configparser
import hashlib
import re
import pandas as pd
from . import models


DEFAULT_COL_MODEL_NAME = {
    'brand': '品牌',
    'model': '型号',
    'quantity': '库存',
    'period': '周期'
}


def build_column_name_mapping():
    col_name_to_field_mapping = {}
    for key in DEFAULT_COL_MODEL_NAME:
        col_name_to_field_mapping[DEFAULT_COL_MODEL_NAME[key]] = key

    config = configparser.ConfigParser()
    read_ok = config.read('stockapp/config.ini')

    section_name = 'EXCEL'
    if section_name in config.sections():
        brand_names = config.get(section_name, 'BrandColumnName').split(',')
        for name in brand_names:
            col_name_to_field_mapping[name] = 'brand'

        model_names = config.get(section_name, 'ModelColumnName').split(',')
        for name in model_names:
            col_name_to_field_mapping[name] = 'model'

        quantity_names = config.get(section_name, 'QuantityColumnName').split(',')
        for name in quantity_names:
            col_name_to_field_mapping[name] = 'quantity'

        period_names = config.get(section_name, 'PeriodColumnName').split(',')
        for name in period_names:
            col_name_to_field_mapping[name] = 'period'

    return col_name_to_field_mapping


def process_excel_file(file_name, size, file):
    """
    @return success, message
    """

    checksum_value = hashlib.file_digest(file, "md5").hexdigest()
    valid_result = validate_file(file_name, size, checksum_value)
    if valid_result is not None:
        return False, valid_result

    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        df = pd.read_excel(file, header=None)
    elif file_name.endswith('.csv'):
        df = pd.read_csv(file, header=None)

    df = df.dropna(how='all')
    df = df.drop_duplicates()
    if len(df) <= 1:
        return False, 'No valid data found in file'
    is_first_row = True
    name_index_map = {}
    quantity_index = -1
    products = []

    col_name_to_field_mapping = build_column_name_mapping()
    for cols in df.itertuples(name=None):
        if is_first_row:
            for i, name in enumerate(cols):
                if name in col_name_to_field_mapping:
                    name_index_map[i] = col_name_to_field_mapping[name]
                    if col_name_to_field_mapping[name] == 'quantity':
                        quantity_index = i

            if len(name_index_map) == 0:
                # no matching columns
                return False, 'No valid column found in file'
            is_first_row = False
        else:
            product_dict = {}
            for i in name_index_map:
                if i == quantity_index:
                    value = extract_number(cols[i])
                else:
                    value = cols[i]
                product_dict[name_index_map[i]] = value
            product_dict['source'] = file_name
            products.append(product_dict)

    # save obj
    prod_data = [models.Product(**product) for product in products]
    objs = models.Product.objects.bulk_create(prod_data, ignore_conflicts=True)
    file_item = models.ProductFile(name=file_name, size=size, checksum=checksum_value)
    file_item.save()

    return True, len(objs)


def validate_file(file_name, size, checksum_value):
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls') or file_name.endswith('.csv')):
        return "文件类型不支持，支持类型：xlsx, xls, csv"
    if models.ProductFile.objects.filter(checksum=checksum_value).exists():
        return "该文件已经导入过了"
    return None


def extract_number(quantity):
    if isinstance(quantity, int):
        return quantity
    qstring = str(quantity)
    qstring = str(re.search(r"^(\d+)", '123+').group())
    return int(qstring)
