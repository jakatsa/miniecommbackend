# Generated by Django 5.1.1 on 2025-01-06 19:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_vendor_shipping_address_alter_product_is_flash_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'credit Card'), ('paypal', 'PayPal'), ('bank_transfer', 'Bank Transfer'), ('mpesa', 'Mpesa')], default='credit_card', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('shipped', 'Shipped'), ('delivered', 'Deleivered')], default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]