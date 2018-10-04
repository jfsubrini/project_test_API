"""
Module for views.
"""

import time

from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
# from django.contrib.admin.views.decorators import staff_member_required
from food.models import Food, Category, NutritionGrade
from api.common import json_to_model



# def performance(func):
#     """Decorator creation to evaluate the performance of the API code
#     """
#     def inner(*args, **kwargs):
#         time_before = time.time()
#         returned_value = func(*args, **kwargs)
#         time_after = time.time()
#         running_time = (time_after - time_before)*1000
#         print("La requête {0} a mis {1} millisecondes pour s'exécuter".format(func, running_time))
#         return returned_value
#     return inner


@require_GET
# @staff_member_required
# @performance
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
# @performance
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
# @performance
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
# @performance
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
