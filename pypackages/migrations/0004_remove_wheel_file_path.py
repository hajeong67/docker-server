# Generated by Django 4.2.18 on 2025-02-05 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pypackages', '0003_wheel_whl_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wheel',
            name='file_path',
        ),
    ]
