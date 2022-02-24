from django.db import models
import logging
# logger = logging.getLogger(__name__)

###################################################################################################
# 측정 단말기 그룹정보
###################################################################################################
class PhoneGroup(models.Model):
    '''측정 단말기 그룹정보'''
    measdate = models.CharField(max_length=10)
    userInfo1 = models.CharField(max_length=100)
    ispId = models.CharField(max_length=10) # 한국:450 / KT:08, SKT:05, LGU+:60
    active = models.BooleanField(default=True)

    # 두개의 측정 단말기의 콜 가운트가 동일하고, 메시지 전송기준 콜 수 있지 확인한다.
    def current_count_check(self, phone):
        '''DL/UL 측정단말의 현재 콜카운트와 보고기준 콜카운트를 확인한다.'''
        result = False
        if phone.total_count in [1, 3, 10, 27, 37, 57]:
            # 단밀기 그룹으로 묶여 았는 상대편 측정 단말기를 조회한다.
            qs = phone.phoneGroup.phone_set.exclude(phone_no=phone.phone_no)
            if qs.exists():
                p = qs[0]
                # 상대편 측정 단말기의 현재 콜 카운트가 측정 단말 보다 같거나 커야 한다. 
                if p.total_count >= phone.total_count:
                    result = True
        # 2.21 로직이 복잡하고, 오류가 있어서 위의 코드로 단순하게 개선함
        # currentCountList = []
        # for p in self.phone_set.all():
        #     currentCountList.append(p.total_count)
        # # 현재 콜카운트가 작은 값부터 나열되도록 정렬한다. 
        # currentCountList.sort()
        # result = len(currentCountList) > 1 and \
        #     all(element >= currentCountList[0] for element in currentCountList) and \
        #     currentCountList[0] in [1, 3, 10, 27, 37, 57]
        # print("current_count_check()함수 실행:", currentCountList, result)
        return result

###################################################################################################
# 측정 단말기 정보
# * 측정중인 단말을 관리한다. 
# * 측정이 종료되면 해당 측정 단말기 정보를 삭제한다. (Active or Inactive 관리도 가능)
###################################################################################################
class Phone(models.Model):
    '''측정 단말기 정보'''
    phoneGroup = models.ForeignKey(PhoneGroup, on_delete=models.DO_NOTHING)
    phone_no = models.BigIntegerField(verbose_name='측정단말')
    userInfo1 = models.CharField(max_length=100)
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name='유형') # 네트워크ID(5G, LTE, 3G, WiFi)    
    ispId = models.CharField(max_length=10, null=True, blank=True) # 한국:450 / KT:08, SKT:05, LGU+:60
    avg_downloadBandwidth = models.FloatField(null=True, default=0.0, verbose_name='DL')
    avg_uploadBandwidth =models.FloatField(null=True, default=0.0, verbose_name='UL')
    dl_count = models.IntegerField(null=True, default=0) # 다운로드 콜수
    ul_count = models.IntegerField(null=True, default=0) # 업로드 콜수
    status = models.CharField(max_length=10, null=True, verbose_name='진행단계')
    total_count = models.IntegerField(null=True, default=0, verbose_name='콜 카운트')
    last_updated = models.BigIntegerField(null=True, blank=True, verbose_name='최종보고시간') # 최종 위치보고시간
    manage = models.BooleanField(default=False) # 관리대상 여부
    active = models.BooleanField(default=True, verbose_name='상태')

    class Meta:
        verbose_name = ('측정 단말')
        verbose_name_plural = ('측정 단말')

    def __str__(self):
        return f"{self.phone_no}/{self.avg_downloadBandwidth}/{self.avg_uploadBandwidth}/{self.dl_count}/{self.ul_count}"
    
    # 측정 단말기의 통계정보를 업데이트 한다.
    def update_info(self, mdata):
        '''측정단말의 통계정보를 업데이트 한다.'''
        # DL/UL 평균속도를 업데이트 한다.
        # 현재 측정 데이터 모두를 가져와서 재계산하는데, 향후 개선필요한 부분임
        dl_sum, ul_sum, dl_count, ul_count = 0, 0, 0, 0
        for mdata in self.measurecalldata_set.all():
            # logger.info("콜단위 데이터" + str(mdata))
            # print("콜단위 데이터" + str(mdata))
            if mdata.downloadBandwidth and mdata.downloadBandwidth > 0:
                dl_sum += mdata.downloadBandwidth
                dl_count += 1
            if mdata.uploadBandwidth and mdata.uploadBandwidth > 0:
                ul_sum += mdata.uploadBandwidth
                ul_count += 1
        if dl_count:
            self.avg_downloadBandwidth = round(dl_sum / dl_count, 3)
        if ul_count:
            self.avg_uploadBandwidth = round(ul_sum / ul_count, 3)

        # 단말기의 콜 수를 업데이트 한다. 
        self.dl_count = dl_count # 다운로드 콜건수
        self.ul_count = ul_count # 업로드 콜건수
        self.total_count = dl_count + ul_count # 전체 콜건수

        # 단말기의 상태를 업데이트 한다. 
        # 상태 - 'POWERON', 'START', 'MEASURING', 'END'
        self.status = 'START' if self.total_count == 1 else 'MEASURING'

        # 최종 위치보고시간을 업데이트 한다. 
        self.last_updated = mdata.meastime

        # 단말기의 정보를 데이터베이스에 저장한다. 
        self.save()



