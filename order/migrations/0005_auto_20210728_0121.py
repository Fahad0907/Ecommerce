# Generated by Django 3.1.4 on 2021-07-27 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_delivered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='paymentType',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]