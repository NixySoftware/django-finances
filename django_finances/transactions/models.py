from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _

from ..fields import UUID4Field
from ..models import FinancialEntity
from ..settings import Settings


class Transaction(models.Model):

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

    if Settings.USE_UUID:
        id = UUID4Field(_('ID'), primary_key=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    amount = models.BigIntegerField(_('amount')) if Settings.USE_BIG_INTEGER else models.IntegerField(_('amount'))
    description = models.TextField(_('description'))

    # TODO: consider adding currency support (e.g. local_amount and local_currency)

    entity = models.ForeignKey(Settings.FINANCIAL_ENTITY_MODEL, verbose_name=_('entity'), related_name='transactions', on_delete=models.PROTECT)

    if Settings.TRANSACTION_SETTLEMENT_ENABLED:
        settled_by = models.ForeignKey('self', verbose_name=_('settled by'), related_name='settled', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description

    @staticmethod
    def generate_settlements():
        with db_transaction.atomic():
            # Find entities and their balances
            entities = FinancialEntity.objects.with_balance().all()

            for entity in entities:
                # Find unsettled transactions
                transactions = entity.transactions.filter(settled_by__isnull=True, settled__isnull=True)

                # Sanity check for current state
                if entity.balance != sum([transaction.amount for transaction in transactions]):
                    raise Exception('Balance and sum of unsettled transactions are not equal.')

                # Check if there is a balance to settle
                if entity.balance == 0:
                    continue

                # Create settlement transaction
                settlement_transaction = Transaction(description=Settings.TRANSACTION_SETTLEMENT_DESCRIPTION, amount=-entity.balance, entity=entity)
                settlement_transaction.save()
                settlement_transaction.settled.set(transactions)
