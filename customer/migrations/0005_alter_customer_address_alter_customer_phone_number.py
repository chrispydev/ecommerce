# Generated by Django 4.2.7 on 2023-12-09 12:01

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_customer_address_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(help_text='please enter an address to recieve notifications', max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='please enter an address to recieve notifications', max_length=128, null=True, region=None),
        ),
    ]