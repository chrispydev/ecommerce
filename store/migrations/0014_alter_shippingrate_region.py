# Generated by Django 4.2.7 on 2023-12-21 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_shippingrate_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingrate',
            name='region',
            field=models.CharField(choices=[('Ashanti Region', 'Ashanti Region'), ('Brong-Ahafo Region', 'Brong-Ahafo Region'), ('Central Region', 'Central Region'), ('Eastern Region', 'Eastern Region'), ('Greater Accra Region', 'Greater Accra Region'), ('Northern Region', 'Northern Region'), ('Upper East Region', 'Upper East Region'), ('Upper West Region', 'Upper West Region'), ('Volta Region', 'Volta Region'), ('Western Region', 'Western Region'), ('Western North Region', 'Western North Region'), ('Oti Region', 'Oti Region'), ('Savannah Region', 'Savannah Region'), ('North East Region', 'North East Region'), ('Bono Region', 'Bono Region'), ('Ahafo Region', 'Ahafo Region')], max_length=100),
        ),
    ]
