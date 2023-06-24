# Generated by Django 4.0.6 on 2023-06-24 17:12

import carservice.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carservice', '0002_remove_car_car_year_car_year_of_prod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='rent_start',
            field=models.DateField(null=True, validators=[carservice.models.val_rent, carservice.models.future_rent]),
        ),
        migrations.AlterField(
            model_name='rent',
            name='rent_stop',
            field=models.DateField(null=True, validators=[carservice.models.val_rent, carservice.models.rent_length]),
        ),
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Rent active'), ('finished', 'Rent finished')], default='active', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='rent',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
