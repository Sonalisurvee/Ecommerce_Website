# Generated by Django 4.1.7 on 2023-03-14 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_mode',
            field=models.CharField(choices=[('cod', 'Cash on Delivery')], default='cod', max_length=150),
        ),
    ]