from django.contrib import admin
from django.contrib.admin import register

from .models import RecurringTransaction, Transaction


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'entity', 'description', 'amount', 'recurring_transaction']
    list_filter = ['timestamp', 'created_at', 'updated_at']
    ordering = ['timestamp', 'amount']


@register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ['entity', 'description', 'amount', 'last_occurred_at']
    list_filter = ['last_occurred_at', 'created_at', 'updated_at']
    ordering = ['entity__name', 'description']
