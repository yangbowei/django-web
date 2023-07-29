import configparser


class ConfigReader:

    def __init__(self, file_path='stockapp/config.ini'):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)

    def build_column_name_mapping(self, default_field_to_column_name_mapping):
        """
        default_column_name_mapping: {'brand': '品牌'}
        """
        col_name_to_field_mapping = {}
        for key in default_field_to_column_name_mapping:
            col_name_to_field_mapping[default_field_to_column_name_mapping[key]] = key

        section_name = 'EXCEL'
        if section_name in self.config.sections():
            brand_names = self.config.get(section_name, 'BrandColumnName').split(',')
            for name in brand_names:
                col_name_to_field_mapping[name] = 'brand'

            model_names = self.config.get(section_name, 'ModelColumnName').split(',')
            for name in model_names:
                col_name_to_field_mapping[name] = 'model'

            quantity_names = self.config.get(section_name, 'QuantityColumnName').split(',')
            for name in quantity_names:
                col_name_to_field_mapping[name] = 'quantity'

            period_names = self.config.get(section_name, 'PeriodColumnName').split(',')
            for name in period_names:
                col_name_to_field_mapping[name] = 'period'

        return col_name_to_field_mapping

    def get_product_page_size(self, default_size=25):
        section_name = 'QUERY'
        if section_name in self.config.sections():
            return self.config.get(section_name, 'ProductPageSize', fallback=default_size)
        return default_size


INSTANCE = ConfigReader()
