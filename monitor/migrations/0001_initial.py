# Generated by Django 4.0.2 on 2022-02-20 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupId', models.CharField(max_length=100)),
                ('userInfo1', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_type', models.CharField(max_length=5, verbose_name='구분')),
                ('phone_no', models.BigIntegerField(verbose_name='측정단말')),
                ('networkId', models.CharField(blank=True, max_length=100, null=True, verbose_name='유형')),
                ('avg_downloadBandwidth', models.FloatField(default=0.0, null=True, verbose_name='DL')),
                ('avg_uploadBandwidth', models.FloatField(default=0.0, null=True, verbose_name='UL')),
                ('status', models.CharField(max_length=10, null=True, verbose_name='진행단계')),
                ('total_count', models.IntegerField(default=0, null=True, verbose_name='콜 카운트')),
                ('last_updated', models.BigIntegerField(blank=True, null=True, verbose_name='최종보고시간')),
                ('active', models.BooleanField(default=True, verbose_name='상태')),
                ('phoneGroup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phonegroup')),
            ],
            options={
                'verbose_name': '측정단말',
                'verbose_name_plural': '측정단말',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_type', models.CharField(max_length=10)),
                ('currentCount', models.IntegerField()),
                ('message', models.TextField()),
                ('channelId', models.CharField(max_length=25)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.phone')),
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
                ('phone_no', models.BigIntegerField(blank=True, null=True)),
                ('meastime', models.BigIntegerField(blank=True, null=True)),
                ('networkId', models.CharField(blank=True, max_length=100, null=True)),
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
    ]
