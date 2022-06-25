from django.db import models


class MolliePayment(models.Model):

    identifier = models.CharField(max_length=32)
    checkout_url = models.CharField(max_length=128)

    payment = models.OneToOneField('payments.Payment', related_name='mollie_payment', on_delete=models.PROTECT)
