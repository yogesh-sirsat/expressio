from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.expressio.live']

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
