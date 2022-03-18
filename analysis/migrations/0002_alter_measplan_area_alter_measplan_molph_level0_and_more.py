# Generated by Django 4.0.2 on 2022-03-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measplan',
            name='area',
            field=models.CharField(blank=True, choices=[('4.상용', '상용'), ('6.등산로', '등산로'), ('2.다중이용시설/교통인프라', '다중이용시설/교통인프라'), ('5.개방', '개방'), ('3.커버리지', '커버리지'), ('1.행정동', '행정동'), ('9.해안도로', '해안도로'), ('8.유인도서', '유인도서'), ('7.여객항로', '여객항로')], help_text='측정위치 구분자 선택해주세요.', max_length=30, null=True, verbose_name='측정위치'),
        ),
        migrations.AlterField(
            model_name='measplan',
            name='molph_level0',
            field=models.CharField(blank=True, choices=[('2.중소도시', '중소도시'), ('4.인빌딩', '인빌딩'), ('5.테마', '테마'), ('1.대도시', '대도시'), ('3.농어촌', '농어촌')], help_text='측정위치1 구분자 선택해주세요.', max_length=30, null=True, verbose_name='측정위치1'),
        ),
        migrations.AlterField(
            model_name='measplan',
            name='networkId',
            field=models.CharField(blank=True, choices=[('품질취약지역', '품질취약지역'), ('5G', '5G'), ('WiFi', 'WiFi+'), ('LTE', 'LTE')], help_text='측정 네트워크를 선택해주세요.', max_length=30, null=True, verbose_name='네트워크구분'),
        ),
        migrations.AlterField(
            model_name='measresult',
            name='area',
            field=models.CharField(blank=True, choices=[('4.상용', '상용'), ('6.등산로', '등산로'), ('2.다중이용시설/교통인프라', '다중이용시설/교통인프라'), ('5.개방', '개방'), ('3.커버리지', '커버리지'), ('1.행정동', '행정동'), ('9.해안도로', '해안도로'), ('8.유인도서', '유인도서'), ('7.여객항로', '여객항로')], help_text='측정위치 구분자 선택해주세요.', max_length=30, null=True, verbose_name='측정위치'),
        ),
        migrations.AlterField(
            model_name='measresult',
            name='molph_level0',
            field=models.CharField(blank=True, choices=[('2.중소도시', '중소도시'), ('4.인빌딩', '인빌딩'), ('5.테마', '테마'), ('1.대도시', '대도시'), ('3.농어촌', '농어촌')], help_text='측정위치1 구분자 선택해주세요.', max_length=30, null=True, verbose_name='측정위치1'),
        ),
        migrations.AlterField(
            model_name='measresult',
            name='networkId',
            field=models.CharField(blank=True, choices=[('품질취약지역', '품질취약지역'), ('5G', '5G'), ('WiFi', 'WiFi'), ('LTE', 'LTE')], help_text='측정 네트워크를 선택해주세요.', max_length=30, null=True, verbose_name='네트워크구분'),
        ),
    ]
