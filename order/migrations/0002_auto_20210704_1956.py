# Generated by Django 3.1.4 on 2021-07-04 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.CharField(default='s', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
