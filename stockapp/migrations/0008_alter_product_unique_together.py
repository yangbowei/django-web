# Generated by Django 4.1 on 2023-08-03 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0007_product_hit_point_alter_product_file_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('brand', 'model', 'quantity', 'period', 'file_id')},
        ),
    ]
