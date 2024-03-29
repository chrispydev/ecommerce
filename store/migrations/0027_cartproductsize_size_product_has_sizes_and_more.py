# Generated by Django 4.2.7 on 2024-02-07 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_alter_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_product_size', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='has_sizes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_in_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item_size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cartproductsize'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='store.size'),
        ),
    ]
