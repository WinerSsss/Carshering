# Generated by Django 4.0.6 on 2023-06-19 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carservice', '0006_remove_rent_status_field_rent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.CharField(max_length=30),
        ),
    ]
