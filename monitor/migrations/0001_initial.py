# Generated by Django 4.0 on 2022-04-08 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measdate', models.CharField(max_length=10, verbose_name='측정일자')),
                ('userInfo1', models.CharField(max_length=100, verbose_name='측정자 입력값1')),
                ('userInfo2', models.CharField(max_length=100, verbose_name='측정자 입력값2')),
                ('networkId', models.CharField(blank=True, max_length=100, null=True, verbose_name='유형')),
                ('measuringTeam', models.CharField(blank=True, choices=[('1조', '1조'), ('2조', '2조'), ('3조', '3조'), ('4조', '4조'), ('5조', '5조')], max_length=20, null=True, verbose_name='측정조')),
                ('ispId', models.CharField(blank=True, choices=[('45008', 'KT'), ('45005', 'SKT'), ('45006', 'LGU+')], max_length=10, null=True, verbose_name='통신사')),
                ('downloadBandwidth', models.FloatField(default=0.0, null=True, verbose_name='DL속도')),
                ('uploadBandwidth', models.FloatField(default=0.0, null=True, verbose_name='UL속도')),
                ('dl_count', models.IntegerField(default=0, null=True, verbose_name='DL콜수')),
                ('ul_count', models.IntegerField(default=0, null=True, verbose_name='UL콜수')),
                ('dl_nr_count', models.IntegerField(default=0, null=True)),
                ('ul_nr_count', models.IntegerField(default=0, null=True)),
                ('total_count', models.IntegerField(default=0, null=True)),
                ('dl_nr_percent', models.FloatField(default=0.0, null=True, verbose_name='DL LTE전환율')),
                ('ul_nr_percent', models.FloatField(default=0.0, null=True, verbose_name='UL LTE전환율')),
                ('nr_percent', models.FloatField(default=0.0, null=True, verbose_name='LTE전환율')),
                ('event_count', models.IntegerField(default=0, null=True, verbose_name='이벤트')),
                ('manage', models.BooleanField(default=False, verbose_name='관리대상')),
                ('active', models.BooleanField(default=True, verbose_name='상태')),
                ('last_updated', models.BigIntegerField(blank=True, null=True, verbose_name='최종보고시간')),
                ('last_updated_dt', models.DateTimeField(blank=True, default='2021-11-01 08:57:54', null=True, verbose_name='최종보고시간')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.center', verbose_name='센터')),
                ('morphology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.morphology', verbose_name='모풀로지')),
            ],
            options={
                'verbose_name': '단말 그룹',
                'verbose_name_plural': '단말 그룹',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measdate', models.CharField(max_length=10, verbose_name='측정일자')),
                ('starttime', models.CharField(max_length=10, verbose_name='측정시작시간')),
                ('phone_no', models.BigIntegerField(verbose_name='측정단말')),
                ('meastype', models.CharField(blank=True, choices=[('DL', 'DL'), ('UL', 'UL')], max_length=10, null=True, verbose_name='측정유형')),
                ('userInfo1', models.CharField(max_length=100, verbose_name='측정자 입력값1')),
                ('userInfo2', models.CharField(max_length=100, verbose_name='측정자 입력값2')),
                ('networkId', models.CharField(blank=True, max_length=100, null=True, verbose_name='유형')),
                ('ispId', models.CharField(blank=True, choices=[('45008', 'KT'), ('45005', 'SKT'), ('45006', 'LGU+')], max_length=10, null=True, verbose_name='통신사')),
                ('downloadBandwidth', models.FloatField(default=0.0, null=True, verbose_name='DL')),
                ('uploadBandwidth', models.FloatField(default=0.0, null=True, verbose_name='UL')),
                ('dl_count', models.IntegerField(default=0, null=True, verbose_name='DL콜수')),
                ('ul_count', models.IntegerField(default=0, null=True, verbose_name='UL콜수')),
                ('nr_count', models.IntegerField(default=0, null=True, verbose_name='LTE전환콜수')),
                ('status', models.CharField(choices=[('POWERON', 'PowerOn'), ('START_F', '측정시작'), ('START_M', '측정시작'), ('MEASURING', '측정중'), ('END', '측정종료')], max_length=10, null=True, verbose_name='진행단계')),
                ('currentCount', models.IntegerField(blank=True, null=True, verbose_name='현재 콜카운트')),
                ('total_count', models.IntegerField(default=0, null=True, verbose_name='콜 카운트')),
                ('siDo', models.CharField(blank=True, max_length=100, null=True, verbose_name='시,도')),
                ('guGun', models.CharField(blank=True, max_length=100, null=True, verbose_name='군,구')),
                ('addressDetail', models.CharField(blank=True, max_length=100, null=True, verbose_name='상세주소')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='위도')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='경도')),
                ('last_updated', models.BigIntegerField(blank=True, null=True, verbose_name='최종보고시간')),
                ('manage', models.BooleanField(default=False, verbose_name='관리대상')),
                ('active', models.BooleanField(default=True, verbose_name='상태')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.center', verbose_name='센터')),
                ('morphology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.morphology', verbose_name='모풀로지')),
                ('phoneGroup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phonegroup')),
            ],
            options={
                'verbose_name': '측정 단말',
                'verbose_name_plural': '측정 단말',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10, null=True)),
                ('measdate', models.CharField(max_length=10)),
                ('sendType', models.CharField(max_length=10)),
                ('userInfo1', models.CharField(blank=True, max_length=100, null=True)),
                ('currentCount', models.IntegerField(blank=True, null=True)),
                ('phone_no', models.BigIntegerField(blank=True, null=True)),
                ('downloadBandwidth', models.FloatField(blank=True, null=True)),
                ('uploadBandwidth', models.FloatField(blank=True, null=True)),
                ('messageType', models.CharField(max_length=10)),
                ('message', models.TextField(default=False)),
                ('channelId', models.CharField(max_length=25)),
                ('sended', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='생성일시')),
                ('sendTime', models.DateTimeField(auto_now=True, verbose_name='보낸시간')),
                ('telemessageId', models.BigIntegerField(blank=True, null=True)),
                ('isDel', models.BooleanField(default=False, verbose_name='회수여부')),
                ('phone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phone')),
            ],
        ),
        migrations.CreateModel(
            name='MeasuringDayClose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measdate', models.CharField(max_length=10, verbose_name='측정일자')),
                ('userInfo1', models.CharField(max_length=100, verbose_name='측정자 입력값1')),
                ('networkId', models.CharField(blank=True, max_length=100, null=True, verbose_name='유형')),
                ('downloadBandwidth', models.FloatField(blank=True, null=True, verbose_name='DL')),
                ('uploadBandwidth', models.FloatField(blank=True, null=True, verbose_name='UL')),
                ('dl_count', models.IntegerField(default=0, null=True, verbose_name='DL콜카운트')),
                ('ul_count', models.IntegerField(default=0, null=True, verbose_name='UL콜카운트')),
                ('dl_nr_count', models.IntegerField(default=0, null=True, verbose_name='DL NR 콜카운트')),
                ('ul_nr_count', models.IntegerField(default=0, null=True, verbose_name='UL NR 콜카운트')),
                ('dl_nr_percent', models.FloatField(default=0.0, null=True, verbose_name='DL LTE전환율')),
                ('ul_nr_percent', models.FloatField(default=0.0, null=True, verbose_name='UL LTE전환율')),
                ('connect_time', models.FloatField(default=0.0, null=True, verbose_name='접속시간')),
                ('udpJitter', models.FloatField(default=0.0, null=True, verbose_name='지연시간')),
                ('total_count', models.IntegerField(default=0, null=True, verbose_name='시도호수')),
                ('success_rate', models.FloatField(default=0.0, null=True, verbose_name='전송성공율')),
                ('ca1_count', models.IntegerField(default=0, null=True, verbose_name='CA1 카운트')),
                ('ca2_count', models.IntegerField(default=0, null=True, verbose_name='CA2 카운트')),
                ('ca3_count', models.IntegerField(default=0, null=True, verbose_name='CA3 카운트')),
                ('ca4_count', models.IntegerField(default=0, null=True, verbose_name='CA4 카운트')),
                ('ca1_rate', models.FloatField(default=0, null=True, verbose_name='CA1 비율')),
                ('ca2_rate', models.FloatField(default=0, null=True, verbose_name='CA2 비율')),
                ('ca3_rate', models.FloatField(default=0, null=True, verbose_name='CA3 비율')),
                ('ca4_rate', models.FloatField(default=0, null=True, verbose_name='CA4 비율')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.center', verbose_name='센터')),
                ('morphology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='management.morphology', verbose_name='모풀로지')),
                ('phoneGroup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phonegroup', verbose_name='단말그룹')),
            ],
        ),
        migrations.CreateModel(
            name='MeasureSecondData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataType', models.CharField(max_length=10)),
                ('phone_no', models.BigIntegerField(blank=True, null=True)),
                ('meastime', models.BigIntegerField(blank=True, null=True)),
                ('neworkid', models.CharField(blank=True, max_length=100, null=True)),
                ('groupId', models.CharField(blank=True, max_length=100, null=True)),
                ('currentTime', models.CharField(blank=True, max_length=100, null=True)),
                ('timeline', models.CharField(blank=True, max_length=100, null=True)),
                ('cellId', models.CharField(blank=True, max_length=100, null=True)),
                ('currentCount', models.IntegerField(blank=True, null=True)),
                ('ispId', models.CharField(blank=True, max_length=10, null=True)),
                ('testNetworkType', models.CharField(blank=True, max_length=100, null=True)),
                ('userInfo1', models.CharField(blank=True, max_length=100, null=True)),
                ('userInfo2', models.CharField(blank=True, max_length=100, null=True)),
                ('siDo', models.CharField(blank=True, max_length=100, null=True)),
                ('guGun', models.CharField(blank=True, max_length=100, null=True)),
                ('addressDetail', models.CharField(blank=True, max_length=100, null=True)),
                ('udpJitter', models.FloatField(blank=True, null=True)),
                ('downloadBandwidth', models.FloatField(blank=True, null=True)),
                ('uploadBandwidth', models.FloatField(blank=True, null=True)),
                ('sinr', models.FloatField(blank=True, null=True)),
                ('isWifi', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('bandType', models.CharField(blank=True, max_length=16, null=True)),
                ('p_dl_earfcn', models.IntegerField(blank=True, null=True)),
                ('p_pci', models.IntegerField(blank=True, null=True)),
                ('p_rsrp', models.FloatField(blank=True, null=True)),
                ('NR_EARFCN', models.IntegerField(blank=True, null=True)),
                ('NR_PCI', models.IntegerField(blank=True, null=True)),
                ('NR_RSRP', models.FloatField(blank=True, null=True)),
                ('NR_SINR', models.FloatField(blank=True, null=True)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phone')),
            ],
        ),
        migrations.CreateModel(
            name='MeasureCallData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataType', models.CharField(max_length=10)),
                ('phone_no', models.BigIntegerField(blank=True, null=True, verbose_name='전화번호')),
                ('meastime', models.BigIntegerField(blank=True, null=True, verbose_name='측정시간')),
                ('networkId', models.CharField(blank=True, max_length=100, null=True, verbose_name='유형')),
                ('groupId', models.CharField(blank=True, max_length=100, null=True)),
                ('currentTime', models.CharField(blank=True, max_length=100, null=True)),
                ('timeline', models.CharField(blank=True, max_length=100, null=True)),
                ('cellId', models.CharField(blank=True, max_length=100, null=True, verbose_name='셀ID')),
                ('currentCount', models.IntegerField(blank=True, null=True, verbose_name='콜카운트')),
                ('ispId', models.CharField(blank=True, max_length=10, null=True)),
                ('testNetworkType', models.CharField(blank=True, max_length=100, null=True)),
                ('userInfo1', models.CharField(blank=True, max_length=100, null=True, verbose_name='측정자 입력값1')),
                ('userInfo2', models.CharField(blank=True, max_length=100, null=True, verbose_name='측정자 입력값2')),
                ('siDo', models.CharField(blank=True, max_length=100, null=True)),
                ('guGun', models.CharField(blank=True, max_length=100, null=True)),
                ('addressDetail', models.CharField(blank=True, max_length=100, null=True, verbose_name='주소상세')),
                ('udpJitter', models.FloatField(blank=True, null=True)),
                ('downloadBandwidth', models.FloatField(blank=True, null=True, verbose_name='DL')),
                ('uploadBandwidth', models.FloatField(blank=True, null=True, verbose_name='UL')),
                ('sinr', models.FloatField(blank=True, null=True)),
                ('isWifi', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('bandType', models.CharField(blank=True, max_length=16, null=True)),
                ('p_dl_earfcn', models.IntegerField(blank=True, null=True)),
                ('p_pci', models.IntegerField(blank=True, null=True)),
                ('p_rsrp', models.FloatField(blank=True, null=True)),
                ('p_SINR', models.FloatField(blank=True, null=True)),
                ('NR_EARFCN', models.IntegerField(blank=True, null=True)),
                ('NR_PCI', models.IntegerField(blank=True, null=True)),
                ('NR_RSRP', models.FloatField(blank=True, null=True)),
                ('NR_SINR', models.FloatField(blank=True, null=True)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phone')),
            ],
            options={
                'verbose_name': '측정 데이터(콜단위)',
                'verbose_name_plural': '측정 데이터(콜단위)',
            },
        ),
    ]
