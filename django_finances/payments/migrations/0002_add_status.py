# Generated by Django 4.0.4 on 2022-06-25 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('PENDING', 'Pending'), ('AUTHORIZED', 'Authorized'), ('COMPLETED', 'Completed'), ('CANCELED', 'Cancelled'), ('EXPIRED', 'Expired'), ('FAILED', 'Failed')], default='OPEN', max_length=15),
        ),
    ]
