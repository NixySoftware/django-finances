import functools
import os
from importlib import import_module
from typing import TypedDict

from django.apps import apps
from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _
from lxml import etree


class CurrencyDefinition(TypedDict):
    code: str
    name: str
    number: int
    minor_units: int


def load_currency_definitions(path: str):
    currency_definitions: dict[str, CurrencyDefinition] = {}

    tree = etree.parse(path)

    for country in tree.find('CcyTbl').findall('CcyNtry'):
        code_element = country.find('Ccy')
        if code_element is None or country.find('CcyMnrUnts').text == 'N.A.':
            continue

        code = code_element.text
        if code not in currency_definitions:
            currency_definitions[code] = {
                'code': code,
                'name': country.find('CcyNm').text,
                'number': int(country.find('CcyNbr').text),
                'minor_units': int(country.find('CcyMnrUnts').text)
            }

    return currency_definitions


class Settings:
    _settings = getattr(django_settings, 'DJANGO_FINANCES', {})

    USE_UUID = _settings.get('use_uuid', False)
    USE_BIG_INTEGER = _settings.get('use_big_integer', False)

    _currency_settings = _settings.get('currencies', {})
    CURRENCY_DEFAULT = _currency_settings.get('default', 'EUR')
    CURRENCY_LIST = _currency_settings.get('list', ['EUR'])
    CURRENCY_XML_PATH = _currency_settings.get('xml_path', os.path.join(os.path.dirname(__file__), 'data', 'iso_4217_1.xml'))
    CURRENCY_DEFINITIONS: dict[str, CurrencyDefinition] = _currency_settings.get('definitions', None)

    if not CURRENCY_DEFINITIONS:
        CURRENCY_DEFINITIONS = load_currency_definitions(CURRENCY_XML_PATH)

    _financial_entity_settings = _settings.get('financial_entities', {})
    FINANCIAL_ENTITY_MODEL = _financial_entity_settings.get('model', 'django_finances.FinancialEntity')
    FINANCIAL_ENTITY_NAME_MAX_LENGTH = _financial_entity_settings.get('name_max_length', 255)

    _transaction_settings = _settings.get('transactions', {})
    TRANSACTION_ENABLED = apps.is_installed('django_finances.transactions')
    TRANSACTION_SETTLEMENT_ENABLED = _transaction_settings.get('settlement_enabled', True)
    TRANSACTION_SETTLEMENT_DESCRIPTION = _transaction_settings.get('settlement_name', _('Settlement'))

    _payment_settings = _settings.get('payments', {})
    PAYMENT_ENABLED = apps.is_installed('django_finances.payments')
    PAYMENT_PROVIDERS = _payment_settings.get('providers', None)

    @staticmethod
    @functools.cache
    def get_payment_providers():
        if Settings.PAYMENT_PROVIDERS:
            provider_module = import_module(Settings.PAYMENT_PROVIDERS)
            return provider_module.providers
        else:
            return []

    @staticmethod
    def get_payment_provider(cls):
        providers = Settings.get_payment_providers()
        for provider in providers:
            if isinstance(provider, cls):
                return provider
        return None

    @staticmethod
    def get_financial_entity_model():
        app_label, _, model = Settings.FINANCIAL_ENTITY_MODEL.rpartition('.')
        return apps.get_model(app_label, model)
