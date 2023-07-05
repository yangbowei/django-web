from django.db import models


class Product(models.Model):
    brand = models.CharField(verbose_name="品牌", max_length=32, )
    model = models.CharField(verbose_name="型号", max_length=64)
    quantity = models.IntegerField(verbose_name="库存", default=0)
    period = models.CharField(verbose_name="周期", max_length=32)
    source = models.CharField(verbose_name="来源", max_length=64)
    creation_time = models.DateTimeField(verbose_name="写入时间", auto_now_add=True)


class ProductFile(models.Model):
    name = models.CharField(max_length=64)
    size = models.IntegerField()
    last_modified_time = models.DateTimeField(auto_now=True)
