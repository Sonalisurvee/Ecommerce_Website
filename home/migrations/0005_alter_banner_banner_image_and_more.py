# Generated by Django 4.1.7 on 2023-03-27 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_carousel_name_carousel_carousel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_image',
            field=models.ImageField(upload_to='banner_image'),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='carousel_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.banner'),
        ),
    ]
