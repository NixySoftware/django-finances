from typing import List

from django_finances.payments.providers.provider import Provider
from django_finances.settings import Settings

from .models import DirectDebitInstruction


class ProviderSEPA(Provider):

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        def create_from_transactions(self, transactions: List[Transaction]):
            pass
    else:
        def create(self, amount: int, description: str, currency: str = Settings.CURRENCY_DEFAULT):
            payment = super().create(amount, description)
            # TODO: addr required fields to constructor
            return DirectDebitInstruction(payment=payment)
