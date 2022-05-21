from django.contrib import admin
from django.contrib.admin import register

from .models import Payment


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'transaction']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
