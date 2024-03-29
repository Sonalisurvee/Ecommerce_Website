# Generated by Django 4.1.7 on 2023-03-20 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_cartt_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.coupon'),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
