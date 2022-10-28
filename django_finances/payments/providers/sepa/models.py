from django.db import models
from django.utils.translation import gettext_lazy as _

from django_finances.settings import Settings


class SequenceType(models.TextChoices):
    FIRST = 'FRST', _('First'),
    RECURRENT = 'RCUR', _('Recurrent'),
    FINAL = 'FNAL', _('Final'),
    ONE_OFF = 'OOFF', _('One-off')


class Mandate(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signed_at = models.DateTimeField()
    identifier = models.CharField(max_length=35)
    iban = models.CharField(max_length=34)
    bic = models.CharField(max_length=11)
    reason = models.TextField()
    next_sequence_type = models.CharField(max_length=4, choices=SequenceType.choices, default=SequenceType.FIRST)

    # TODO: status, error message

    entity = models.ForeignKey(Settings.FINANCIAL_ENTITY_MODEL, related_name='mandates', on_delete=models.CASCADE)


class DirectDebit(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collected_at = models.DateField()
    identifier = models.CharField(max_length=35)


class DirectDebitBatch(models.Model):
    class Meta:
        unique_together = ('direct_debit', 'sequence_type')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=35)
    sequence_type = models.CharField(max_length=4, choices=SequenceType.choices)

    direct_debit = models.ForeignKey(DirectDebit, related_name='batches', on_delete=models.CASCADE)


class DirectDebitInstruction(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=35)
    iban = models.CharField(max_length=34)
    bic = models.CharField(max_length=11)
    description = models.CharField(max_length=140, blank=True)
    reference = models.CharField(max_length=35, blank=True)

    batch = models.ForeignKey(DirectDebit, related_name='instructions', on_delete=models.CASCADE)
    mandate = models.ForeignKey(Mandate, related_name='instructions', blank=True, null=True, on_delete=models.SET_NULL)

    payment = models.OneToOneField('payments.Payment', related_name='direct_debit_instruction', on_delete=models.PROTECT)
