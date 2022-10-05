from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.getenv('PROD_DB_ENGINE'),
        'NAME': os.getenv('PROD_DB_NAME'),
        'USER': os.getenv('PROD_DB_USER'),
        'PASSWORD': os.getenv('PROD_DB_PASSWORD'),
        'HOST': os.getenv('PROD_DB_HOST'),
        'PORT': os.getenv('PROD_DB_PORT'),
    }
}
