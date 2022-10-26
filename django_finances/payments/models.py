from django.db import models
from django.utils.translation import gettext_lazy as _

from ..fields import UUID4Field
from ..settings import Settings


class Payment(models.Model):

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    class Status(models.TextChoices):
        # TODO: potentially add more statuses (e.g. REFUNDED)
        OPEN = 'OPEN', _('Open'),
        PENDING = 'PENDING', _('Pending'),
        AUTHORIZED = 'AUTHORIZED', _('Authorized'),
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELED = 'CANCELED', _('Cancelled'),
        EXPIRED = 'EXPIRED', _('Expired'),
        FAILED = 'FAILED', _('Failed')

    if Settings.USE_UUID:
        id = UUID4Field(_('ID'), primary_key=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    status = models.CharField(_('status'), max_length=15, choices=Status.choices, default=Status.OPEN)

    if Settings.TRANSACTION_ENABLED:
        transaction = models.OneToOneField('transactions.Transaction', verbose_name=_('transaction'), related_name='payment', on_delete=models.PROTECT)
    else:
        amount = models.BigIntegerField(_('amount')) if Settings.USE_BIG_INTEGER else models.IntegerField(_('amount'))
        description = models.TextField(_('description'))

    def get_amount(self):
        if Settings.TRANSACTION_ENABLED:
            return self.transaction.amount
        return self.amount

    def get_description(self):
        if Settings.TRANSACTION_ENABLED:
            return self.transaction.description
        return self.description
