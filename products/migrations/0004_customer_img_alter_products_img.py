# Generated by Django 4.2.8 on 2024-03-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_products_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
