from dateutil.rrule import rrulestr
from django.db import models, transaction as db_transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models import BaseModel, FinancialEntity
from ..settings import Settings


class BaseTransaction(BaseModel):

    class Meta:
        abstract = True

    timestamp = models.DateField(_('timestamp'), default=timezone.now)
    amount = models.BigIntegerField(_('amount')) if Settings.USE_BIG_INTEGER else models.IntegerField(_('amount'))
    description = models.TextField(_('description'))

    # TODO: consider adding currency support (e.g. local_amount and local_currency)

    entity = models.ForeignKey(Settings.FINANCIAL_ENTITY_MODEL, verbose_name=_('entity'), related_name='transactions', on_delete=models.PROTECT)

    def __str__(self):
        return self.description


class RecurringTransaction(BaseTransaction):

    class Meta:
        verbose_name = _('recurring transaction')
        verbose_name_plural = _('recurring transactions')

    # TODO: add rrule validation
    recurrence = models.TextField(_('recurrence'))
    last_occurred_at = models.DateTimeField(blank=True)

    def generate_transactions(self):
        with db_transaction.atomic():
            # Parse recurrence rule and determine occurrences
            recurrence_rule = rrulestr(self.recurrence)
            occurrences = recurrence_rule.between(self.last_occurred_at, timezone.now())

            for occurrence in occurrences:
                # TODO: replace placeholders in description (date, etc.)

                # Create transaction
                transaction = Transaction(timestamp=occurrence, amount=self.amount, description=self.description, entity=self.entity)
                transaction.save()

                # Update last occurrence
                self.last_occurred_at = occurrence

            # Save last occurrence
            self.save()


class Transaction(BaseTransaction):

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

    recurring_transaction = models.ForeignKey(RecurringTransaction, verbose_name=_('recurring transaction'), related_name='transactions',
                                              blank=True, null=True, on_delete=models.SET_NULL)

    if Settings.TRANSACTION_SETTLEMENT_ENABLED:
        settled_by = models.ForeignKey('self', verbose_name=_('settled by'), related_name='settled', blank=True, null=True, on_delete=models.SET_NULL)

    @staticmethod
    def generate_settlements():
        with db_transaction.atomic():
            # Find entities and their balances
            # TODO: support Settings.FINANCIAL_ENTITY_MODEL
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
