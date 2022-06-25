from django.contrib import admin
from django.contrib.admin import register

from .models import MolliePayment


@register(MolliePayment)
class MolliePaymentAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'checkout_url', 'payment']
    list_filter = []
    ordering = ['identifier']
