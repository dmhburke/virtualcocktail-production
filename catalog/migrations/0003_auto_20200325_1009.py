# Generated by Django 3.0.4 on 2020-03-25 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_businessrecord_postcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessrecord',
            old_name='venmo_details',
            new_name='bank_details',
        ),
    ]
