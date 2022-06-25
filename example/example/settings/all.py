from .base import *

INSTALLED_APPS += [
    'django_finances',
    'django_finances.transactions',
    'django_finances.payments',
    'django_finances.payments.providers.mollie',
    # 'django_finances.payments.providers.invoice',
    # 'django_finances.payments.providers.sepa',
]
