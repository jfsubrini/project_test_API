'''
Module for views.
'''

from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
# from django.contrib.admin.views.decorators import staff_member_required
from food.models import Food, Category
from api.common import json_to_model


@require_GET
# @staff_member_required
def product(request, product_id):
    """
    Method: GET
    Path: /api/product/<id>
    Get given product:
    - id: the product ID
    Return: the product as Json (model_to_json)
    """
    return Food.objects.get(id=product_id)

# A TESTER CETTE VUE
@require_POST
# @staff_member_required
def product_create(request):
    """
    Method: POST
    Path: /api/product/create
    Create a product:
    - data: customer fields as json in request body
    Return: nothing
    """
    json_to_model(request.body.decode('utf-8'), Food).save()
    return HttpResponse()

@require_GET
# @staff_member_required
def product_search(request):
    """
    Method: GET
    Path: /api/product/search
    Search for products. Search parameters are passed as URL parameters. Thus to get products
    with named Nutella, you would add parameters '?name=Nutella&brand=Ferrero'.
    Return: the products list (queryset_to_json)
    """
    filters = dict(request.GET.items())
    return Food.objects.filter(**filters)

@require_GET
# @staff_member_required
def category_search(request):
    """
    Method: GET
    Path: /api/category/search
    Search for categories. Search parameters are passed as URL parameters.
    Possible search by id : '?id=4'.
    Return: the categories list (queryset_to_json)
    """
    filters = dict(request.GET.items())
    return Category.objects.filter(**filters)
