# Generated by Django 4.0.2 on 2022-02-25 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_alter_register_dong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='dong',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
