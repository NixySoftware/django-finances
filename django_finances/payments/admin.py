from django.contrib import admin
from django.contrib.admin import register

from django_finances.settings import Settings

from .models import Payment


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'amount', 'transaction'] if Settings.TRANSACTION_ENABLED else ['created_at', 'updated_at', 'amount']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
