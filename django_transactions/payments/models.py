from django.apps import apps
from django.db import models


class Payment(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if apps.is_installed('django_transactions.transactions'):
        transaction = models.OneToOneField('transactions.Transaction', related_name='payment', on_delete=models.PROTECT)
