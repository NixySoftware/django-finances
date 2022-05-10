from django.db import models
from django.utils.translation import gettext_lazy as _

from django_transactions.payments.models import Payment

# TODO: mandates


class DirectDebit(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collected_at = models.DateField()
    identifier = models.CharField(max_length=35)


class SequenceType(models.TextChoices):
    FIRST = 'FRST', _('First'),
    RECURRENT = 'RCUR', _('Recurrent'),
    FINAL = 'FNAL', _('Final'),
    ONE_OFF = 'OOFF', _('One-off')


class DirectDebitBatch(models.Model):
    class Meta:
        unique_together = ('direct_debit', 'sequence_type')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=35)
    sequence_type = models.CharField(max_length=4, choices=SequenceType)

    direct_debit = models.ForeignKey(DirectDebit, related_name='batches', on_delete=models.CASCADE)


class DirectDebitInstruction(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=35)
    # TODO: description, amount, etc

    batch = models.ForeignKey(DirectDebit, related_name='instructions', on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, related_name='direct_debit_instruction', on_delete=models.PROTECT)
