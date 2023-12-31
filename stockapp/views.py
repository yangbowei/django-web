import json

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django_tables2 import RequestConfig

from . import configreader
from . import filters
from . import forms
from . import models
from . import tables


# Create your views here.
def index(req):
    return HttpResponse("Hello!")


def get_product(request):
    product_list = models.Product.objects.all()
    f = filters.ProductFilter(request.GET, queryset=product_list)
    table = tables.ProductTable(data=f.qs)
    RequestConfig(request).configure(table)
    page_size = configreader.INSTANCE.get_product_page_size(default_size=25)
    table.paginate(page=request.GET.get("page", 1), per_page=page_size)
    table.attrs.update({"class": "table table-striped table-bordered"})
    return render(request, "products.html", {"table": table, "filter": f})


def add_product(request):
    if request.method == "GET":
        form = forms.ProductModelForm()
        return render(request, 'add_product.html', {"form": form})

    # Post
    form = forms.ProductModelForm(data=request.POST)
    if not form.is_valid():
        print(form.errors)
    else:
        form.save()
        return redirect(get_product)


"""
# Deprecated. use FileFieldFormView instead.
def add_products(request):
    if request.method == "POST":
        form = forms.UploadProductFileForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('file'):
                success, result_msg = processor.process_excel_file(file.name, file.size, file.file)
                if success:
                    m = str.format('成功导入{}条数据，文件："{}"', result_msg, file.name)
                    messages.success(request, m)
                else:
                    m = str.format('导入失败，原因：{}。文件："{}"', result_msg, file.name)
                    messages.error(request, m)
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = forms.UploadProductFileForm()
        return render(request, "add_products.html", {"form": form})
"""


def edit_product(request, uid):
    prod_info = models.Product.objects.filter(id=uid).first()

    if request.method == "GET":
        form = forms.ProductModelForm(instance=prod_info)
        return render(request, 'edit_product.html', {"form": form})

    # Post
    form = forms.ProductModelForm(data=request.POST, instance=prod_info)
    if form.is_valid():
        form.save()
        return redirect(get_product)
    else:
        return render(request, 'edit_product.html', {"form": form})


def delete_product(request, uid):
    models.Product.objects.filter(id=uid).delete()
    return redirect(get_product)


def delete_all_products(request):
    product_file_count = models.ProductFile.objects.count()
    if product_file_count == 0:
        messages.info(request, "没有文件")
        return redirect(request.META['HTTP_REFERER'])

    product_count = models.Product.objects.count()
    models.ProductFile.objects.all().delete()
    models.Product.objects.all().delete()
    messages.success(request, str.format('来自{}个文件的{}条数据已被删除!', product_file_count, product_count))
    return redirect(request.META['HTTP_REFERER'])


def product_files(request):
    file_list = models.ProductFile.objects.all()
    table = tables.ProductFileTable(file_list)
    table.paginate(page=request.GET.get("page", 1), per_page=configreader.INSTANCE.get_product_file_page_size())
    table.attrs.update({"class": "table table-striped table-bordered"})
    return render(request, "delete_products.html", {"table": table})


def delete_product_file(request, fid):
    if models.ProductFile.objects.filter(pk=fid).exists():
        models.ProductFile.objects.filter(pk=fid).delete()
        product_set_to_delete = models.Product.objects.filter(file_id=fid)
        count = product_set_to_delete.count()
        product_set_to_delete.delete()
        messages.success(request, str(count) + "条记录被删除")
    else:
        messages.error(request, "文件未找到")
    return redirect(request.META['HTTP_REFERER'])


def search_product(request):
    if request.method == "GET":
        form = forms.QueryTextForm()
        return render(request, 'search_product.html', {"form": form})

    # Post
    form = forms.QueryTextForm(data=request.POST)
    if form.is_valid():
        for name, data in form.cleaned_data.items():
            filtered = filter(lambda x: x != '', data.split('\n'))
            key_words = set(map(lambda x: x.strip(), filtered))

            # build or conditions
            condition = Q()
            for key_word in key_words:
                condition |= Q(model__contains=key_word)
                condition |= Q(brand__contains=key_word)
            result = models.Product.objects.filter(condition)
            # result = models.Product.objects.filter(model__contains=key_words, brand__contains=key_words)
            table = tables.ProductTable(result)
            # table.paginate(page=request.GET.get("page", 1), per_page=5)
            table.attrs.update({"class": "table table-striped table-bordered"})
            return render(request, "product_search_result.html", {"table": table})


def update_product_hit_point(request):
    if request.method == "POST" and \
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # is ajax request
        product_id = request.POST.get('pid')
        hit_point_value = request.POST.get('val')
        if hit_point_value is None or product_id is None:
            data = {'result': 'failure'}
            return HttpResponse(json.dump(data))

        try:
            pid = int(product_id)
            hp = int(hit_point_value)
            if models.Product.objects.filter(pk=pid).exists():
                models.Product.objects.filter(pk=pid).update(hit_point=hp)
                data = {'result': 'success'}
            else:
                # log data not found
                data = {'result': 'failure'}
        except ValueError:
            data = {'result': 'failure'}
        return HttpResponse(json.dumps(data))

    return HttpResponse("not supported method type")
