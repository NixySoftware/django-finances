from typing import List

from django.db import transaction
from mollie.api.client import Client

from django_finances.payments.models import Payment
from django_finances.payments.providers.provider import Provider
from django_finances.settings import Settings
from django_finances.templatetags.currency import currency_amount

from .models import MolliePayment


class ProviderMollie(Provider):

    STATUS_LOOKUP: dict[str, Payment.Status] = {
        'open': Payment.Status.OPEN,
        'canceled': Payment.Status.CANCELED,
        'pending': Payment.Status.PENDING,
        'authorized': Payment.Status.AUTHORIZED,
        'expired': Payment.Status.EXPIRED,
        'failed': Payment.Status.FAILED,
        'paid': Payment.Status.COMPLETED
    }

    _client: Client
    _webhook_url: str
    _redirect_url: str

    def __init__(self, api_key: str, webhook_url: str, redirect_url: str = None):
        self._client = Client()
        self._client.set_api_key(api_key)

        self._webhook_url = webhook_url
        self._redirect_url = redirect_url

    def get_client(self):
        return self._client

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        def create_from_transactions(self, transactions: List[Transaction]):
            pass
    else:
        @transaction.atomic
        def create(self, amount: int, description: str, currency: str = Settings.CURRENCY_DEFAULT, redirect_url: str = None):
            payment = super().create(amount, description, currency)

            api_payment = self._client.payments.create({
                'amount': {
                    'currency': currency,
                    'value': currency_amount(amount, currency)
                },
                'description': description,
                'redirectUrl': redirect_url if redirect_url else self._redirect_url,
                'webhookUrl': self._webhook_url
            })

            payment.status = ProviderMollie.STATUS_LOOKUP[api_payment['status']]
            payment.save()

            mollie_payment = MolliePayment(identifier=api_payment['id'], checkout_url=api_payment['_links']['checkout']['href'], payment=payment)
            mollie_payment.save()

            return mollie_payment

    def webhook(self, mollie_id: str):
        if mollie_id.startswith('tr_'):
            # Fetch Mollie payment data
            payment_data = self._client.payments.get(mollie_id)

            # Update Mollie payment
            mollie_payment = MolliePayment.objects.get(identifier=payment_data['id'])
            mollie_payment.payment.status = ProviderMollie.STATUS_LOOKUP[payment_data.get('status')]
            mollie_payment.payment.save()
        elif mollie_id.startswith('ord_'):
            # Ignore webhooks for orders
            pass
        elif mollie_id.startswith('sub_'):
            # Ignore webhooks for subscriptions
            pass
        else:
            raise Exception(f'Invalid Mollie ID "{mollie_id}".')
