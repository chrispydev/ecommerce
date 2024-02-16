# Generated by Django 4.2.7 on 2023-12-09 10:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_address_alter_customer_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='please add a number', max_length=128, null=True, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='AdminContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emails', models.ManyToManyField(blank=True, to='customer.email')),
                ('phone_numbers', models.ManyToManyField(blank=True, to='customer.phonenumber')),
            ],
        ),
    ]