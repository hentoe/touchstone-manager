# Generated by Django 5.0.4 on 2024-04-28 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aero', '0014_alter_measurement_mean_s21_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='measurement_date',
            field=models.DateTimeField(verbose_name='Measurement date'),
        ),
    ]