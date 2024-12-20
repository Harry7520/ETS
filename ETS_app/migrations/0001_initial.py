# Generated by Django 2.2 on 2024-02-06 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('birth', models.DateField()),
                ('nrc', models.CharField(max_length=100)),
                ('f_image', models.ImageField(blank=True, default=None, upload_to='NRC')),
                ('b_image', models.ImageField(blank=True, default=None, upload_to='NRC')),
                ('qualification', models.TextField()),
                ('gender', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ETS_app.Gender')),
                ('occupation', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ETS_app.Occupation')),
            ],
        ),
    ]
