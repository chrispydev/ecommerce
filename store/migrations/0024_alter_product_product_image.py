# Generated by Django 4.2.7 on 2024-01-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.URLField(default='http://localhost:8000/https%3A/images-na.ssl-images-amazon.com/images/I/616Vuoutx2L._AC_SX679_.jpg'),
        ),
    ]