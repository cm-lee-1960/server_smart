# Generated by Django 4.0.2 on 2022-02-17 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurecalldata',
            name='ispId',
            field=models.CharField(default='45008', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measureseconddata',
            name='ispId',
            field=models.CharField(default='45008', max_length=10),
            preserve_default=False,
        ),
    ]
