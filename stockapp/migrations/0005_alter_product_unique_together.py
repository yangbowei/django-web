# Generated by Django 4.1 on 2023-07-07 05:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('stockapp', '0004_alter_product_brand_alter_product_period'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('brand', 'model', 'quantity', 'period', 'source')},
        ),
    ]