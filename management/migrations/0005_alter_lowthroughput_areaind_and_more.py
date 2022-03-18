# Generated by Django 4.0.2 on 2022-03-18 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_lowthroughput_datatype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowthroughput',
            name='areaInd',
            field=models.CharField(choices=[('WEEK', '취약지역'), ('NORM', '보통지역')], max_length=10, verbose_name='지역구분'),
        ),
        migrations.AlterField(
            model_name='lowthroughput',
            name='dataType',
            field=models.CharField(choices=[('DL', 'DL'), ('UL', 'UL')], max_length=10, verbose_name='데이터유형'),
        ),
        migrations.AlterField(
            model_name='lowthroughput',
            name='networkId',
            field=models.CharField(blank=True, choices=[('WiFi', 'WiFi'), ('LTE', 'LTE'), ('3G', '3G'), ('5G', '5G')], max_length=10, null=True, verbose_name='단말유형'),
        ),
        migrations.AlterField(
            model_name='morphologymap',
            name='wordsCond',
            field=models.CharField(blank=True, choices=[('포함단어', '포함단어'), ('시작단어', '시작단어')], max_length=20, null=True, verbose_name='조건'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='areaInd',
            field=models.CharField(choices=[('WEEK', '취약지역'), ('NORM', '보통지역')], max_length=10, verbose_name='지역구분'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='dataType',
            field=models.CharField(choices=[('DL', 'DL'), ('UL', 'UL')], max_length=10, verbose_name='데이터유형'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='networkId',
            field=models.CharField(blank=True, choices=[('WiFi', 'WiFi'), ('LTE', 'LTE'), ('3G', '3G'), ('5G', '5G')], max_length=10, null=True, verbose_name='단말유형'),
        ),
    ]
