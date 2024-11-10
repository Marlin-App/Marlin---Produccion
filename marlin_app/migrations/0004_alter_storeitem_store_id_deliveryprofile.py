# Generated by Django 5.1 on 2024-11-01 21:24

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marlin_app', '0003_store_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeitem',
            name='store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='marlin_app.store'),
        ),
        migrations.CreateModel(
            name='DeliveryProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('plate', models.CharField(max_length=10)),
                ('vehicle', models.CharField(choices=[('Carga Liviana', 'Carga Liviana'), ('Liviano', 'Liviano'), ('Bicicleta', 'Bicicleta'), ('Motocicleta', 'Motocicleta')], max_length=20)),
                ('selfie', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('vehicle_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('iD_front_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('iD_back_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('license_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('status', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Bloqueado', 'Bloqueado'), ('Aprobado', 'Aprobado')], default='Pendiente', max_length=100)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
