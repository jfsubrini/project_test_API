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
        it with 10 000 requests.
        """

        # Introduction message informing on the process.
        self.stdout.write(self.style.SUCCESS(
            "\nLancement du test de performance de mon API avec 10 000 requêtes.\n"))

        # Call to the API to get a json file for each product with a range of ids.
        # Starting time for the testing process.
        time_before = time.time()
        # Collecting the needed data for each food product.
        d = 1000
        t = 10000
        j = 0
        for product_id in range(d, d+t):
            # If the product item has these data then collects them all.
            my_api = self.my_api_data(product_id)
            if my_api != []:
                j += 1
            else:
                self.stdout.write(self.style.WARNING(
                "Il n'y a pas d'aliment avec l'id n° {0} dans la base de données".format(product_id)))

        # Ending time and calculation of duration time for the whole testing process.
        time_after = time.time()
        running_time = (time_after - time_before)
        running_time = round(running_time, 2)
        # Ending message when the test is over, with the performance result.
        self.stdout.write(self.style.SUCCESS(
            "\nLe test est terminé.\nAvec {0} requêtes ayant abouties sur un total de {1}, le test a mis {2} secondes pour s'exécuter.".format(j, t, running_time)))


    def my_api_data(self, product_id):
        """Request to my API to collect data for the food products in the pur_beurre database,
        with ids from 1000 to 10999."""
        try:
            payload = {'id': product_id}
            response = requests.get(MY_API_URL, params=payload)
            my_api = response.json()
            print(my_api)
            return my_api
        except:
            raise CommandError("""
                Problème de connexion avec mon API.
                """)
