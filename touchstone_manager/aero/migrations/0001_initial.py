# Generated by Django 5.0.4 on 2024-04-23 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name of Material')),
                ('short_name', models.CharField(max_length=30, verbose_name='Abbreviated name of Material')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaterialSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name of Sample')),
                ('sample_number', models.IntegerField(unique=True, verbose_name='Number of Sample')),
                ('thickness', models.FloatField(verbose_name='Thickness in mm')),
                ('weight', models.FloatField(verbose_name='Weight in mg')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aero.material', verbose_name='Material')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('measurement_date', models.DateField(verbose_name='Measurement date')),
                ('mean_s21', models.FloatField(verbose_name='Mean S21 over frequency range')),
                ('aero_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aero.materialsample', verbose_name='Device under Test')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
