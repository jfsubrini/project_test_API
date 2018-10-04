#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that evaluate the performance of my API. 
"""


# Standard libraries imports
import requests, time

# Django imports
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

# Imports from my app
from api.constants import MY_API_URL



class Command(BaseCommand):
    """
    Django management class to enable the './manage.py test_perf_api.py' command.
    """

    help = "Lance un test pour évaluer la performance de mon API."


    def handle(self, *args, **options):
        """"Handles the process evaluating the performance of my API by testing
        it with 5000 requests.
        """

        # Introduction message informing on the process.
        self.stdout.write(self.style.SUCCESS(
            "\nLancement du test de performance de mon API avec 5 000 requêtes.\n"))

        # First update the categories into the database.
        # self.check_categories()
        # self.stdout.write(self.style.SUCCESS(
        #     "Mise à jour des catégories d'aliments en fonction de la liste établie.\n"))

        # Call to the API to get a json file for each category products.
        

        # time_before = time.time()
        # returned_value = func(*args, **kwargs)
        # time_after = time.time()
        # running_time = (time_after - time_before)*1000


        # Collecting the needed data for each food product.
        j = 0
        for product_id in range(1000, 5999):
            # If the product item has these data then collects them all.
            try:
                my_api = self.my_api_data(product_id)
                j += 1
            except IntegrityError:
                self.stdout.write(self.style.WARNING(
                    "Il n'y a pas d'aliment avec un id n° {0} dans la base de données".format(product_id)))

        # Ending message when the whole update is a success.
        self.stdout.write(self.style.SUCCESS(
            "\nLe test est terminé.\nAvec {0} requêtes ayant abouties, \
            le test a mis {1} millisecondes pour s'exécuter".format("xxxx", running_time)))


    def my_api_data(self, product_id):
        """Request to my API to collect data for the food products in the pur_beurre database."""
        try:
            payload = {'id': product_id}
            response = requests.get(MY_API_URL, params=payload)
            my_api = response.json()
            return my_api
        except:
            raise CommandError("""
                Problème de connexion avec mon API.
                """)
