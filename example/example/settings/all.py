from .base import *

INSTALLED_APPS += [
    'django_transactions',
    'django_transactions.transactions',
    'django_transactions.payments',
    # 'django_transactions.payments.providers.invoice',
    # 'django_transactions.payments.providers.sepa',
]
