from abc import abstractmethod, ABC
from typing import List

from django_finances.settings import Settings

from ..models import Payment


class Provider(ABC):

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        @abstractmethod
        def create_from_transactions(self, transactions: List[Transaction]):
            pass
    else:
        def create(self, amount: int, description: str, currency: str = Settings.CURRENCY_DEFAULT, save=False):
            payment = Payment(amount=amount, description=description)
            if save:
                payment.save()
            return payment
