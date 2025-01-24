# Generated by Django 4.2.18 on 2025-01-24 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WatchData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(unique=True)),
                ('name', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=False)),
                ('ppg_data', models.JSONField()),
                ('imu_data', models.JSONField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wheel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('version', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
