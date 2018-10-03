# encoding: UTF-8


"""Api app URL Configuration."""


# Django imports
from django.urls import path


# Import from my app
from . import views



urlpatterns = [
    path('product/<int:product_id>', views.product, name='product_get'),
    path('product/create', views.product_create, name='product_create'),
    path('product/search', views.product_search, name='product_search'),
    path('category/search', views.category_search, name='category_search'),
]
