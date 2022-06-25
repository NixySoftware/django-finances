from django.db import models
from django.utils.translation import gettext_lazy as _

from django_finances.settings import Settings


class Payment(models.Model):

    class Status(models.TextChoices):
        # TODO: potentially add more statuses (e.g. REFUNDED)
        OPEN = 'OPEN', _('Open'),
        PENDING = 'PENDING', _('Pending'),
        AUTHORIZED = 'AUTHORIZED', _('Authorized'),
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELED = 'CANCELED', _('Cancelled'),
        EXPIRED = 'EXPIRED', _('Expired'),
        FAILED = 'FAILED', _('Failed')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)

    if Settings.TRANSACTION_ENABLED:
        transaction = models.OneToOneField('transactions.Transaction', related_name='payment', on_delete=models.PROTECT)
    else:
        amount = models.BigIntegerField() if Settings.USE_BIG_INTEGER else models.IntegerField()
        description = models.TextField()

    def get_amount(self):
        if Settings.TRANSACTION_ENABLED:
            return self.transaction.amount
        return self.amount

    def get_description(self):
        if Settings.TRANSACTION_ENABLED:
            return self.transaction.description
        return self.description
