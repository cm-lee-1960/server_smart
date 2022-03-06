from xml.dom.pulldom import PROCESSING_INSTRUCTION
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from .geo import KakaoLocalAPI
from message.tele_msg import TelegramBot # 텔레그램 메시지 전송 클래스
from message.xmcs_msg import send_message # 2022.03.04 크로샷 메시지 전송 함수 호출
from management.models import Morphology, MorphologyMap
# import logging

# logger = logging.getLogger(__name__)

###################################################################################################
# 측정 단말기 그룹정보
# 2022.02.25 - 해당지역에 단말이 첫번째 측정을 시작했을 때 측정시작(START) 메시지를 한번 전송한다.
###################################################################################################
class PhoneGroup(models.Model):
    """측정 단말기 그룹정보"""

    measdate = models.CharField(max_length=10)
    userInfo1 = models.CharField(max_length=100)
    ispId = models.CharField(max_length=10)  # 한국:450 / KT:08, SKT:05, LGU+:60
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.measdate}"


###################################################################################################
# 측정 단말기 정보
# * 측정중인 단말을 관리한다.
# * 측정이 종료되면 해당 측정 단말기 정보를 삭제한다. (Active or Inactive 관리도 가능)
# ------------------------------------------------------------------------------------------------
# 2022.02.25 - 측정일자(measdate) 문자열(8자래) 항목 추가
# 2022.02.27 - 주소상세(addressDetail) 항목 추가 
#            - 측정 콜이 행정동 범위를 벗어났는지 확인하기 위해 첫번째 콜 위치를 측정 단말기 정보에 담아 둔다.
# 2022.03.01 - 첫번째 측정 위치(위도,경도)에 대한 주소지를 행정동으로 변환하여 업데이트 하는 함수를 추가함
# 2022.03.03 - 모풀로지 항목 추가
#            - 측정 데이터의 userInfo2에서 측정자가 입력한 모풀로지가 부정확하게 입력된 경우 매핑 테이블로 재지정하기 위함
#            - 측정 데이터의 userInfo2 -> Morphology -> 모풀로지 맵핑 재지정 모듈 추가
# 2022.03.04 - 5G->LTE 전환 콜수 항목 추가 및 누적 업데이트 코드 추가
# 2022.03.05 - 모폴로지를 변경하는 경우 측정 단말기의 관리대상 여부도 자동으로 변경되도록 함 (모풀로지에 따라 관리대상여부 결정)
#            - 기본 모폴로지를 모폴로지와 모폴로지 맵으로 분리함에 따라 관련 소스코드 수정함
#              '행정동', '테마', '인빌딩, '커버리지', 취약지역 등을 소스에 하드코딩 하지 않고, 또 추가 가능하게 하기 위함
#
###################################################################################################
class Phone(models.Model):
    """측정 단말기 정보"""

    ISPID_CHOICES = {
        ("45008", "KT"),
        ("45005", "SKT"),
        ("45006", "LGU+"),
    }
    STATUS_CHOICES = {
        ("POWERON", "PowerOn"),
        ("START", "측정시작"),
        ("MEASURING", "측정중"),
        ("END", "측정종료"),
    }

    phoneGroup = models.ForeignKey(PhoneGroup, on_delete=models.DO_NOTHING)
    measdate = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(verbose_name="측정단말")
    userInfo1 = models.CharField(max_length=100, verbose_name="측정지역")
    userInfo2 = models.CharField(max_length=100, verbose_name="모풀로지(측정데이터)")
    networkId = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="유형"
    )  # 네트워크ID(5G, LTE, 3G, WiFi)
    ispId = models.CharField(
        max_length=10, null=True, blank=True, choices=ISPID_CHOICES, verbose_name="통신사"
    )  # 한국:450 / KT:08, SKT:05, LGU+:60
    avg_downloadBandwidth = models.FloatField(null=True, default=0.0, verbose_name="DL")
    avg_uploadBandwidth = models.FloatField(null=True, default=0.0, verbose_name="UL")
    dl_count = models.IntegerField(null=True, default=0)  # 다운로드 콜수
    ul_count = models.IntegerField(null=True, default=0)  # 업로드 콜수
    nr_count = models.IntegerField(null=True, default=0)  # 5G->NR 전환 콜수   
    status = models.CharField(
        max_length=10, null=True, choices=STATUS_CHOICES, verbose_name="진행단계"
    )
    currentCount = models.IntegerField(null=True, blank=True)
    total_count = models.IntegerField(null=True, default=0, verbose_name="콜 카운트")
    addressDetail = models.CharField(max_length=100, null=True, blank=True)  # 주소상세
    latitude = models.FloatField(null=True, blank=True)  # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도
    last_updated = models.BigIntegerField(
        null=True, blank=True, verbose_name="최종보고시간"
    )  # 최종 위치보고시간
    morphology = models.ForeignKey(Morphology, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="모풀로지")
    manage = models.BooleanField(default=False, verbose_name="관리대상")  # 관리대상 여부
    active = models.BooleanField(default=True, verbose_name="상태")

    class Meta:
        verbose_name = "측정 단말"
        verbose_name_plural = "측정 단말"

    def __str__(self):
        # return f"{self.phone_no}/{self.avg_downloadBandwidth}/{self.avg_uploadBandwidth}/{self.dl_count}/{self.ul_count}"
        return f"{self.phone_no}/{self.id}/{self.total_count}"

    # ---------------------------------------------------------------------------------------------
    # 모풀로지가 변경되는 경우 측정 단말기의 관래대상 여부를 자동으로 변경한다.
    # ---------------------------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        qs = Morphology.objects.filter(morphology=self.morphology)
        if qs.exists():
            self.manage = qs[0].manage
        else:
            self.manage = False
        super(Phone, self).save(*args, **kwargs)

    # ---------------------------------------------------------------------------------------------
    # 측정 단말기의 통계정보를 업데이트 한다.
    # ---------------------------------------------------------------------------------------------
    def update_phone(self, mdata):
        """측정단말의 통계정보를 업데이트 한다."""
        #### 방식 1 ####
        # # DL/UL 평균속도를 업데이트 한다.
        # # 현재 측정 데이터 모두를 가져와서 재계산하는데, 향후 개선필요한 부분임
        # # 2022.02.25 속도 데이터 + NR(5G->LTE)제외 조건
        # dl_sum, ul_sum, dl_count, ul_count = 0, 0, 0, 0
        # for mdata in self.measurecalldata_set.filter(testNetworkType="speed").exclude(
        #     networkId="NR"
        # ):
        #     # logger.info("콜단위 데이터" + str(mdata))
        #     # print("콜단위 데이터" + str(mdata))
        #     if mdata.downloadBandwidth and mdata.downloadBandwidth > 0:
        #         dl_sum += mdata.downloadBandwidth
        #         dl_count += 1
        #     if mdata.uploadBandwidth and mdata.uploadBandwidth > 0:
        #         ul_sum += mdata.uploadBandwidth
        #         ul_count += 1
        # if dl_count:
        #     self.avg_downloadBandwidth = round(dl_sum / dl_count, 3)
        # if ul_count:
        #     self.avg_uploadBandwidth = round(ul_sum / ul_count, 3)

        # # 단말기의 콜 수를 업데이트 한다.
        # self.dl_count = dl_count  # 다운로드 콜건수
        # self.ul_count = ul_count  # 업로드 콜건수
        # self.currentCount = mdata.currentCount # 현재 콜카운트
        # self.total_count = dl_count + ul_count  # 전체 콜건수

        #### 방식 2 ####
        # UL/DL 평균속도 산출시 NR(5G->LTE전환) 데이터는 제외한다.
        # 2022.02.26 - 측정 데이터를 가져와서 재계산 방식에서 수신 받은 한건에 대해서 누적 재계산한다. 
        if mdata.networkId != 'NR':
            # DL 평균속도 계산
            if mdata.downloadBandwidth and mdata.downloadBandwidth > 0:
                self.avg_downloadBandwidth = round(((self.avg_downloadBandwidth * self.dl_count) + mdata.downloadBandwidth) / (self.dl_count + 1), 3)
                self.dl_count += 1
            # UP 평균속도 계산
            if mdata.uploadBandwidth and mdata.uploadBandwidth > 0:
                self.avg_uploadBandwidth = round(((self.avg_uploadBandwidth * self.ul_count) + mdata.uploadBandwidth) / (self.ul_count + 1), 3)
                self.ul_count += 1
        # 5G 측정 단말기 이고, 측정시 NR이면 5G->LTE 전환 콜수를 누적한다.
        elif mdata.phone.networkId == '5G':
            self.nr_count += 1
        
        # 현재 콜카운트와 전체 콜건수를 업데이트 한다.
        self.currentCount = mdata.currentCount # 현재 콜카운트
        self.total_count = self.dl_count + self.ul_count  # 전체 콜건수
        
        # 단말기의 상태를 업데이트 한다.
        # 상태 - 'POWERON', 'START', 'MEASURING', 'END'
        self.status = "START" if self.total_count == 1 else "MEASURING"

        # 최종 위치보고시간을 업데이트 한다.
        self.last_updated = mdata.meastime

        # 단말기의 정보를 데이터베이스에 저장한다.
        self.save()

    # ---------------------------------------------------------------------------------------------
    # 해당 위치(위도,경도)에 대한 주소지를 행정동으로 변환하여 업데이트 한다.
    # 측정 데이터의 userInfo2를 확인하여 모풀로지를 매핑하여 지정한다.
    # ---------------------------------------------------------------------------------------------
    def update_initial_data(self):
        # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
        if self.longitude and self.latitude:
            rest_api_key = settings.KAKAO_REST_API_KEY
            kakao = KakaoLocalAPI(rest_api_key)
            input_coord = "WGS84" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
            output_coord = "TM" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

            result = kakao.geo_coord2regioncode(self.longitude, self.latitude, input_coord, output_coord)

            region_3depth_name = result['documents'][1]['region_3depth_name']

            self.addressDetail = region_3depth_name

        # 측정 데이터의 userInfo2를 확인하여 모풀로지를 매핑하여 지정한다.
        morphology = None # 모풀로지
        manage = False # 관리대상 여부

        if self.userInfo2:
            # 모풀로지 DB 테이블에서 정보를 가져와서 해당 측정 데이터에 대한 모풀로지를 재지정한다. 
            for mp in MorphologyMap.objects.all():
                if mp.wordsCond == '시작단어':
                    if self.userInfo2.startswith(mp.words):
                        morphology = mp.morphology
                        manage = mp.manage
                        break
                elif mp.wordsCond == '포함단어':
                    if self.userInfo2.find(mp.words) >= 0:
                        morphology = mp.morphology
                        manage = mp.manage
                        break

        self.morphology = morphology
        self.manage = manage

        # 측정 단말기 정보를 저장한다.
        self.save()

