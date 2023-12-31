"""repoweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from stockapp import views
from . import settings
from stockapp import formviews

urlpatterns = [
    path('', views.get_product),
    path('product/', views.get_product),
    path('product/add/', views.add_product),
    path('product/<int:uid>/edit/', views.edit_product),
    path('product/<int:uid>/delete/', views.delete_product),
    path('product/delete_all/', views.delete_all_products),
    path('product-file/', views.product_files),
    path('product-file/<int:fid>/delete/', views.delete_product_file),
    path('product/batch-add/', formviews.FileFieldFormView.as_view()),
    path('product/search/', views.search_product),
    path('product/update-hp/', views.update_product_hit_point),
    path('admin/', admin.site.urls),
    # define routing for static files
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media')
]
