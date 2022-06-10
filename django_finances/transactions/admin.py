from django.contrib import admin
from django.contrib.admin import register

from .models import Transaction


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'entity', 'description', 'amount']
    list_filter = ['created_at', 'updated_at']
    ordering = ['created_at', 'amount']
