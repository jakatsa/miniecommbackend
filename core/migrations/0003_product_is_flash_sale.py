# Generated by Django 5.1.1 on 2024-10-28 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_product_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_flash_sale',
            field=models.BooleanField(default=True),
        ),
    ]