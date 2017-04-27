from .base import *

INSTALLED_APPS += (
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # The following settings are not used with sqlite3:
        'NAME': 'woodkirkskills$woodkirkdb',
        'USER': 'woodkirkskills',
        'PASSWORD': 'v0n-neumann',
        'HOST': 'woodkirkskills.mysql.pythonanywhere-services.com',
        # Empty for localhost through domain sockets or   '127.0.0.1' for localhost through TCP.
        'PORT': '',
    }
}