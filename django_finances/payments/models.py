from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models import BaseModel
from ..settings import Settings


class Payment(BaseModel):

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
