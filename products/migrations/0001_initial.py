# Generated by Django 4.2.8 on 2024-03-26 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('create_at', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('price', models.FloatField(blank=True, help_text='in Indian Rupee Rs', null=True)),
                ('create_at', models.DateField(auto_now_add=True, null=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'ordering': ['-create_at'],
            },
        ),
    ]
