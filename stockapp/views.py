from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from . import forms
from . import models
from . import processor
from . import tables


# Create your views here.
def index(req):
    return HttpResponse("Hello!")


def get_product(request):
    product_list = models.Product.objects.all()
    table = tables.ProductTable(product_list)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    table.attrs.update({"class": "table table-striped table-bordered"})
    return render(request, "products.html", {"table": table})


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


def add_products(request):
    if request.method == "POST":
        form = forms.UploadProductFileForm(request.POST, request.FILES)
        if form.is_valid():
            msg = []
            for file in request.FILES.getlist('file'):
                success, result_msg = processor.process_excel_file(file.name, file.size, file.file)
                if success:
                    msg.append(str.format('成功导入{}条数据，文件："{}"', result_msg, file.name))
                else:
                    msg.append(str.format('导入失败，原因：{}。文件："{}"', result_msg, file.name))
            return render(request, "action_result.html", {"messages": msg})
    else:
        form = forms.UploadProductFileForm()
        return render(request, "add_products.html", {"form": form})


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
    product_count = models.Product.objects.count()
    models.ProductFile.objects.all().delete()
    models.Product.objects.all().delete()
    msg = str.format('来自{}个文件的{}条数据已被删除!', product_file_count, product_count)
    return render(request, "action_result.html", {"messages": [msg]})


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
