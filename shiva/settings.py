# Import base settings.
from shiva.base import *

# 30 days until ticket expiraion.
TICKET_EXPIRATION = 30

# The site domain.
SITE_ADDRESS = 'http://0.0.0.0:8000'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*7y@tp@b3d1kr900sre3jy)i@(+1113!n_js^&%frs$qtgnosi'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']

# Email settings.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Captcha attributes.
NOCAPTCHA = True

# For debugging on 0.0.0.0.
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
