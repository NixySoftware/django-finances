from django.db import models


def get_invoice_template_file_path(invoice_template_file, filename):
    return f'invoice_templates/{invoice_template_file.template.id}/{filename}'


def get_invoice_file_path(invoice_file, filename):
    return f'invoices/{invoice_file.invoice.id}/{filename}'


class InvoiceTemplate(models.Model):
    # TODO
    pass


class InvoiceTemplateFile(models.Model):

    file = models.FileField(upload_to=get_invoice_file_path)

    template = models.ForeignKey(InvoiceTemplate, related_name='files', on_delete=models.CASCADE)


class Invoice(models.Model):

    # TODO

    payment = models.OneToOneField('payments.Payment', related_name='invoice', on_delete=models.PROTECT)
    template = models.ForeignKey(InvoiceTemplate, related_name='invoices', blank=True, null=True, on_delete=models.CASCADE)


class InvoiceFile(models.Model):

    file = models.FileField(upload_to=get_invoice_file_path)

    invoice = models.ForeignKey(Invoice, related_name='files', on_delete=models.CASCADE)
