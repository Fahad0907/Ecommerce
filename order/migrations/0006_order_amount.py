# Generated by Django 3.1.4 on 2021-07-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210728_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]