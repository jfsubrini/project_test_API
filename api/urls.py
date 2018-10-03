"""Api app URL Configuration."""


# Django imports
from django.urls import path


# Import from my app
from . import views



urlpatterns = [
    # path('food/<int:customer_id>', views.food, name='food-get'),
    path('food/create', views.customer_create, name='customers-create'),
    path('food/search', views.customer_search, name='customers-search'),
]