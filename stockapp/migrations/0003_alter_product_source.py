# Generated by Django 4.1 on 2023-07-05 17:32

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stockapp', '0002_productfile_checksum_alter_product_creation_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='source',
            field=models.CharField(blank=True, default=datetime.datetime(2023, 7, 6, 1, 32, 50, 620940), max_length=64,
                                   verbose_name='来源'),
            preserve_default=False,
        ),
    ]
