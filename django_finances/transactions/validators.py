from dateutil.rrule import rrulestr
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_rrule(value: str):
    try:
        rrulestr(value)
    except ValueError as e:
        raise ValidationError(_('Enter a valid recurrence rule (%(error)s).'), code='invalid', params={'value': value, 'error': str(e)})
