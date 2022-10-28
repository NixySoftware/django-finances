from typing import List

from django.db import transaction

from django_finances.payments.providers.provider import Provider
from django_finances.settings import Settings

from .models import DirectDebitInstruction


class ProviderSEPA(Provider):

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        def create_from_transactions(self, transactions: List[Transaction]):
            pass
    else:
        @transaction.atomic
        def create(self, amount: int, description: str, currency: str = Settings.CURRENCY_DEFAULT, **kwargs):
            payment = super().create(amount, description, **kwargs)
            # TODO: add required fields to constructor
            instruction = DirectDebitInstruction(payment=payment)
            instruction.save()
