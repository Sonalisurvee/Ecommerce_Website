# Generated by Django 4.1.7 on 2023-03-22 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_remove_cartitem_cart_remove_cartitem_coupon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='coupon',
        ),
        migrations.AddField(
            model_name='cartt',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.coupon'),
        ),
    ]
