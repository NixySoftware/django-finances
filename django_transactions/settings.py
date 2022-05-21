import os
from typing import TypedDict

from django.conf import settings as django_settings
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
    _settings = getattr(django_settings, 'DJANGO_TRANSACTIONS', {})

    USE_BIG_INTEGER = _settings.get('use_big_integer', False)

    _currency_settings = _settings.get('currencies', {})
    CURRENCY_DEFAULT = _currency_settings.get('default', 'EUR')
    CURRENCY_LIST = _currency_settings.get('list', ['EUR'])
    CURRENCY_XML_PATH = _currency_settings.get('xml_path', os.path.join(os.path.dirname(__file__), 'data', 'iso_4217_1.xml'))
    CURRENCY_DEFINITIONS: dict[str, CurrencyDefinition] = _currency_settings.get('definitions', None)

    if not CURRENCY_DEFINITIONS:
        CURRENCY_DEFINITIONS = load_currency_definitions(CURRENCY_XML_PATH)

    _financial_entity_settings = _settings.get('financial_entities', {})
    FINANCIAL_ENTITY_NAME_MAX_LENGTH = _financial_entity_settings.get('name_max_length', 255)

    _transaction_settings = _settings.get('transactions', {})
    TRANSACTION_SETTLEMENT_ENABLED = _transaction_settings.get('settlement_enabled', True)
    TRANSACTION_SETTLEMENT_DESCRIPTION = _transaction_settings.get('settlement_name', 'Settlement')

    _payment_settings = _settings.get('payments', {})
    _provider_settings = _payment_settings.get('providers', {})
