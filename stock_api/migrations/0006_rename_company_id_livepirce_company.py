# Generated by Django 3.2.6 on 2021-08-08 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0005_alter_company_instrument_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livepirce',
            old_name='company_id',
            new_name='company',
        ),
    ]