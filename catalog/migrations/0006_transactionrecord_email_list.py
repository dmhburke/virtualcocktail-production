# Generated by Django 3.0.4 on 2020-04-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_transactionrecord_donor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionrecord',
            name='email_list',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
