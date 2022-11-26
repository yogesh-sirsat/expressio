from .base import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if os.getenv('USE_DEV_DB') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DEV_DB_ENGINE'),
            'NAME': os.getenv('DEV_DB_NAME'),
            'USER': os.getenv('DEV_DB_USER'),
            'PASSWORD': os.getenv('DEV_DB_PASSWORD'),
            'HOST': os.getenv('DEV_DB_HOST'),
            'PORT': os.getenv('DEV_DB_PORT'),
        }
    }