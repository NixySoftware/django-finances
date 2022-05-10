from django.db import models

from django_transactions.payments.models import Payment


class Invoice(models.Model):

    payment = models.OneToOneField(Payment, related_name='invoice', on_delete=models.PROTECT)

    # TODO: templates, files
