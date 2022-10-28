from django.contrib import admin
from django.contrib.admin import register

from .models import FinancialEntity
from .settings import Settings


if Settings.FINANCIAL_ENTITY_MODEL == 'django_finances.FinancialEntity':
    @register(FinancialEntity)
    class FinancialEntityAdmin(admin.ModelAdmin):
        list_display = ['name', 'balance'] if Settings.TRANSACTION_ENABLED else ['name']
        ordering = ['name']

        @staticmethod
        def balance(entity):
            # The field is not accepted in list_display without this method, even though it was added by the queryset.
            return entity.balance

        def get_queryset(self, request):
            if not Settings.TRANSACTION_ENABLED:
                return super().get_queryset(request)

            qs = FinancialEntity.objects.with_balance()

            # NOTE: copied from super().get_queryset()
            ordering = self.get_ordering(request)
            if ordering:
                qs = qs.order_by(*ordering)
            return qs
