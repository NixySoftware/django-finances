from django.conf import settings
from django.db import models
from django.db.models import Sum

from .settings import TransactionsSettings


class FinancialEntity(models.Model):
    class Meta:
        verbose_name_plural = 'financial entities'

    name = models.CharField(max_length=TransactionsSettings.FINANCIAL_ENTITY_NAME_MAX_LENGTH)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    @property
    def balance(self):
        return self.transactions.aggregate(amount=Sum('amount'))['amount']


class FinancialEntityMixin:
    entity = models.OneToOneField(FinancialEntity, blank=True, null=True, on_delete=models.SET_NULL)


class Transaction(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.BigIntegerField() if TransactionsSettings.USE_BIG_INTEGER else models.IntegerField()
    description = models.TextField()

    # TODO: consider adding currency support (e.g. local_amount and local_currency)

    entity = models.ForeignKey(FinancialEntity, related_name='transactions', on_delete=models.PROTECT)

    def __str__(self):
        return self.description
