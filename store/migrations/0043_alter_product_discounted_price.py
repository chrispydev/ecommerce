# Generated by Django 4.2.7 on 2024-02-20 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_product_discounted_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True),
        ),
    ]