###################################################################################################
# 실시간 측정 데이터(콜 단위)
###################################################################################################
class MeasureCallData(models.Model):
    """실시간 측정 데이터(콜 단위)"""

    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(
        null=True, blank=True, verbose_name="전화번호"
    )  # 전화번호
    meastime = models.BigIntegerField(
        null=True, blank=True, verbose_name="측정시간"
    )  # 측정시간
    networkId = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="유형"
    )  # 네트워크ID(5G, LTE, 3G, WiFi)
    groupId = models.CharField(max_length=100, null=True, blank=True)  # 그룹ID
    currentTime = models.CharField(max_length=100, null=True, blank=True)  # 현재시간
    timeline = models.CharField(max_length=100, null=True, blank=True)  # 타입라인
    cellId = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="셀ID"
    )  # 셀ID
    currentCount = models.IntegerField(
        null=True, blank=True, verbose_name="현재 콜카운트"
    )  # 현재 콜카운트
    ispId = models.CharField(
        max_length=10, null=True, blank=True
    )  # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(
        max_length=100, null=True, blank=True
    )  # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True)  # 입력된 주소정보
    userInfo2 = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="모풀로지"
    )  # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    siDo = models.CharField(max_length=100, null=True, blank=True)  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True)  # 구,군
    addressDetail = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="주소상세"
    )  # 주소상세
    udpJitter = models.FloatField(null=True, blank=True)  # 지연시간
    downloadBandwidth = models.FloatField(
        null=True, blank=True, verbose_name="DL"
    )  # DL속도
    uploadBandwidth = models.FloatField(
        null=True, blank=True, verbose_name="UL"
    )  # UP속도
    sinr = models.FloatField(null=True, blank=True)  # SINR
    isWifi = models.CharField(max_length=100, null=True, blank=True)  # 와이파이 사용여부
    latitude = models.FloatField(null=True, blank=True)  # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도
    bandType = models.CharField(
        max_length=16, null=True, blank=True
    )  # CA(ex.1CL2-> 1CA(20M), 3CL4->3CA(40M))
    p_dl_earfcn = models.IntegerField(null=True, blank=True)  # P 주파수
    p_pci = models.IntegerField(null=True, blank=True)  # P PCI
    p_rsrp = models.FloatField(null=True, blank=True)  # P RSRP
    p_SINR = models.FloatField(null=True, blank=True)   # P SINR
    NR_EARFCN = models.IntegerField(null=True, blank=True)  # 5G 주파수
    NR_PCI = models.IntegerField(null=True, blank=True)  # 5G CI
    NR_RSRP = models.FloatField(null=True, blank=True)  # 5G PCI
    NR_SINR = models.FloatField(null=True, blank=True)  # 5G SINR
    # before_lat = models.FloatField(null=True, blank=True) # 이전 위도 - 의미없음(위도와 동일)
    # before_lon = models.FloatField(null=True, blank=True) # 이전 경도 - 의미없음(경도와 동일)

    class Meta:
        verbose_name = "측정 데이터(콜단위)"
        verbose_name_plural = "측정 데이터(콜단위)"

    def __str__(self):
        return f"{self.phone_no}/{self.networkId}/{self.meastime}/{self.currentCount}/{self.downloadBandwidth}/{self.uploadBandwidth}/"


