# Generated by Django 3.2.6 on 2021-08-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0002_rename_sectors_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
