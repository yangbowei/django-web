# Generated by Django 4.1 on 2023-07-05 17:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='checksum',
            field=models.CharField(default=datetime.datetime(2023, 7, 6, 1, 29, 14, 899591), max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='写入时间'),
        ),
        migrations.AlterField(
            model_name='product',
            name='source',
            field=models.CharField(max_length=64, null=True, verbose_name='来源'),
        ),
    ]
