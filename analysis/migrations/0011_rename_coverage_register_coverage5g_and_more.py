# Generated by Django 4.0.2 on 2022-03-08 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0010_alter_todayregister_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='coverage',
            new_name='coverage5g',
        ),
        migrations.AddField(
            model_name='register',
            name='coveragelte',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
