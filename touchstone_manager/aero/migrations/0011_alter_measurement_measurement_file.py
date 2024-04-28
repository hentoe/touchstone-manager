# Generated by Django 5.0.4 on 2024-04-26 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aero', '0010_remove_measurement_processing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='measurement_file',
            field=models.FileField(blank=True, upload_to='uploads/measurements/', verbose_name='Touchstone file'),
        ),
    ]