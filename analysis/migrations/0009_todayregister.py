# Generated by Django 4.0.2 on 2022-03-04 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_register_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodayRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('category', models.CharField(blank=True, max_length=10, null=True)),
                ('jiyok', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateField(blank=True, default=datetime.date(2022, 3, 4))),
                ('dongdaco', models.CharField(blank=True, max_length=30, null=True)),
                ('bigsmallnongintheme', models.CharField(blank=True, max_length=10, null=True)),
                ('sanggae', models.CharField(blank=True, max_length=10, null=True)),
                ('weakjiyok', models.CharField(blank=True, max_length=10, null=True)),
                ('total', models.IntegerField(default=0, null=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
