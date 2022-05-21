from django.contrib import admin
from django.contrib.admin import register

from .models import FinancialEntity, Transaction


@register(FinancialEntity)
class FinancialEntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance']
    ordering = ['name']

    @staticmethod
    def balance(entity):
        # The field is not accepted in list_display without this method, even though it was added by the queryset.
        return entity.balance

    def get_queryset(self, request):
        qs = FinancialEntity.objects.with_balance()

        # NOTE: copied from super().get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'entity', 'description', 'amount']
    list_filter = ['created_at', 'updated_at']
    ordering = ['created_at', 'amount']
