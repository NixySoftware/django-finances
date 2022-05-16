from typing import Optional

from django import template

from ..settings import TransactionsSettings

register = template.Library()


@register.filter
def currency_amount(amount: int, currency: Optional[str]):
    if not isinstance(amount, int):
        raise ValueError('Amount is not an integer.')

    if not currency:
        currency = TransactionsSettings.CURRENCY_DEFAULT

    if currency not in TransactionsSettings.CURRENCY_DEFINITIONS:
        raise ValueError(f'Unknown currency "{currency}"')

    minor_units = TransactionsSettings.CURRENCY_DEFINITIONS[currency]['minor_units']
    currency_format = f'{{:.{minor_units}f}}'

    return currency_format.format(amount / (10 ** minor_units) if minor_units > 0 else amount)