###################################################################################################
# 실시간 측정 데이터(콜 단위)
###################################################################################################     
class MeasureCallData(models.Model):
    '''실시간 측정 데이터(콜 단위)'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(null=True, blank=True, verbose_name='전화번호') # 전화번호
    meastime = models.BigIntegerField(null=True, blank=True, verbose_name='측정시간') # 측정시간
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name='유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    groupId = models.CharField(max_length=100, null=True, blank=True) # 그룹ID
    currentTime = models.CharField(max_length=100, null=True, blank=True) # 현재시간
    timeline = models.CharField(max_length=100, null=True, blank=True) # 타입라인
    cellId = models.CharField(max_length=100, null=True, blank=True, verbose_name='셀ID') # 셀ID
    currentCount = models.IntegerField(null=True, blank=True, verbose_name='현재 콜카운트') # 현재 콜카운트
    ispId = models.CharField(max_length=10, null=True, blank=True) # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(max_length=100, null=True,blank=True) # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True) # 입력된 주소정보
    userInfo2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='모폴러지') # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    siDo = models.CharField(max_length=100, null=True, blank=True) # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True) # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True, verbose_name='주소상세') # 주소상세
    udpJitter = models.FloatField(null=True, blank=True) # 지연시간
    downloadBandwidth = models.FloatField(null=True, blank=True, verbose_name='DL') # DL속도
    uploadBandwidth = models.FloatField(null=True, blank=True, verbose_name='UL') # UP속도
    sinr = models.FloatField(null=True, blank=True) # SINR
    isWifi = models.CharField(max_length=100, null=True, blank=True) # 와이파이 사용여부
    latitude = models.FloatField(null=True, blank=True) # 위도
    longitude = models.FloatField(null=True, blank=True) # 경도
    bandType = models.CharField(max_length=16, null=True, blank=True) # CA(ex.1CL2-> 1CA(20M), 3CL4->3CA(40M))
    p_dl_earfcn = models.IntegerField(null=True, blank=True) # P 주파수 
    p_pci = models.IntegerField(null=True, blank=True) # P PCI
    p_rsrp = models.FloatField(null=True, blank=True) # P RSRP
    NR_EARFCN = models.IntegerField(null=True, blank=True) # 5G 주파수
    NR_PCI = models.IntegerField(null=True, blank=True) # 5G CI
    NR_RSRP = models.FloatField(null=True, blank=True) # 5G PCI
    NR_SINR = models.FloatField(null=True, blank=True) # 5G SINR
    # before_lat = models.FloatField(null=True, blank=True) # 이전 위도 - 의미없음(위도와 동일)
    # before_lon = models.FloatField(null=True, blank=True) # 이전 경도 - 의미없음(경도와 동일)
    
    class Meta:
        verbose_name = ('측정 데이터(콜단위)')
        verbose_name_plural = ('측정 데이터(콜단위)')

    def __str__(self):
         return f"{self.phone_no}/{self.networkId}/{self.meastime}/{self.currentCount}/{self.downloadBandwidth}/{self.uploadBandwidth}/"


###################################################################################################
# 실시간 측정 데이터(초 단위)
###################################################################################################
class MeasureSecondData(models.Model):
    '''실시간 측정 데이터(초 단위)'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(null=True, blank=True) # 전화번호
    meastime = models.BigIntegerField(null=True, blank=True) # 측정시간
    neworkid = models.CharField(max_length=100, null=True, blank=True) # 네트워크ID(5G, LTE, 3G, WiFi)
    groupId = models.CharField(max_length=100, null=True, blank=True) # 그룹ID
    currentTime = models.CharField(max_length=100, null=True, blank=True) # 현재시간
    timeline = models.CharField(max_length=100, null=True, blank=True) # 타입라인
    cellId = models.CharField(max_length=100, null=True, blank=True) # 셀ID
    currentCount = models.IntegerField(null=True, blank=True) # 현재 콜카운트
    ispId = models.CharField(max_length=10, null=True, blank=True) # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(max_length=100, null=True,blank=True) # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True) # 입력된 주소정보
    userInfo2 = models.CharField(max_length=100, null=True, blank=True) # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    siDo = models.CharField(max_length=100, null=True, blank=True) # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True) # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True) # 주소상세
    udpJitter = models.FloatField(null=True, blank=True) # 지연시간
    downloadBandwidth = models.FloatField(null=True, blank=True) # DL속도
    uploadBandwidth = models.FloatField(null=True, blank=True) # UP속도
    sinr = models.FloatField(null=True, blank=True) # SINR
    isWifi = models.CharField(max_length=100, null=True, blank=True) # 와이파이 사용여부
    latitude = models.FloatField(null=True, blank=True) # 위도
    longitude = models.FloatField(null=True, blank=True) # 경도
    bandType = models.CharField(max_length=16, null=True, blank=True) # CA(ex.1CL2-> 1CA(20M), 3CL4->3CA(40M))
    p_dl_earfcn = models.IntegerField(null=True, blank=True) # P 주파수 
    p_pci = models.IntegerField(null=True, blank=True) # P PCI
    p_rsrp = models.FloatField(null=True, blank=True) # P RSRP
    NR_EARFCN = models.IntegerField(null=True, blank=True) # 5G 주파수
    NR_PCI = models.IntegerField(null=True, blank=True) # 5G CI
    NR_RSRP = models.FloatField(null=True, blank=True) # 5G PCI
    NR_SINR = models.FloatField(null=True, blank=True) # 5G SINR
    # before_lat = models.FloatField(null=True, blank=True) # 이전 위도 - 의미없음(위도와 동일)
    # before_lon = models.FloatField(null=True, blank=True) # 이전 경도 - 의미없음(경도와 동일)


    def __str__(self):
        return f"{self.phone_no}/{self.neworkid}/{self.meastime}/{self.currentCount}"

###################################################################################################
# 금일측정조 데이터
###################################################################################################
class MeasureingTeam(models.Model):
    meastime = models.DateField(verbose_name='측정일자')
    message = models.TextField(verbose_name='메시지 내용')