###################################################################################################
# 실시간 측정 데이터(초 단위)
###################################################################################################
class MeasureSecondData(models.Model):
    """실시간 측정 데이터(초 단위)"""

    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(null=True, blank=True)  # 전화번호
    meastime = models.BigIntegerField(null=True, blank=True)  # 측정시간
    neworkid = models.CharField(
        max_length=100, null=True, blank=True
    )  # 네트워크ID(5G, LTE, 3G, WiFi)
    groupId = models.CharField(max_length=100, null=True, blank=True)  # 그룹ID
    currentTime = models.CharField(max_length=100, null=True, blank=True)  # 현재시간
    timeline = models.CharField(max_length=100, null=True, blank=True)  # 타입라인
    cellId = models.CharField(max_length=100, null=True, blank=True)  # 셀ID
    currentCount = models.IntegerField(null=True, blank=True)  # 현재 콜카운트
    ispId = models.CharField(
        max_length=10, null=True, blank=True
    )  # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(
        max_length=100, null=True, blank=True
    )  # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True)  # 입력된 주소정보
    userInfo2 = models.CharField(
        max_length=100, null=True, blank=True
    )  # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    siDo = models.CharField(max_length=100, null=True, blank=True)  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True)  # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True)  # 주소상세
    udpJitter = models.FloatField(null=True, blank=True)  # 지연시간
    downloadBandwidth = models.FloatField(null=True, blank=True)  # DL속도
    uploadBandwidth = models.FloatField(null=True, blank=True)  # UP속도
    sinr = models.FloatField(null=True, blank=True)  # SINR
    isWifi = models.CharField(max_length=100, null=True, blank=True)  # 와이파이 사용여부
    latitude = models.FloatField(null=True, blank=True)  # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도
    bandType = models.CharField(
        max_length=16, null=True, blank=True
    )  # CA(ex.1CL2-> 1CA(20M), 3CL4->3CA(40M))
    p_dl_earfcn = models.IntegerField(null=True, blank=True)  # P 주파수
    p_pci = models.IntegerField(null=True, blank=True)  # P PCI
    p_rsrp = models.FloatField(null=True, blank=True)  # P RSRP
    NR_EARFCN = models.IntegerField(null=True, blank=True)  # 5G 주파수
    NR_PCI = models.IntegerField(null=True, blank=True)  # 5G CI
    NR_RSRP = models.FloatField(null=True, blank=True)  # 5G PCI
    NR_SINR = models.FloatField(null=True, blank=True)  # 5G SINR
    # before_lat = models.FloatField(null=True, blank=True) # 이전 위도 - 의미없음(위도와 동일)
    # before_lon = models.FloatField(null=True, blank=True) # 이전 경도 - 의미없음(경도와 동일)


    def __str__(self):
        return f"{self.phone_no}/{self.neworkid}/{self.meastime}/{self.currentCount}"


