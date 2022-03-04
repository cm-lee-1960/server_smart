# Generated by Django 4.0.2 on 2022-03-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_alter_lowthroughput_areaind_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowthroughput',
            name='areaInd',
            field=models.CharField(choices=[('NORM', '보통지역'), ('WEEK', '취약지역')], max_length=10, verbose_name='지역구분'),
        ),
        migrations.AlterField(
            model_name='lowthroughput',
            name='networkId',
            field=models.CharField(blank=True, choices=[('LTE', 'LTE'), ('3G', '3G'), ('WiFi', 'WiFi'), ('5G', '5G')], max_length=10, null=True, verbose_name='단말유형'),
        ),
        migrations.AlterField(
            model_name='morphology',
            name='morphology',
            field=models.CharField(blank=True, choices=[('행정동', '행정동'), ('취약지구', '취약지구'), ('커버리지', '커버리지'), ('테마', '테마'), ('인빌딩', '인빌딩')], max_length=100, null=True, verbose_name='모폴러지'),
        ),
        migrations.AlterField(
            model_name='morphology',
            name='wordsCond',
            field=models.CharField(blank=True, choices=[('포함단어', '포함단어'), ('시작단어', '시작단어')], max_length=20, null=True, verbose_name='조건'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='areaInd',
            field=models.CharField(choices=[('NORM', '보통지역'), ('WEEK', '취약지역')], max_length=10, verbose_name='지역구분'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='networkId',
            field=models.CharField(blank=True, choices=[('LTE', 'LTE'), ('3G', '3G'), ('WiFi', 'WiFi'), ('5G', '5G')], max_length=10, null=True, verbose_name='단말유형'),
        ),
    ]
