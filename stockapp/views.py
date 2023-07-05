from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.shortcuts import redirect
import stockapp.models as models
import stockapp.tables as tables
import stockapp.forms as forms


# Create your views here.
def index(req):
    return HttpResponse("Hello!")


def get_product(request):
    product_list = models.Product.objects.all()
    table = tables.ProductTable(product_list)
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
            for name, file in form.files.items():
                print(name, file.name, file.size)
            # handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/products/")
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
