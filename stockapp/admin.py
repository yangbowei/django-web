from django.contrib import admin

from stockapp import models


class ProductAdmin(admin.ModelAdmin):
    # 定制哪些字段需要展示
    list_display = ('brand', 'model', 'quantity', 'period', 'source', 'creation_time')

    '''定义哪个字段可以编辑'''
    # list_editable = ('status',)

    '''分页：每页10条'''
    list_per_page = 20

    '''最大条目'''
    # list_max_show_all = 200  # default

    '''搜索框 ^, =, @, None=icontains'''
    search_fields = ['brand', 'model']


class ProductFileAdmin(admin.ModelAdmin):
    # 定制哪些字段需要展示
    list_display = ('name', 'size', 'last_modified_time', 'checksum',)

    '''定义哪个字段可以编辑'''
    # list_editable = ('status',)

    '''分页：每页10条'''
    list_per_page = 20

    '''最大条目'''
    # list_max_show_all = 200  # default

    '''搜索框 ^, =, @, None=icontains'''
    search_fields = ['name']


# Register your models here.
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductFile, ProductFileAdmin)
