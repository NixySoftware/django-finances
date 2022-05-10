from django.conf import settings as django_settings


class PaymentsSettings:
    _settings = getattr(django_settings, 'DJANGO_TRANSACTIONS', {})
