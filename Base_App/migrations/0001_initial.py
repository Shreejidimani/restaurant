# Generated by Django 5.1.5 on 2025-01-29 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BookTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=15)),
                ('Phone_number', models.IntegerField()),
                ('Email', models.EmailField(max_length=254)),
                ('Total_person', models.IntegerField()),
                ('Booking_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_name', models.CharField(max_length=15)),
                ('Description', models.TextField()),
                ('Rating', models.IntegerField()),
                ('Image', models.ImageField(blank=True, upload_to='items/')),
            ],
        ),
        migrations.CreateModel(
            name='ItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item_name', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('Price', models.IntegerField()),
                ('Image', models.ImageField(upload_to='items/')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Name', to='Base_App.itemlist')),
            ],
        ),
    ]
