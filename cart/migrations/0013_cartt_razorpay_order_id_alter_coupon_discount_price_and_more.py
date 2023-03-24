# Generated by Django 4.1.7 on 2023-03-24 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_remove_orderitem_order_remove_orderitem_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartt',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount_price',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='minimum_amount',
            field=models.PositiveIntegerField(default=500),
        ),
    ]
