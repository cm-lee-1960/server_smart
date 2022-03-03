# Generated by Django 4.0.2 on 2022-03-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_delete_morph_set_morphology_manage_morphology_words_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='morphology',
            name='userInfo2',
        ),
        migrations.AlterField(
            model_name='lowthroughput',
            name='dataType',
            field=models.CharField(choices=[('UL', 'UL'), ('DL', 'DL')], max_length=10, verbose_name='데이터유형'),
        ),
        migrations.AlterField(
            model_name='lowthroughput',
            name='networkId',
            field=models.CharField(blank=True, choices=[('LTE', 'LTE'), ('WiFi', 'WiFi'), ('3G', '3G'), ('5G', '5G')], max_length=10, null=True, verbose_name='단말유형'),
        ),
        migrations.AlterField(
            model_name='morphology',
            name='morphology',
            field=models.CharField(blank=True, choices=[('커버리지', '커버리지'), ('인빌딩', '인빌딩'), ('취약지구', '취약지구'), ('행정동', '행정동'), ('테마', '테마')], max_length=100, null=True, verbose_name='모폴러지'),
        ),
        migrations.AlterField(
            model_name='morphology',
            name='wordsCond',
            field=models.CharField(blank=True, choices=[('포함단어', '포함단어'), ('시작단어', '시작단어')], max_length=20, null=True, verbose_name='조건'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='dataType',
            field=models.CharField(choices=[('UL', 'UL'), ('DL', 'DL')], max_length=10, verbose_name='데이터유형'),
        ),
        migrations.AlterField(
            model_name='sendfailure',
            name='networkId',
            field=models.CharField(blank=True, choices=[('LTE', 'LTE'), ('WiFi', 'WiFi'), ('3G', '3G'), ('5G', '5G')], max_length=10, null=True, verbose_name='단말유형'),
        ),
    ]
