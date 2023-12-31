# Generated by Django 4.2.7 on 2023-12-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
