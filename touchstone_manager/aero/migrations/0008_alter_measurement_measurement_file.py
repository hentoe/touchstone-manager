# Generated by Django 5.0.4 on 2024-04-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aero', '0007_alter_measurement_measurement_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='measurement_file',
            field=models.FileField(blank=True, upload_to='uploads/measurements/'),
        ),
    ]
