# Generated by Django 4.2.7 on 2023-12-09 11:58

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_email_phonenumber_admincontact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(default='please enter an address to recieve notifications', max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='please enter a number to recieve notifications', max_length=128, null=True, region=None),
        ),
    ]