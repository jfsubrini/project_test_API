#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that uses the OpenFoodFacts API to collect all the data needed
for the pur_beurre database, the first time and for updates.
"""


# Standard libraries imports
import requests

# Django imports
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

# Imports from my app
from food.constants import OFF_API_URL, CATEGORIES_LIST
from food.models import Food, Category, NutritionGrade



class Command(BaseCommand):
    """
    Django management class to enable the './manage.py off_api.py' command.
    This Command class collects and updates all the data needed for all selected categories
    for the pur_beurre database from the OpenFoodFacts API.
    """

    help = "Met à jour la base de données pur_beurre avec les dernières données d'OpenFoodFacts \n\
    pour les catégories définies dans constants.py"


    def handle(self, *args, **options):
        """"Handles the process of updating the data into the pur_beurre database.
        Returns the information when the process is completed.
        """

        # Introduction message informing on the process.
        self.stdout.write(self.style.SUCCESS(
            "\nLancement de l'actualisation de la base de données pur_beurre grâce à l'API d'OpenFoodFacts.\n"))

        # First update the categories into the database.
        self.check_categories()
        self.stdout.write(self.style.SUCCESS(
            "Mise à jour des catégories d'aliments en fonction de la liste établie.\n"))

        # Second for each food category update the food data needed into the database,
        # collecting the data from the Open Food Facts REST API.
        for category in CATEGORIES_LIST:
            # Displaying message when new food data from each category is being processing.
            self.stdout.write(
                self.style.WARNING(
                    "Collecte des informations sur les aliments de la catégorie : '%s' ..." % category)
                )
            # Call to the API to get a json file for each category products.
            openfoodfacts = self.off_api_data(category)
            # Collecting the needed data for each food product.
            j = 0
            for item in range(0, openfoodfacts['count']-1):
                # If the product item has these data then collects them all.
                try:
                    shortcut = openfoodfacts['products'][item]
                    name = shortcut['product_name']
                    brand = shortcut['brands']
                    image_food = shortcut['image_front_url']
                    image_nutrition = shortcut['image_nutrition_url']
                    nutrition_grade = shortcut['nutrition_grade_fr']
                    nutrition_score = shortcut['nutriments']['nutrition-score-fr_100g']
                    url = shortcut['url']
                    j += 1
                    # Converting for EnumChoiceField.
                    if nutrition_grade == "a":
                        nutrition_grade = NutritionGrade.a
                    elif nutrition_grade == "b":
                        nutrition_grade = NutritionGrade.b
                    elif nutrition_grade == "c":
                        nutrition_grade = NutritionGrade.c
                    elif nutrition_grade == "d":
                        nutrition_grade = NutritionGrade.d
                    elif nutrition_grade == "e":
                        nutrition_grade = NutritionGrade.e
                    # Call to the function that inserts the food values into the database.
                    self.insert_data(name, brand, category, nutrition_grade, \
                        nutrition_score, url, image_food, image_nutrition, j)
                except:
                    pass

        # Ending message when the whole update is a success.
        self.stdout.write(self.style.SUCCESS(
            "\nLa base de données pur_beurre a bien été mise à jour.\nBon appétit !\n"))


    @transaction.atomic
    def check_categories(self):
        """Method that maintains equivalence between the categories present in the
        CATEGORIES_LIST and the ones present into the database Category table."""
        db_actual_cat = Category.objects.values_list('name', flat=True)
        for list_cat in CATEGORIES_LIST:
            if list_cat not in db_actual_cat:
                # Creation of a new category into the database.
                try:
                    Category.objects.create(name=list_cat)
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(
                        "La catégorie {} n'a pas pu être enregistrée dans la base de données.".format(list_cat)))

        for db_cat in db_actual_cat:
            if db_cat not in CATEGORIES_LIST:
                # Delete of the category presents into the database
                # because it's not anymore into the CATEGORIES_LIST.
                try:
                    Category.objects.filter(name=db_cat).delete()
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(
                        "La catégorie {} n'a pas pu être supprimée de la base de données.".format(db_cat)))


    def off_api_data(self, category):
        """Request to the OFF API to collect data for one category."""
        try:
            payload = {'search_terms': category, 'page_size': 1000, 'json': 1}
            response = requests.get(OFF_API_URL, params=payload)
            openfoodfacts = response.json()
            return openfoodfacts
        except:
            raise CommandError("""
                Problème de connexion avec l'API d'OpenFoodFacts.
                Vérifiez votre connexion Internet
                ainsi que la liste des catégories dans constants.py.
                """)


    def insert_data(self, name, brand, category, nutrition_grade, \
        nutrition_score, url, image_food, image_nutrition, j):
        """Inserting into the Food table all the data for each new food of one category."""
        try:
            with transaction.atomic():
                Food.objects.create(
                    name=name.lower().capitalize(),
                    brand=brand.lower().capitalize(),
                    category=Category.objects.get(name=category),
                    nutrition_grade=nutrition_grade,
                    nutrition_score=nutrition_score,
                    url=url,
                    image_food=image_food,
                    image_nutrition=image_nutrition
                    )
                # Prints for the Console Command Line
                self.stdout.write("Nom : {}".format(name))
                self.stdout.write("Marque : {}".format(brand))
                self.stdout.write("Image de l'aliment : {}".format(image_food))
                self.stdout.write("Image repères nutritionnels : {}".format(image_nutrition))
                self.stdout.write("Nutriscore : {}".format(nutrition_grade))
                self.stdout.write("Nutriscore numérique : {}".format(nutrition_score))
                self.stdout.write("URL fiche aliment : {}".format(url))
                self.stdout.write("Catégorie : {}".format(category))
                self.stdout.write("N° de l'aliment : {}\n\n".format(j))
        except IntegrityError:
            self.stdout.write(self.style.WARNING(
                "Problème : {} n'a pas pu être enregistré dans la base de données.".format(name)))
