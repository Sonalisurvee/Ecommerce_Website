# Generated by Django 4.1.7 on 2023-03-25 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner_image')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.banner')),
            ],
        ),
    ]
