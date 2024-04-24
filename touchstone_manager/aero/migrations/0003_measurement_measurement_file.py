# Generated by Django 5.0.4 on 2024-04-23 13:56

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aero', '0002_materialsample_infiltrations'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='measurement_file',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/uploads'), upload_to='measurements/'),
        ),
    ]