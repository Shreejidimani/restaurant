# Generated by Django 5.1.5 on 2025-01-31 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base_App', '0004_rename_order_date_order_created_at_order_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='upi_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
