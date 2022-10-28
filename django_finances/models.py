from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .fields import UUID4Field
from .settings import Settings


class BaseModel(models.Model):

    class Meta:
        abstract = True

    if Settings.USE_UUID:
        id = UUID4Field(_('ID'), primary_key=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


class FinancialEntityManager(models.Manager):

    def with_balance(self):
        return self.annotate(balance=Sum('transactions__amount'))


class AbstractFinancialEntity(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(_('name'), max_length=Settings.FINANCIAL_ENTITY_NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class FinancialEntity(BaseModel, AbstractFinancialEntity):

    class Meta:
        verbose_name = _('financial entity')
        verbose_name_plural = _('financial entities')

    if Settings.TRANSACTION_ENABLED:
        objects = FinancialEntityManager()

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'), blank=True, null=True, on_delete=models.SET_NULL)


class FinancialEntityMixin:
    entity = models.OneToOneField(Settings.FINANCIAL_ENTITY_MODEL, verbose_name=_('entity'), blank=True, null=True, on_delete=models.SET_NULL)
