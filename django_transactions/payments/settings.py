from django.conf import settings as django_settings


class PaymentsSettings:
    _settings = getattr(django_settings, 'DJANGO_TRANSACTIONS', {})

    _provider_settings = _settings.get('payment_providers', {})
