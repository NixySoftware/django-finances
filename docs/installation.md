# Installation

1. Install the Python package:
```bash
pip install django-finances
# Or
pipenv install django-finances
# Or
poetry add django-finances
```
2. Add the Django applications to the list of installed applications:
```python
INSTALLED_APPS = [
    # ...
    
    # Required
    'django_finances',
    
    # One or both modules
    'django_finances.transactions',
    'django_finances.payments',
    
    # Zero or more payment providers
    'django_finances.payments.providers.invoice',
    'django_finances.payments.providers.mollie',
    'django_finances.payments.providers.sepa',
]
```
3. Configure the settings, see [configuration](configuration.md):
```python
# Django Finances

DJANGO_FINANCES = {
    # ...
}
```
**Note:** Some settings can only be configured before the first migration.

4. Migrate the database:
```bash
python manage.py migrate
```
