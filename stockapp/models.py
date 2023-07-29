from django.db import models


class Product(models.Model):
    brand = models.CharField(verbose_name="品牌", max_length=32, blank=True)
    model = models.CharField(verbose_name="型号", max_length=64)
    quantity = models.IntegerField(verbose_name="库存", default=0)
    period = models.CharField(verbose_name="周期", max_length=32, blank=True)
    creation_time = models.DateTimeField(verbose_name="写入时间", auto_now_add=True)
    source = models.CharField(verbose_name="来源文件", max_length=64, blank=True)
    file_id = models.IntegerField(verbose_name="文件ID", default=-1)

    class Meta:
        unique_together = ['brand', 'model', 'quantity', 'period', 'source']


class ProductFile(models.Model):
    name = models.CharField(verbose_name="文件名", max_length=64)
    size = models.IntegerField(verbose_name="文件大小", )
    checksum = models.CharField(verbose_name="Checksum", max_length=64)
    last_modified_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
