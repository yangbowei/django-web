import django_tables2 as tables

from stockapp.models import Product


class ProductTable(tables.Table):
    extra_columns = {"Edit": tables.LinkColumn("edit/")}
    buttons = tables.TemplateColumn(
        template_name="table_button.html", verbose_name="Actions", orderable=False
    )

    class Meta:
        orderable = False
        model = Product
        template_name = "django_tables2/bootstrap5.html"
