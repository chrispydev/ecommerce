# Generated by Django 4.2.7 on 2023-12-08 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_order_payment_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Total',
            new_name='total',
        ),
    ]
