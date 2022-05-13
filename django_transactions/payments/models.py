from django.db import models

from django_transactions.transactions.models import Transaction


class Payment(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    debit_transactions = models.ForeignKey(Transaction, related_name='debit_payment', on_delete=models.PROTECT)
    credit_transaction = models.OneToOneField(Transaction, related_name='credit_payment', on_delete=models.PROTECT)
