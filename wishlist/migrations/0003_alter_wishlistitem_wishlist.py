# Generated by Django 4.1.7 on 2023-03-13 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_wishlistitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='wishlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wishlist.wishlist'),
        ),
    ]
