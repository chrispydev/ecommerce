# Generated by Django 4.2.7 on 2023-12-19 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_rename_postal_code_shippingrate_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingrate',
            old_name='location',
            new_name='nearest_location',
        ),
    ]
