from typing import List

from django_finances.payments.providers.provider import Provider
from django_finances.settings import Settings


class ProviderInvoice(Provider):

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        def generate_from_transactions(self, transactions: List[Transaction]):
            pass
