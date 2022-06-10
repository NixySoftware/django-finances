from django.conf import settings
from django.db import models
from django.db.models import Sum

from .settings import Settings


class FinancialEntityManager(models.Manager):

    def with_balance(self):
        return self.annotate(balance=Sum('transactions__amount'))


class FinancialEntity(models.Model):
    class Meta:
        verbose_name_plural = 'financial entities'

    if Settings.TRANSACTION_ENABLED:
        objects = FinancialEntityManager()

    name = models.CharField(max_length=Settings.FINANCIAL_ENTITY_NAME_MAX_LENGTH)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class FinancialEntityMixin:
    entity = models.OneToOneField(FinancialEntity, blank=True, null=True, on_delete=models.SET_NULL)
