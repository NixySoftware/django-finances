from django.db import models
from django.utils.translation import gettext_lazy as _

from django_finances.fields import UUID4Field
from django_finances.settings import Settings


class MolliePayment(models.Model):

    class Meta:
        verbose_name = _('mollie payment')
        verbose_name_plural = _('mollie payments')

    if Settings.USE_UUID:
        id = UUID4Field(_('ID'), primary_key=True)

    identifier = models.CharField(_('identifier'), max_length=32)
    checkout_url = models.CharField(_('checkout url'), max_length=128)

    payment = models.OneToOneField('payments.Payment', verbose_name=_('payment'), related_name='mollie_payment', on_delete=models.PROTECT)
