# Generated by Django 4.1.7 on 2023-04-02 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_alter_cartt_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='color_variant',
        ),
    ]