"""
Only testing the POST HTTP method because I don't want to touch at
the pur_beurre databasein the real world but want to see if the code is working !
"""


import json

from django.test import TestCase
from food.models import Food, Category, NutritionGrade



class FoodTestCase(TestCase):


    def test_product_create(self):
        category = Category.objects.create(name="Pâte à tartiner")
        nutella = {
            'id': '312',
            'name': 'Nutella',
            'brand': 'Ferrero',
            'category': Category.objects.get(name=category),
            'nutrition_grade': NutritionGrade.e,
            'nutrition_score': 26,
            'url': 'https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero',
            'image_food': 'https://blablanut',
            'image_nutrition': 'https://blablablanut',
        }
        nutella = Food.objects.create(**nutella)
        uri = '/api/product/create'
        response = self.client.post(uri, data=nutella, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_product_get(self):
        category = Category.objects.create(name="Pâte à tartiner")
        nutella = {
            'id': '312',
            'name': 'Nutella',
            'brand': 'Ferrero',
            'category': Category.objects.get(name=category),
            'nutrition_grade': NutritionGrade.e,
            'nutrition_score': 26,
            'url': 'https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero',
            'image_food': 'https://blablanut',
            'image_nutrition': 'https://blablablanut',
        }
        nutella = Food.objects.create(**nutella)
        response = self.client.get('/api/product/search?name=Nutella')
        self.assertEqual(response.status_code, 200)
        foods = json.loads(response.content)
        self.assertEqual(len(foods), 1)
        food = foods[0]
        expected = {
            'id': 312,
            'name': 'Nutella',
            'brand': 'Ferrero',
            'category': 2,
            'nutrition_grade': 'E',
            'nutrition_score': 26,
            'url': 'https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero',
            'image_food': 'https://blablanut',
            'image_nutrition': 'https://blablablanut',
        }
        self.assertDictEqual(food, expected)
