# Generated by Django 4.2.7 on 2023-12-19 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_shippingrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingrate',
            old_name='postal_code',
            new_name='location',
        ),
    ]