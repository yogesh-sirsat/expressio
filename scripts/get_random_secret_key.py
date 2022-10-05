# generate_secret.py
from django.core.management import utils

def run():
    print(utils.get_random_secret_key())
