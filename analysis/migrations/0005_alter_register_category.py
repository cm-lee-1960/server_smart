# Generated by Django 4.0.2 on 2022-02-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_alter_register_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='category',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]