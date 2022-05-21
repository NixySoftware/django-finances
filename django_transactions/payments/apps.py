from django.apps import AppConfig, apps


class PaymentsConfig(AppConfig):
    name = 'django_transactions.payments'

    def ready(self):
        # from .models import Payment
        # Payment.generate_payments()
        pass
