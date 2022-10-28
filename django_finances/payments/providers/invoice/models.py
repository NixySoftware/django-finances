from django.db import models
from django.utils.translation import gettext_lazy as _

from django_finances.models import BaseModel


def get_invoice_template_file_path(invoice_template_file, filename):
    return f'invoice_templates/{invoice_template_file.template.id}/{filename}'


def get_invoice_file_path(invoice_file, filename):
    return f'invoices/{invoice_file.invoice.id}/{filename}'


class InvoiceTemplate(BaseModel):

    class Meta:
        verbose_name = _('invoice template')
        verbose_name_plural = _('invoice templates')

    # TODO: locale, etc.


class InvoiceTemplateFile(BaseModel):

    class Meta:
        verbose_name = _('invoice template file')
        verbose_name_plural = _('invoice template files')

    file = models.FileField(_('file'), upload_to=get_invoice_file_path)

    template = models.ForeignKey(InvoiceTemplate, verbose_name=_('template'), related_name='files', on_delete=models.CASCADE)


class Invoice(BaseModel):

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    # TODO

    payment = models.OneToOneField('payments.Payment', verbose_name=_('payment'), related_name='invoice', on_delete=models.PROTECT)
    template = models.ForeignKey(InvoiceTemplate, verbose_name=_('template'), related_name='invoices', blank=True, null=True, on_delete=models.CASCADE)


class InvoiceFile(BaseModel):

    class Meta:
        verbose_name = _('invoice file')
        verbose_name_plural = _('invoice files')

    file = models.FileField(_('file'), upload_to=get_invoice_file_path)

    invoice = models.ForeignKey(Invoice, verbose_name=_('invoice'), related_name='files', on_delete=models.CASCADE)
