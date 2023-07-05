from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

import stockapp.models as models
import stockapp.tables as tables


# Create your views here.
def index(req):
    return HttpResponse("Hello!")


def products(request):
    product_list = models.Product.objects.all()
    table = tables.ProductTable(product_list)
    table.attrs.update({"class": "table table-striped table-bordered"})
    return render(request, "products.html", {"table": table})


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['brand', 'model', 'quantity', 'period', 'source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


def add_product(request):
    if request.method == "GET":
        form = ProductModelForm()
        return render(request, 'add_product.html', {"form": form})

    # Post
    form = ProductModelForm(data=request.POST)
    if not form.is_valid():
        print(form.errors)
    else:
        form.save()
        return redirect(products)


def add_products(request):
    if request.method == "GET":
        form = ProductModelForm()
        return render(request, 'add_products.html', {"form": form})

    # Post
    form = ProductModelForm(data=request.POST)
    if not form.is_valid():
        print(form.errors)
    else:
        form.save()
        return redirect(products)
