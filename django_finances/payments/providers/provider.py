from abc import abstractmethod, ABC
from typing import List

from django_finances.settings import Settings


class Provider(ABC):

    if Settings.TRANSACTION_ENABLED:
        from django_finances.transactions.models import Transaction

        @abstractmethod
        def generate_from_transactions(self, transactions: List[Transaction]):
            pass
