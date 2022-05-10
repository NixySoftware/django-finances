from django.conf import settings as django_settings


class TransactionsSettings:
    _settings = getattr(django_settings, 'DJANGO_TRANSACTIONS', {})

    USE_BIG_INTEGER = _settings.get('use_big_integer', False)

    _financial_entity_settings = _settings.get('financial_entities', {})
    FINANCIAL_ENTITY_NAME_MAX_LENGTH = _financial_entity_settings.get('name_max_length', 255)
