# Generated by Django 3.0.4 on 2020-03-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200325_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessrecord',
            name='instagram_handle',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
