import os

from django.conf import settings
from django_finances.payments.providers.mollie.provider import ProviderMollie

providers = [
    ProviderMollie(
        api_key=os.getenv('PAYMENT_PROVIDER_MOLLIE_API_KEY', ''),
        webhook_url=f'{settings.PUBLIC_URL}/payments/providers/mollie/webhook'
    )
]
