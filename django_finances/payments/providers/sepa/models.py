from django.db import models
from django.utils.translation import gettext_lazy as _

from django_finances.models import BaseModel
from django_finances.settings import Settings


class SequenceType(models.TextChoices):
    FIRST = 'FRST', _('First'),
    RECURRENT = 'RCUR', _('Recurrent'),
    FINAL = 'FNAL', _('Final'),
    ONE_OFF = 'OOFF', _('One-off')


class Mandate(BaseModel):

    class Meta:
        verbose_name = _('mandate')
        verbose_name_plural = _('mandates')

    signed_at = models.DateTimeField(_('signed at'))
    identifier = models.CharField(_('identifier'), max_length=35)
    iban = models.CharField(_('IBAN'), max_length=34)
    bic = models.CharField(_('BIC'), max_length=11)
    reason = models.TextField(_('reason'))
    next_sequence_type = models.CharField(_('next sequence type'), max_length=4, choices=SequenceType.choices, default=SequenceType.FIRST)
    # TODO: status, error message

    entity = models.ForeignKey(Settings.FINANCIAL_ENTITY_MODEL, verbose_name=_('entity'), related_name='mandates', on_delete=models.CASCADE)


class DirectDebit(BaseModel):

    class Meta:
        verbose_name = _('direct debit')
        verbose_name_plural = _('direct debits')

    collected_at = models.DateField(_('collected at'))
    identifier = models.CharField(max_length=35)


class DirectDebitBatch(BaseModel):

    class Meta:
        verbose_name = _('direct debit batch')
        verbose_name_plural = _('direct debit batches')
        unique_together = ('direct_debit', 'sequence_type')

    identifier = models.CharField(_('identifier'), max_length=35)
    sequence_type = models.CharField(_('sequence type'), max_length=4, choices=SequenceType.choices)

    direct_debit = models.ForeignKey(DirectDebit, verbose_name=_('direct debit'), related_name='batches', on_delete=models.CASCADE)


class DirectDebitInstruction(BaseModel):

    class Meta:
        verbose_name = _('direct debit instruction')
        verbose_name_plural = _('direct debit instructions')

    identifier = models.CharField(_('identifier'), max_length=35)
    iban = models.CharField(_('IBAN'), max_length=34)
    bic = models.CharField(_('BIC'), max_length=11)
    description = models.CharField(_('description'), max_length=140, blank=True)
    reference = models.CharField(_('reference'), max_length=35, blank=True)

    batch = models.ForeignKey(DirectDebit, verbose_name=_('batch'), related_name='instructions', on_delete=models.CASCADE)
    mandate = models.ForeignKey(Mandate, verbose_name=_('mandate'), related_name='instructions', blank=True, null=True, on_delete=models.SET_NULL)

    payment = models.OneToOneField('payments.Payment', verbose_name=_('payment'), related_name='direct_debit_instruction', on_delete=models.PROTECT)
