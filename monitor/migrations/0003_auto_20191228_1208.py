# Generated by Django 3.0.1 on 2019-12-28 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20191228_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='actual_price',
            new_name='purchase_price',
        ),
    ]
