# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class TbNdmDataMeasure(models.Model):
    phone_no = models.BigIntegerField(blank=True, null=True)
    meastime = models.BigIntegerField(blank=True, null=True)
    scenarioid = models.CharField(db_column='scenarioId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    elementtype = models.CharField(db_column='elementType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    elementid = models.CharField(db_column='elementId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    measuringtype = models.CharField(db_column='measuringType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    measuringmode = models.CharField(db_column='measuringMode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    extrasubject = models.CharField(db_column='extraSubject', max_length=100, blank=True, null=True)  # Field name made lowercase.
    subsid = models.CharField(db_column='subsId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deviceid = models.CharField(db_column='deviceId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deviceos = models.CharField(db_column='deviceOs', max_length=100, blank=True, null=True)  # Field name made lowercase.
    devicekind = models.CharField(db_column='deviceKind', max_length=100, blank=True, null=True)  # Field name made lowercase.
    networkid = models.CharField(db_column='networkId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    groupid = models.CharField(db_column='groupId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    starttime = models.CharField(db_column='startTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    endtime = models.CharField(db_column='endTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    currenttime = models.CharField(db_column='currentTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timeline = models.CharField(max_length=100, blank=True, null=True)
    cellid = models.CharField(db_column='cellId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    currentcount = models.IntegerField(db_column='currentCount', blank=True, null=True)  # Field name made lowercase.
    ispid = models.CharField(db_column='ispId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    branchid = models.CharField(db_column='branchId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    testnetworktype = models.CharField(db_column='testNetworkType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='contentType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    miid = models.CharField(db_column='miId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    userinfo1 = models.CharField(db_column='userInfo1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    userinfo2 = models.CharField(db_column='userInfo2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(max_length=100, blank=True, null=True)
    sido = models.CharField(db_column='siDo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gugun = models.CharField(db_column='guGun', max_length=100, blank=True, null=True)  # Field name made lowercase.
    addressdetail = models.CharField(db_column='addressDetail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    battery_temp = models.CharField(max_length=10, blank=True, null=True)
    cpu_temp = models.CharField(max_length=10, blank=True, null=True)
    udptransfer = models.IntegerField(db_column='udpTransfer', blank=True, null=True)  # Field name made lowercase.
    udpjitter = models.FloatField(db_column='udpJitter', blank=True, null=True)  # Field name made lowercase.
    udploss = models.FloatField(db_column='udpLoss', blank=True, null=True)  # Field name made lowercase.
    udperrorcode = models.CharField(db_column='udpErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    downloadtransfer = models.IntegerField(db_column='downloadTransfer', blank=True, null=True)  # Field name made lowercase.
    downloadbandwidth = models.FloatField(db_column='downloadBandwidth', blank=True, null=True)  # Field name made lowercase.
    downloadelapse = models.FloatField(db_column='downloadElapse', blank=True, null=True)  # Field name made lowercase.
    downloadconnectionsuccess = models.FloatField(db_column='downloadConnectionSuccess', blank=True, null=True)  # Field name made lowercase.
    downloadnetworkvalidation = models.IntegerField(db_column='downloadNetworkValidation', blank=True, null=True)  # Field name made lowercase.
    downloaderrorcode = models.CharField(db_column='downloadErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uploadtransfer = models.IntegerField(db_column='uploadTransfer', blank=True, null=True)  # Field name made lowercase.
    uploadbandwidth = models.FloatField(db_column='uploadBandwidth', blank=True, null=True)  # Field name made lowercase.
    uploadelapse = models.FloatField(db_column='uploadElapse', blank=True, null=True)  # Field name made lowercase.
    uploadconnectionsuccess = models.FloatField(db_column='uploadConnectionSuccess', blank=True, null=True)  # Field name made lowercase.
    uploadnetworkvalidation = models.IntegerField(db_column='uploadNetworkValidation', blank=True, null=True)  # Field name made lowercase.
    uploaderrorcode = models.CharField(db_column='uploadErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url0 = models.CharField(max_length=100, blank=True, null=True)
    transfer0 = models.IntegerField(blank=True, null=True)
    interval0 = models.FloatField(blank=True, null=True)
    urlerrorcode0 = models.CharField(db_column='urlErrorCode0', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url1 = models.CharField(max_length=100, blank=True, null=True)
    transfer1 = models.IntegerField(blank=True, null=True)
    interval1 = models.FloatField(blank=True, null=True)
    urlerrorcode1 = models.CharField(db_column='urlErrorCode1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url2 = models.CharField(max_length=100, blank=True, null=True)
    transfer2 = models.IntegerField(blank=True, null=True)
    interval2 = models.FloatField(blank=True, null=True)
    urlerrorcode2 = models.CharField(db_column='urlErrorCode2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url3 = models.CharField(max_length=100, blank=True, null=True)
    transfer3 = models.IntegerField(blank=True, null=True)
    interval3 = models.FloatField(blank=True, null=True)
    urlerrorcode3 = models.CharField(db_column='urlErrorCode3', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url4 = models.CharField(max_length=100, blank=True, null=True)
    transfer4 = models.IntegerField(blank=True, null=True)
    interval4 = models.FloatField(blank=True, null=True)
    urlerrorcode4 = models.CharField(db_column='urlErrorCode4', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url5 = models.CharField(max_length=100, blank=True, null=True)
    transfer5 = models.IntegerField(blank=True, null=True)
    interval5 = models.FloatField(blank=True, null=True)
    urlerrorcode5 = models.CharField(db_column='urlErrorCode5', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url6 = models.CharField(max_length=100, blank=True, null=True)
    transfer6 = models.IntegerField(blank=True, null=True)
    interval6 = models.FloatField(blank=True, null=True)
    urlerrorcode6 = models.CharField(db_column='urlErrorCode6', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url7 = models.CharField(max_length=100, blank=True, null=True)
    transfer7 = models.IntegerField(blank=True, null=True)
    interval7 = models.FloatField(blank=True, null=True)
    urlerrorcode7 = models.CharField(db_column='urlErrorCode7', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url8 = models.CharField(max_length=100, blank=True, null=True)
    transfer8 = models.IntegerField(blank=True, null=True)
    interval8 = models.FloatField(blank=True, null=True)
    urlerrorcode8 = models.CharField(db_column='urlErrorCode8', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url9 = models.CharField(max_length=100, blank=True, null=True)
    transfer9 = models.IntegerField(blank=True, null=True)
    interval9 = models.FloatField(blank=True, null=True)
    urlerrorcode9 = models.CharField(db_column='urlErrorCode9', max_length=100, blank=True, null=True)  # Field name made lowercase.
    connectionsuccess = models.CharField(db_column='connectionSuccess', max_length=100, blank=True, null=True)  # Field name made lowercase.
    networkvalidation = models.CharField(db_column='networkValidation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    webtesterrorcode = models.CharField(db_column='webTestErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    weburltype = models.CharField(db_column='webUrlType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    totalweburlcount = models.IntegerField(db_column='totalWebUrlCount', blank=True, null=True)  # Field name made lowercase.
    transfercompletion = models.CharField(db_column='transferCompletion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isregistered = models.CharField(db_column='isRegistered', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grade = models.IntegerField(blank=True, null=True)
    phonenumber = models.BigIntegerField(db_column='phoneNumber', blank=True, null=True)  # Field name made lowercase.
    rssi = models.FloatField(blank=True, null=True)
    ber = models.IntegerField(blank=True, null=True)
    sinr = models.FloatField(blank=True, null=True)
    txpower = models.FloatField(db_column='txPower', blank=True, null=True)  # Field name made lowercase.
    rsrp = models.FloatField(blank=True, null=True)
    rscp = models.FloatField(blank=True, null=True)
    band = models.IntegerField(blank=True, null=True)
    psc = models.IntegerField(blank=True, null=True)
    networktype = models.IntegerField(db_column='networkType', blank=True, null=True)  # Field name made lowercase.
    countrycode = models.CharField(db_column='countryCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isgsm = models.CharField(db_column='isGsm', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nonwifisignalstrength = models.IntegerField(db_column='nonWifiSignalStrength', blank=True, null=True)  # Field name made lowercase.
    nonwifisignallevel = models.IntegerField(db_column='nonWifiSignalLevel', blank=True, null=True)  # Field name made lowercase.
    iswifi = models.CharField(db_column='isWifi', max_length=100, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    wifi_rssi = models.CharField(max_length=100, blank=True, null=True)
    wifi_ssid = models.CharField(db_column='wifi_ssId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_bssid = models.CharField(db_column='wifi_bssId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_ipaddress = models.CharField(db_column='wifi_ipAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_macaddress = models.CharField(db_column='wifi_macAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_wifisignallevel = models.CharField(db_column='wifi_wifiSignalLevel', max_length=100, blank=True, null=True)  # Field name made lowercase.
    recordtype = models.IntegerField(db_column='recordType', blank=True, null=True)  # Field name made lowercase.
    bandtype = models.CharField(db_column='bandType', max_length=16, blank=True, null=True)  # Field name made lowercase.
    p_dl_earfcn = models.IntegerField(blank=True, null=True)
    p_pci = models.IntegerField(blank=True, null=True)
    p_rb = models.FloatField(blank=True, null=True)
    p_rsrp = models.FloatField(blank=True, null=True)
    p_pdsch = models.FloatField(blank=True, null=True)
    p_pusch = models.FloatField(blank=True, null=True)
    s1_dl_earfcn = models.IntegerField(blank=True, null=True)
    s1_pci = models.IntegerField(blank=True, null=True)
    s1_rb = models.FloatField(blank=True, null=True)
    s1_rsrp = models.FloatField(blank=True, null=True)
    s1_psch = models.FloatField(blank=True, null=True)
    s2_dl_earfcn = models.IntegerField(blank=True, null=True)
    s2_pci = models.IntegerField(blank=True, null=True)
    s2_rb = models.FloatField(blank=True, null=True)
    s2_rsrp = models.FloatField(blank=True, null=True)
    s2_psch = models.FloatField(blank=True, null=True)
    s3_earfcn = models.IntegerField(db_column='s3_EARFCN', blank=True, null=True)  # Field name made lowercase.
    s4_earfcn = models.IntegerField(db_column='s4_EARFCN', blank=True, null=True)  # Field name made lowercase.
    s3_pci = models.IntegerField(db_column='s3_PCI', blank=True, null=True)  # Field name made lowercase.
    s4_pci = models.IntegerField(db_column='s4_PCI', blank=True, null=True)  # Field name made lowercase.
    s3_rb = models.FloatField(db_column='s3_RB', blank=True, null=True)  # Field name made lowercase.
    s4_rb = models.FloatField(db_column='s4_RB', blank=True, null=True)  # Field name made lowercase.
    s3_rsrp = models.FloatField(db_column='s3_RSRP', blank=True, null=True)  # Field name made lowercase.
    s4_rsrp = models.FloatField(db_column='s4_RSRP', blank=True, null=True)  # Field name made lowercase.
    s3_pdsch = models.FloatField(db_column='s3_PDSCH', blank=True, null=True)  # Field name made lowercase.
    s4_pdsch = models.FloatField(db_column='s4_PDSCH', blank=True, null=True)  # Field name made lowercase.
    nr_earfcn = models.IntegerField(db_column='NR_EARFCN', blank=True, null=True)  # Field name made lowercase.
    nr_pci = models.IntegerField(db_column='NR_PCI', blank=True, null=True)  # Field name made lowercase.
    nr_rsrp = models.FloatField(db_column='NR_RSRP', blank=True, null=True)  # Field name made lowercase.
    nr_rsrq = models.FloatField(db_column='NR_RSRQ', blank=True, null=True)  # Field name made lowercase.
    nr_sinr = models.FloatField(db_column='NR_SINR', blank=True, null=True)  # Field name made lowercase.
    nr_ssb = models.FloatField(db_column='NR_SSB', blank=True, null=True)  # Field name made lowercase.
    nr_rb = models.FloatField(db_column='NR_RB', blank=True, null=True)  # Field name made lowercase.
    p_sinr = models.FloatField(db_column='p_SINR', blank=True, null=True)  # Field name made lowercase.
    s1_sinr = models.FloatField(db_column='s1_SINR', blank=True, null=True)  # Field name made lowercase.
    s2_sinr = models.FloatField(db_column='s2_SINR', blank=True, null=True)  # Field name made lowercase.
    s3_sinr = models.FloatField(db_column='s3_SINR', blank=True, null=True)  # Field name made lowercase.
    s4_sinr = models.FloatField(db_column='s4_SINR', blank=True, null=True)  # Field name made lowercase.
    mobile_ip = models.CharField(max_length=40, blank=True, null=True)
    before_lat = models.FloatField(blank=True, null=True)
    before_lon = models.FloatField(blank=True, null=True)
    savetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_ndm_data_measure'


class TbNdmDataSampleMeasure(models.Model):
    phone_no = models.BigIntegerField(blank=True, null=True)
    meastime = models.BigIntegerField(blank=True, null=True)
    scenarioid = models.CharField(db_column='scenarioId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    elementtype = models.CharField(db_column='elementType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    elementid = models.CharField(db_column='elementId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    measuringtype = models.CharField(db_column='measuringType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    measuringmode = models.CharField(db_column='measuringMode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    extrasubject = models.CharField(db_column='extraSubject', max_length=100, blank=True, null=True)  # Field name made lowercase.
    subsid = models.CharField(db_column='subsId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deviceid = models.CharField(db_column='deviceId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    deviceos = models.CharField(db_column='deviceOs', max_length=100, blank=True, null=True)  # Field name made lowercase.
    devicekind = models.CharField(db_column='deviceKind', max_length=100, blank=True, null=True)  # Field name made lowercase.
    networkid = models.CharField(db_column='networkId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    groupid = models.CharField(db_column='groupId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    starttime = models.CharField(db_column='startTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    endtime = models.CharField(db_column='endTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    currenttime = models.CharField(db_column='currentTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timeline = models.CharField(max_length=100, blank=True, null=True)
    cellid = models.CharField(db_column='cellId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    currentcount = models.IntegerField(db_column='currentCount', blank=True, null=True)  # Field name made lowercase.
    ispid = models.CharField(db_column='ispId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    branchid = models.CharField(db_column='branchId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    testnetworktype = models.CharField(db_column='testNetworkType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='contentType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    miid = models.CharField(db_column='miId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    userinfo1 = models.CharField(db_column='userInfo1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    userinfo2 = models.CharField(db_column='userInfo2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(max_length=100, blank=True, null=True)
    sido = models.CharField(db_column='siDo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gugun = models.CharField(db_column='guGun', max_length=100, blank=True, null=True)  # Field name made lowercase.
    addressdetail = models.CharField(db_column='addressDetail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    battery_temp = models.CharField(max_length=10, blank=True, null=True)
    cpu_temp = models.CharField(max_length=10, blank=True, null=True)
    udptransfer = models.IntegerField(db_column='udpTransfer', blank=True, null=True)  # Field name made lowercase.
    udpjitter = models.FloatField(db_column='udpJitter', blank=True, null=True)  # Field name made lowercase.
    udploss = models.FloatField(db_column='udpLoss', blank=True, null=True)  # Field name made lowercase.
    udperrorcode = models.CharField(db_column='udpErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    downloadtransfer = models.IntegerField(db_column='downloadTransfer', blank=True, null=True)  # Field name made lowercase.
    downloadbandwidth = models.FloatField(db_column='downloadBandwidth', blank=True, null=True)  # Field name made lowercase.
    downloadelapse = models.FloatField(db_column='downloadElapse', blank=True, null=True)  # Field name made lowercase.
    downloadconnectionsuccess = models.FloatField(db_column='downloadConnectionSuccess', blank=True, null=True)  # Field name made lowercase.
    downloadnetworkvalidation = models.IntegerField(db_column='downloadNetworkValidation', blank=True, null=True)  # Field name made lowercase.
    downloaderrorcode = models.CharField(db_column='downloadErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uploadtransfer = models.IntegerField(db_column='uploadTransfer', blank=True, null=True)  # Field name made lowercase.
    uploadbandwidth = models.FloatField(db_column='uploadBandwidth', blank=True, null=True)  # Field name made lowercase.
    uploadelapse = models.FloatField(db_column='uploadElapse', blank=True, null=True)  # Field name made lowercase.
    uploadconnectionsuccess = models.FloatField(db_column='uploadConnectionSuccess', blank=True, null=True)  # Field name made lowercase.
    uploadnetworkvalidation = models.IntegerField(db_column='uploadNetworkValidation', blank=True, null=True)  # Field name made lowercase.
    uploaderrorcode = models.CharField(db_column='uploadErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url0 = models.CharField(max_length=100, blank=True, null=True)
    transfer0 = models.IntegerField(blank=True, null=True)
    interval0 = models.FloatField(blank=True, null=True)
    urlerrorcode0 = models.CharField(db_column='urlErrorCode0', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url1 = models.CharField(max_length=100, blank=True, null=True)
    transfer1 = models.IntegerField(blank=True, null=True)
    interval1 = models.FloatField(blank=True, null=True)
    urlerrorcode1 = models.CharField(db_column='urlErrorCode1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url2 = models.CharField(max_length=100, blank=True, null=True)
    transfer2 = models.IntegerField(blank=True, null=True)
    interval2 = models.FloatField(blank=True, null=True)
    urlerrorcode2 = models.CharField(db_column='urlErrorCode2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url3 = models.CharField(max_length=100, blank=True, null=True)
    transfer3 = models.IntegerField(blank=True, null=True)
    interval3 = models.FloatField(blank=True, null=True)
    urlerrorcode3 = models.CharField(db_column='urlErrorCode3', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url4 = models.CharField(max_length=100, blank=True, null=True)
    transfer4 = models.IntegerField(blank=True, null=True)
    interval4 = models.FloatField(blank=True, null=True)
    urlerrorcode4 = models.CharField(db_column='urlErrorCode4', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url5 = models.CharField(max_length=100, blank=True, null=True)
    transfer5 = models.IntegerField(blank=True, null=True)
    interval5 = models.FloatField(blank=True, null=True)
    urlerrorcode5 = models.CharField(db_column='urlErrorCode5', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url6 = models.CharField(max_length=100, blank=True, null=True)
    transfer6 = models.IntegerField(blank=True, null=True)
    interval6 = models.FloatField(blank=True, null=True)
    urlerrorcode6 = models.CharField(db_column='urlErrorCode6', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url7 = models.CharField(max_length=100, blank=True, null=True)
    transfer7 = models.IntegerField(blank=True, null=True)
    interval7 = models.FloatField(blank=True, null=True)
    urlerrorcode7 = models.CharField(db_column='urlErrorCode7', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url8 = models.CharField(max_length=100, blank=True, null=True)
    transfer8 = models.IntegerField(blank=True, null=True)
    interval8 = models.FloatField(blank=True, null=True)
    urlerrorcode8 = models.CharField(db_column='urlErrorCode8', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url9 = models.CharField(max_length=100, blank=True, null=True)
    transfer9 = models.IntegerField(blank=True, null=True)
    interval9 = models.FloatField(blank=True, null=True)
    urlerrorcode9 = models.CharField(db_column='urlErrorCode9', max_length=100, blank=True, null=True)  # Field name made lowercase.
    connectionsuccess = models.CharField(db_column='connectionSuccess', max_length=100, blank=True, null=True)  # Field name made lowercase.
    networkvalidation = models.CharField(db_column='networkValidation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    webtesterrorcode = models.CharField(db_column='webTestErrorCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    weburltype = models.CharField(db_column='webUrlType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    totalweburlcount = models.IntegerField(db_column='totalWebUrlCount', blank=True, null=True)  # Field name made lowercase.
    transfercompletion = models.CharField(db_column='transferCompletion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isregistered = models.CharField(db_column='isRegistered', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grade = models.IntegerField(blank=True, null=True)
    phonenumber = models.BigIntegerField(db_column='phoneNumber', blank=True, null=True)  # Field name made lowercase.
    rssi = models.FloatField(blank=True, null=True)
    ber = models.IntegerField(blank=True, null=True)
    sinr = models.FloatField(blank=True, null=True)
    txpower = models.FloatField(db_column='txPower', blank=True, null=True)  # Field name made lowercase.
    rsrp = models.FloatField(blank=True, null=True)
    rscp = models.FloatField(blank=True, null=True)
    band = models.IntegerField(blank=True, null=True)
    psc = models.IntegerField(blank=True, null=True)
    networktype = models.IntegerField(db_column='networkType', blank=True, null=True)  # Field name made lowercase.
    countrycode = models.CharField(db_column='countryCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isgsm = models.CharField(db_column='isGsm', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nonwifisignalstrength = models.IntegerField(db_column='nonWifiSignalStrength', blank=True, null=True)  # Field name made lowercase.
    nonwifisignallevel = models.IntegerField(db_column='nonWifiSignalLevel', blank=True, null=True)  # Field name made lowercase.
    iswifi = models.CharField(db_column='isWifi', max_length=100, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    wifi_rssi = models.CharField(max_length=100, blank=True, null=True)
    wifi_ssid = models.CharField(db_column='wifi_ssId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_bssid = models.CharField(db_column='wifi_bssId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_ipaddress = models.CharField(db_column='wifi_ipAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_macaddress = models.CharField(db_column='wifi_macAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wifi_wifisignallevel = models.CharField(db_column='wifi_wifiSignalLevel', max_length=100, blank=True, null=True)  # Field name made lowercase.
    recordtype = models.IntegerField(db_column='recordType', blank=True, null=True)  # Field name made lowercase.
    bandtype = models.CharField(db_column='bandType', max_length=16, blank=True, null=True)  # Field name made lowercase.
    p_dl_earfcn = models.IntegerField(blank=True, null=True)
    p_pci = models.IntegerField(blank=True, null=True)
    p_rb = models.FloatField(blank=True, null=True)
    p_rsrp = models.FloatField(blank=True, null=True)
    p_pdsch = models.FloatField(blank=True, null=True)
    p_pusch = models.FloatField(blank=True, null=True)
    s1_dl_earfcn = models.IntegerField(blank=True, null=True)
    s1_pci = models.IntegerField(blank=True, null=True)
    s1_rb = models.FloatField(blank=True, null=True)
    s1_rsrp = models.FloatField(blank=True, null=True)
    s1_psch = models.FloatField(blank=True, null=True)
    s2_dl_earfcn = models.IntegerField(blank=True, null=True)
    s2_pci = models.IntegerField(blank=True, null=True)
    s2_rb = models.FloatField(blank=True, null=True)
    s2_rsrp = models.FloatField(blank=True, null=True)
    s2_psch = models.FloatField(blank=True, null=True)
    s3_earfcn = models.IntegerField(db_column='s3_EARFCN', blank=True, null=True)  # Field name made lowercase.
    s4_earfcn = models.IntegerField(db_column='s4_EARFCN', blank=True, null=True)  # Field name made lowercase.
    s3_pci = models.IntegerField(db_column='s3_PCI', blank=True, null=True)  # Field name made lowercase.
    s4_pci = models.IntegerField(db_column='s4_PCI', blank=True, null=True)  # Field name made lowercase.
    s3_rb = models.FloatField(db_column='s3_RB', blank=True, null=True)  # Field name made lowercase.
    s4_rb = models.FloatField(db_column='s4_RB', blank=True, null=True)  # Field name made lowercase.
    s3_rsrp = models.FloatField(db_column='s3_RSRP', blank=True, null=True)  # Field name made lowercase.
    s4_rsrp = models.FloatField(db_column='s4_RSRP', blank=True, null=True)  # Field name made lowercase.
    s3_pdsch = models.FloatField(db_column='s3_PDSCH', blank=True, null=True)  # Field name made lowercase.
    s4_pdsch = models.FloatField(db_column='s4_PDSCH', blank=True, null=True)  # Field name made lowercase.
    nr_earfcn = models.IntegerField(db_column='NR_EARFCN', blank=True, null=True)  # Field name made lowercase.
    nr_pci = models.IntegerField(db_column='NR_PCI', blank=True, null=True)  # Field name made lowercase.
    nr_rsrp = models.FloatField(db_column='NR_RSRP', blank=True, null=True)  # Field name made lowercase.
    nr_rsrq = models.FloatField(db_column='NR_RSRQ', blank=True, null=True)  # Field name made lowercase.
    nr_sinr = models.FloatField(db_column='NR_SINR', blank=True, null=True)  # Field name made lowercase.
    nr_ssb = models.FloatField(db_column='NR_SSB', blank=True, null=True)  # Field name made lowercase.
    nr_rb = models.FloatField(db_column='NR_RB', blank=True, null=True)  # Field name made lowercase.
    p_sinr = models.FloatField(db_column='p_SINR', blank=True, null=True)  # Field name made lowercase.
    s1_sinr = models.FloatField(db_column='s1_SINR', blank=True, null=True)  # Field name made lowercase.
    s2_sinr = models.FloatField(db_column='s2_SINR', blank=True, null=True)  # Field name made lowercase.
    s3_sinr = models.FloatField(db_column='s3_SINR', blank=True, null=True)  # Field name made lowercase.
    s4_sinr = models.FloatField(db_column='s4_SINR', blank=True, null=True)  # Field name made lowercase.
    mobile_ip = models.CharField(max_length=40, blank=True, null=True)
    before_lat = models.FloatField(blank=True, null=True)
    before_lon = models.FloatField(blank=True, null=True)
    savetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_ndm_data_sample_measure'


# class TriggerLog(models.Model):
#     savetime = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'trigger_log'
