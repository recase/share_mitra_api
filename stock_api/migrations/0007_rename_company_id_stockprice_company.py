# Generated by Django 3.2.6 on 2021-08-12 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0006_rename_company_id_livepirce_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockprice',
            old_name='company_id',
            new_name='company',
        ),
    ]
