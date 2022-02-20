from django.db import models
from django.db.models.signals import post_save
from telemsg.tele_msg_old import send_message_bot
import logging
logger = logging.getLogger(__name__)

###################################################################################################
# 측정 단말기 그룹정보
###################################################################################################
class PhoneGroup(models.Model):
    '''측정 단말기 그룹정보'''
    groupId = models.CharField(max_length=100)
    userInfo1 = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    # 두개의 측정 단말기의 콜 가운트가 동일하고, 메시지 전송기준 콜 수 있지 확인한다.
    def current_count_check(self):
        '''DL/UL 측정단말의 현재 콜카운트와 보고기준 콜카운트를 확인한다.'''
        currentCountList = []
        for p in self.phone_set.all():
            currentCountList.append(p.total_count)
        result = len(currentCountList) > 1 and \
            all(element == currentCountList[0] for element in currentCountList) and \
            currentCountList[0] in [1, 3, 10, 27, 37, 57]
        print("current_count_check()함수 실행:", currentCountList)
        return result

###################################################################################################
# 측정 단말기 정보
# * 측정중인 단말을 관리한다. 
# * 측정이 종료되면 해당 측정 단말기 정보를 삭제한다. (Active or Inactive 관리도 가능)
###################################################################################################
class Phone(models.Model):
    '''측정 단말기 정보'''
    phoneGroup = models.ForeignKey(PhoneGroup, on_delete=models.DO_NOTHING)
    phone_type = models.CharField(max_length=5, verbose_name='구분')
    phone_no = models.BigIntegerField(verbose_name='측정단말')
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name='유형') # 네트워크ID(5G, LTE, 3G, WiFi)    
    avg_downloadBandwidth = models.FloatField(null=True, default=0.0, verbose_name='DL')
    avg_uploadBandwidth =models.FloatField(null=True, default=0.0, verbose_name='UL')
    status = models.CharField(max_length=10, null=True, verbose_name='진행단계')
    total_count = models.IntegerField(null=True, default=0, verbose_name='콜 카운트')
    last_updated = models.BigIntegerField(null=True, blank=True, verbose_name='최종보고시간') # 최종 위치보고시간
    active = models.BooleanField(default=True, verbose_name='상태')

    class Meta:
        verbose_name = ('측정단말')
        verbose_name_plural = ('측정단말')

    def __str__(self):
        return f"{self.phone_type}/{self.phone_no}/{self.avg_downloadBandwidth}/{self.avg_uploadBandwidth}/{self.total_count}"
    
    # 측정 단말기의 통계정보를 업데이트 한다.
    def update_info(self, mdata):
        '''측정단말의 통계정보를 업데이트 한다.'''
        # DL/UL 평균속도를 업데이트 한다.
        # 현재 측정 데이터 모두를 가져와서 재계산하는데, 향후 개선필요한 부분임
        dl_sum, up_sum, total_count = 0, 0, 0
        for mdata in self.measurecalldata_set.all():
            logger.info("콜단위 데이터" + str(mdata))
            # print("콜단위 데이터" + str(mdata))
            dl_sum += mdata.downloadBandwidth if mdata.downloadBandwidth else 0
            up_sum += mdata.uploadBandwidth if mdata.uploadBandwidth else 0
            total_count += 1
        if self.phone_type == 'DL':
            self.avg_downloadBandwidth = dl_sum / total_count
        if self.phone_type == 'UL':
            self.avg_uploadBandwidth = up_sum / total_count

        # 단말기의 콜 수를 업데이트 한다. 
        self.total_count = total_count

        # 단말기의 상태를 업데이트 한다. 
        # 상태 - 'POWERON', 'START', 'MEASURING', 'END'
        self.status = 'START' if self.total_count == 1 else 'MEASURING'

        # 최종 위치보고시간을 업데이트 한다. 
        self.last_updated = mdata.meastime

        # 단말기의 정보를 데이터베이스에 저장한다. 
        self.save()

    # 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
    def make_message(self):
        '''측정단말의 상태에 따라서 메시지를 작성한다.'''
        print("make_message()함수 시작")
        # settings.PHONE_STATUS 변수로 선언해도 될지 고민 예정임
        # 2022.01.17 Power On/Off는 데이터 추가해 달라고 하겠음
        channelId = '-736183270' 
        status = ['POWERON', 'START', 'MEASURING', 'END']
        # 측정 진행 메시지는 DL/UP 측정 단말기의 현재 콜 카운트가 같고, 3, 10, 27, 37, 57 콜 단위로 보고함
        if self.status in status and self.phoneGroup.current_count_check():
            # 측정 단말기의 DL/UP 평균값들을 가져온다.
            for phone in self.phoneGroup.phone_set.all():
                if phone.phone_type == 'DL':
                    avg_downloadBandwidth = phone.avg_downloadBandwidth
                elif phone.phone_type == 'UL':
                    avg_uploadBandwidth = phone.avg_uploadBandwidth

            # 메시지를 작성한다. 
            messages = { 
                'POWERON': "OO지역 단말이 켜졌습니다.",
                'START': f"측정을 시작합니다.\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
                'MEASURING': f"{self.total_count}번째 측정 데이터입니다.\n{avg_downloadBandwidth:.1f} / {avg_downloadBandwidth:.1f}",
                'END': f"측정이 종료되었습니다(총{self.total_count}건).\n{avg_downloadBandwidth:.1f} / {avg_downloadBandwidth:.1f}",
                }

            # 전송 메시지를 생성한다. 
            Message.objects.create(
                phone = self,
                send_type = 'TELE',
                currentCount = self.total_count,
                message = messages[self.status],
                channelId = channelId
            )


###################################################################################################
# 실시간 측정 데이터(콜 단위)
###################################################################################################     
class MeasureCallData(models.Model):
    '''실시간 측정 데이터(콜 단위)'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(null=True, blank=True) # 전화번호
    meastime = models.BigIntegerField(null=True, blank=True) # 측정시간
    networkId = models.CharField(max_length=100, null=True, blank=True) # 네트워크ID(5G, LTE, 3G, WiFi)
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
# 전송 메시지
###################################################################################################
class Message(models.Model):
    '''전송 메시지'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    send_type = models.CharField(max_length=10)
    currentCount = models.IntegerField()
    message = models.TextField()
    channelId = models.CharField(max_length=25)
    # 전송일시 항목추가

# -------------------------------------------------------------------------------------------------
# 전송 메시지가 저장된 후 텔래그램 전송 모듈을 호출한다. 
#--------------------------------------------------------------------------------------------------
post_save.connect(send_message_bot, sender=Message)


