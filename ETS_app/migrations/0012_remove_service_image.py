# Generated by Django 2.2 on 2024-05-10 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ETS_app', '0011_auto_20240510_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='image',
        ),
    ]
