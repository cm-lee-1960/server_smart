# Generated by Django 2.2.1 on 2022-03-10 16:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centerName', models.CharField(max_length=100, verbose_name='센터명')),
                ('channelId', models.CharField(max_length=25, verbose_name='채널ID')),
                ('permissionLevel', models.IntegerField(default=1, verbose_name='권한레벨')),
                ('active', models.BooleanField(default=True, verbose_name='상태')),
            ],
            options={
                'verbose_name': '센터정보',
                'verbose_name_plural': '센터정보',
            },
        ),
        migrations.CreateModel(
            name='Morphology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morphology', models.CharField(blank=True, max_length=100, null=True, verbose_name='모풀로지')),
                ('manage', models.BooleanField(default=False, verbose_name='관리대상')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Center', verbose_name='센터')),
            ],
            options={
                'verbose_name': '모풀로지',
                'verbose_name_plural': '모풀로지',
            },
        ),
        migrations.CreateModel(
            name='SendFailure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areaInd', models.CharField(choices=[('WEEK', '취약지역'), ('NORM', '보통지역')], max_length=10, verbose_name='지역구분')),
                ('networkId', models.CharField(blank=True, choices=[('3G', '3G'), ('WiFi', 'WiFi'), ('5G', '5G'), ('LTE', 'LTE')], max_length=10, null=True, verbose_name='단말유형')),
                ('dataType', models.CharField(choices=[('DL', 'DL'), ('UL', 'UL')], max_length=10, verbose_name='데이터유형')),
                ('bandwidth', models.FloatField(default=0.0, null=True, verbose_name='속도')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Center', verbose_name='센터')),
            ],
            options={
                'verbose_name': '전송실패 기준',
                'verbose_name_plural': '전송실패 기준',
            },
        ),
        migrations.CreateModel(
            name='ReportCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportCycle', models.CharField(max_length=100, verbose_name='보고주기')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Center', verbose_name='센터')),
            ],
            options={
                'verbose_name': '측정 보고주기',
                'verbose_name_plural': '측정 보고주기',
            },
        ),
        migrations.CreateModel(
            name='MorphologyMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.CharField(blank=True, max_length=200, null=True, verbose_name='단어')),
                ('wordsCond', models.CharField(blank=True, choices=[('포함단어', '포함단어'), ('시작단어', '시작단어')], max_length=20, null=True, verbose_name='조건')),
                ('manage', models.BooleanField(default=False, verbose_name='관리대상')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Center', verbose_name='센터')),
                ('morphology', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Morphology', verbose_name='모풀로지')),
            ],
            options={
                'verbose_name': '모풀로지 맵',
                'verbose_name_plural': '모풀로지 맵',
            },
        ),
        migrations.CreateModel(
            name='MeasureingTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measdate', models.DateField(default=datetime.datetime.now, help_text='측정일자를 반드시 입력해야 합니다.', verbose_name='측정일자')),
                ('message', models.TextField(verbose_name='금일 측정조')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Center', verbose_name='센터')),
            ],
            options={
                'verbose_name': '금일 측정조',
                'verbose_name_plural': '금일 측정조',
            },
        ),
        migrations.CreateModel(
            name='LowThroughput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areaInd', models.CharField(choices=[('WEEK', '취약지역'), ('NORM', '보통지역')], max_length=10, verbose_name='지역구분')),
                ('networkId', models.CharField(blank=True, choices=[('3G', '3G'), ('WiFi', 'WiFi'), ('5G', '5G'), ('LTE', 'LTE')], max_length=10, null=True, verbose_name='단말유형')),
                ('dataType', models.CharField(choices=[('DL', 'DL'), ('UL', 'UL')], max_length=10, verbose_name='데이터유형')),
                ('bandwidth', models.FloatField(default=0.0, null=True, verbose_name='속도')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Center', verbose_name='센터')),
            ],
            options={
                'verbose_name': '속도저하 기준',
                'verbose_name_plural': '속도저하 기준',
            },
        ),
    ]