###################################################################################################
# 전송 메시지 클래스
# 2022.02.25 - 의존성으로 마이그레이트 및 롤백 시 오류가 자주 발생하여 모니터 앱으로 옮겨 왔음
# 2022.02.27 - 메시지 유형을 메시지(SMS)와 이벤트(EVENT)로 구분할 수 있도록 항목 추가
###################################################################################################
class Message(models.Model):
    '''전송 메시지'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    measdate = models.CharField(max_length=10)
    sendType = models.CharField(max_length=10) # 전송유형(TELE: 텔레그램, XMCS: 크로샷)
    #### 디버깅을 위해 임시로 만든 항목(향후 삭제예정) ###########
    userInfo1 = models.CharField(max_length=100, null=True, blank=True) 
    currentCount = models.IntegerField(null=True, blank=True)
    phone_no = models.BigIntegerField(null=True, blank=True)
    downloadBandwidth = models.FloatField(null=True, blank=True)  # DL속도
    uploadBandwidth = models.FloatField(null=True, blank=True)  # UP속도
    ###################################################
    messageType = models.CharField(max_length=10) # 메시지유형(SMS: 메시지, EVENT: 이벤트)
    message = models.TextField(default=False)
    channelId = models.CharField(max_length=25)
    sended = models.BooleanField(default=True)


# -------------------------------------------------------------------------------------------------
# 생성된 메시지 타입에 따라서 크로샷 또는 텔레그램으로 메시지를 전송한다.
#--------------------------------------------------------------------------------------------------
def send_message(sender, **kwargs):
    bot = TelegramBot()  ## 텔레그램 인스턴스 선언(3.3)
    # 텔레그램으로 메시지를 전송한다.
    if kwargs['instance'].sendType == 'TELE':
        bot.send_message_bot(kwargs['instance'].channelId, kwargs['instance'].message)
    # 크로샷으로 메시지를 전송한다.
    elif kwargs['instance'].sendType == 'XMCS':
        #######################################################################################################
        # (3.4) 크로샷 메시지 전송  --  node.js 파일 호출하여 전송
        # 현재 변수 전달(메시지/수신번호) 구현되어 있지 않아 /message/sms_broadcast.js에 설정된 내용/번호로만 전송
        # npm install request 명령어로 모듈 설치 후 사용 가능 
        #######################################################################################################
        send_message()

# -------------------------------------------------------------------------------------------------
# 전송 메시지가 저장된 후 메시지 전송 모듈을 호출한다(SIGNAL). 
#--------------------------------------------------------------------------------------------------
post_save.connect(send_message, sender=Message)




