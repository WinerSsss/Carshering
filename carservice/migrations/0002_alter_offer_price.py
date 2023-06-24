# Generated by Django 4.0.6 on 2023-06-18 18:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(100000.0)]),
        ),
    ]
