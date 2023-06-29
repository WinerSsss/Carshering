import carservice.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_photo', models.ImageField(null=True, upload_to='static/image')),
                ('serial_number', models.CharField(max_length=17, validators=[carservice.models.check_vin_number])),
                ('car_mileage', models.PositiveIntegerField(validators=[carservice.models.validate_mileage])),
                ('car_brand', models.CharField(choices=[('Volkswagen', 'Volkswagen'), ('BMW', 'BMW'), ('Audi', 'Audi'), ('Ford', 'Ford'), ('Opel', 'Opel'), ('Mercedes-Benz', 'Mercedes-Benz'), ('Renault', 'Renault'), ('Skoda', 'Skoda'), ('Toyota', 'Toyota'), ('Peugeot', 'Peugeot'), ('Hyundai', 'Hyundai'), ('Citroën', 'Citroën'), ('Volvo', 'Volvo'), ('Nissan', 'Nissan'), ('Fiat', 'Fiat'), ('Seat', 'Seat'), ('Mazda', 'Mazda'), ('Honda', 'Honda'), ('Suzuki', 'Suzuki'), ('Jeep', 'Jeep'), ('Dacia', 'Dacia'), ('Mitsubishi', 'Mitsubishi'), ('MINI', 'MINI'), ('Other', 'Other')], max_length=30)),
                ('car_model', models.CharField(max_length=30)),
                ('date_of_prod', models.DateField(null=True, validators=[carservice.models.validate_year])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(10.0)])),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carservice.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('active', 'Rent active'), ('finished', 'Rent finished'), ('overdue', 'Rent overdue')], default='active', max_length=30, null=True)),
                ('rent_start', models.DateField(null=True, validators=[carservice.models.past_rent, carservice.models.future_rent, carservice.models.rent_length])),
                ('duration', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(30)])),
                ('offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carservice.offer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
