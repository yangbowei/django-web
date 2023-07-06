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
from django.urls import path
from stockapp import views

urlpatterns = [
    path('', views.get_product),
    path('product/', views.get_product),
    path('product/add/', views.add_product),
    path('product/<int:uid>/edit/', views.edit_product),
    path('product/<int:uid>/delete/', views.delete_product),
    path('product/batch-add/', views.add_products),
    path('product/search/', views.search_product),
    path('admin/', admin.site.urls)
]
