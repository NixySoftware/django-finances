from typing import List

from django_finances.payments.providers.provider import Provider
from django_finances.settings import Settings

from .models import Invoice, InvoiceTemplate


class ProviderInvoice(Provider):

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        def create_from_transactions(self, transactions: List[Transaction]):
            pass
    else:
        def create(self, amount: int, description: str, currency: str = Settings.CURRENCY_DEFAULT, template: InvoiceTemplate = None):
            payment = super().create(amount, description)
            return Invoice(payment=payment, template=template)
