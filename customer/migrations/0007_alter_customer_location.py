# Generated by Django 4.2.7 on 2023-12-09 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_customer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='location',
            field=models.CharField(help_text='please enter a correct to help with address', max_length=20),
        ),
    ]
