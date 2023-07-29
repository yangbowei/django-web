import django_tables2 as tables
from stockapp.models import Product, ProductFile


class ProductTable(tables.Table):
    # hit_point_column = tables.Column(accessor='hit_point', verbose_name='HotPoint', orderable=True,
    #                                  attrs={
    #                                      "td": {
    #                                          "contenteditable": "true",
    #                                          "class": 'editable_cell',
    #                                          "id": lambda record: record.id
    #                                      }
    #                                  })
    buttons = tables.TemplateColumn(
        template_name="table_button.html", verbose_name="操作", orderable=False
    )

    # overload the init method
    def __init__(self, *args, **kwargs):
        for col in self.base_columns:
            if col == 'hit_point':
                if 'td' not in self.base_columns[col].attrs:
                    self.base_columns[col].attrs['td'] = {}
                self.base_columns[col].attrs['td'].update(
                    {
                        "contenteditable": "true",
                        "class": 'editable_cell',
                        "id": lambda record: record.id
                    })
        # very important! call the parent method
        super(ProductTable, self).__init__(*args, **kwargs)

    class Meta:
        orderable = True
        model = Product
        template_name = "django_tables2/bootstrap5.html"
        exclude = ('id',)


class ProductFileTable(tables.Table):
    extra_columns = {"Delete": tables.LinkColumn("delete/")}
    buttons = tables.TemplateColumn(
        template_name="table_delete_button.html", verbose_name="操作", orderable=False
    )

    class Meta:
        orderable = False
        model = ProductFile
        template_name = "django_tables2/bootstrap5.html"
