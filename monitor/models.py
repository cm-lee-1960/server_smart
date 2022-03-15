
from operator import itemgetter
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from .geo import KakaoLocalAPI
from message.tele_msg import TelegramBot # 텔레그램 메시지 전송 클래스
from message.xmcs_msg import send_sms # 2022.03.04 크로샷 메시지 전송 함수 호출
from management.models import Morphology, MorphologyMap
# import logging

# logger = logging.getLogger(__name__)

###################################################################################################
# 측정 단말기 그룹정보
# 2022.02.25 - 해당지역에 단말이 첫번째 측정을 시작했을 때 측정시작(START) 메시지를 한번 전송한다.
# 2022.03.06 - 측정 데이터에 통신사(ispId)가 널(NULL)인 값이 들어와서 동일하게 모델의 해당 항목에 널을 허용함
# 2022.03.11 - 단말그룹에 묶여 있는 측정 단말기들이 당일 이전에 측정이 있었는지 확인하고 있었다면 그때 단말그룹 측정조 값을
#              가져와서 업데이트 하는 모듈 추가
###################################################################################################
class PhoneGroup(models.Model):
    """측정 단말기 그룹정보"""

    MEASURINGTEAM_CHOICES = {
        ("1조", "1조"),
        ("2조", "2조"),
        ("3조", "3조"),
        ("4조", "4조"),
        ("5조", "5조"),
    }
    ISPID_CHOICES = {
        ("45008", "KT"),
        ("45005", "SKT"),
        ("45006", "LGU+"),
    }

    measdate = models.CharField(max_length=10, verbose_name="측정일자")
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    userInfo2 = models.CharField(max_length=100, verbose_name="측정자 입력값2")
    morphology = models.ForeignKey(Morphology, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="모풀로지")
    measuringTeam = models.CharField(max_length=20, null=True, blank=True, \
        choices=sorted(MEASURINGTEAM_CHOICES,key=itemgetter(0)), verbose_name='측정조')
    ispId = models.CharField(max_length=10, null=True, blank=True, choices=ISPID_CHOICES, verbose_name="통신사")  # 한국:450 / KT:08, SKT:05, LGU+:60
    active = models.BooleanField(default=True, verbose_name="상태")

    class Meta:
        verbose_name = "단말 그룹"
        verbose_name_plural = "단말 그룹"

    def __str__(self):
        return f"{self.measdate}"

    # 해당 단말그룹의 측정조를 업데이트 한다.
    def update_initial_data(self):
        phone_list = [ p.phone_no for p in self.phone_set.all()]
        qs = Phone.objects.filter(measdate=self.measdate, phone_no__in=phone_list).exclude(phoneGroup=self)
        if qs.exists():
            measuringTeam = None
            for p in qs:
                print(p, p.phoneGroup.id, p.phoneGroup.measuringTeam)
                if p.phoneGroup.measuringTeam and p.phoneGroup.measuringTeam != None:
                    measuringTeam = p.phoneGroup.measuringTeam
                    break
            self.measuringTeam = measuringTeam
            self.save()

# -------------------------------------------------------------------------------------------------
# 측정자 입력값2(userInfo2)로 모폴로지를 확인한다. 
# 2022.03.15 - 측정자 입력값(userInfo2)가 입력오류가 자주 발생하므로 모폴로지를 찾지 못하는 경우 "행정동"으로 초기화 함
#--------------------------------------------------------------------------------------------------
def get_morphology(userInfo2):
    # 측정자 입력값2(userInfo2)에 따라 모폴로지를 결정한다.
    morphology = Morphology.objects.filter(morphology='행정동')[0] # 초기값 설정
    if userInfo2 and userInfo2 != None:
        # 모풀로지 DB 테이블에서 정보를 가져와서 해당 측정 데이터에 대한 모풀로지를 반환한다.
        for mp in MorphologyMap.objects.all():
            if mp.wordsCond == '시작단어':
                if userInfo2.startswith(mp.words):
                    morphology = mp.morphology
                    break
            elif mp.wordsCond == '포함단어':
                if userInfo2.find(mp.words) >= 0:
                    morphology = mp.morphology
                    break
    return morphology


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
# 2022.03.06 - 행정동 찾기 및 모폴로지 변환 모듈에 대한 예외처리 루팅 추가
# 2022.03.11 - 측정시작 메시지를 2개로 분리함에 따라서 측정시작 상태코드 분리
#              1) START_F: 전체대상 측정시작
#              2) START_M: 해당지역 측정시작
# 2022.03.12 - 측정시작 위치에 대한 행정동 주소(시/도, 구/군, 읍/동/면)을 측정 단말기 정보에 가져감
#              (5G->LTE로 전환시 위도,경도는 있지만 주소가 널(Null)인 경우가 많음)
# 2022.03.16 - 중복측정 이벤트 발생여부를 확인하기 위해서 측정 단말기에 현재 측정유형 항목을 가져감(DL, UL)
#              그룹으로 묶여 있는 단말기의 측정유형이 2개가 모두 동일할 때 이벤트 발생(DL/DL, UL/UL)
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
        ("START_F", "측정시작"),
        ("START_M", "측정시작"),    
        ("MEASURING", "측정중"),
        ("END", "측정종료"),
    }
    MEASTYPE_CHOICES = {
        ("DL", "DL"),
        ("UL", "UL")
    }

    phoneGroup = models.ForeignKey(PhoneGroup, on_delete=models.DO_NOTHING)
    measdate = models.CharField(max_length=10, verbose_name="측정일자")
    starttime = models.CharField(max_length=10, verbose_name="측정시작시간")  # 측정시작시간
    phone_no = models.BigIntegerField(verbose_name="측정단말")
    meastype = models.CharField(max_length=10, null=True, blank=True, choices=MEASTYPE_CHOICES, verbose_name="측정유형")
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    userInfo2 = models.CharField(max_length=100, verbose_name="측정자 입력값2")
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
    siDo = models.CharField(max_length=100, null=True, blank=True)  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True)  # 구,군
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
        return f"{self.userInfo1}/{self.userInfo2}/{self.phone_no}/{self.total_count}"

    # 전화번호 뒤에서 4자리를 반환한다.
    def get_phone_no_sht(self):
        return str(self.phone_no)[-4:]

    # ---------------------------------------------------------------------------------------------
    # 모델을 DB에 저장하는 함수(오버라이딩)
    # - 모델을 DB에 저장하기 전에 처리해야 하는 것들을 작선하다.
    # * 모풀로지가 변경되는 경우 측정 단말기의 관래대상 여부를 자동으로 변경한다.
    # ---------------------------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        qs = Morphology.objects.filter(morphology=self.morphology)
        if qs.exists():
            self.manage = qs[0].manage
        else:
            self.manage = False
        super(Phone, self).save(*args, **kwargs)

    # ---------------------------------------------------------------------------------------------
    # 측정 단말기의 통계정보를 업데이트 하는 합수
    # - DL/UL 평균속도, 콜수, 진행상태, 최종 위치보고시간 등
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
        if mdata.networkId == 'NR':
            self.nr_count += 1
        else:
            # DL 평균속도 계산
            if mdata.downloadBandwidth and mdata.downloadBandwidth > 0:
                self.avg_downloadBandwidth = round(((self.avg_downloadBandwidth * self.dl_count) + mdata.downloadBandwidth) / (self.dl_count + 1), 3)
                self.meastype = 'DL'
                self.dl_count += 1
            # UP 평균속도 계산
            if mdata.uploadBandwidth and mdata.uploadBandwidth > 0:
                self.avg_uploadBandwidth = round(((self.avg_uploadBandwidth * self.ul_count) + mdata.uploadBandwidth) / (self.ul_count + 1), 3)
                self.meastype = 'UL'
                self.ul_count += 1

        # 현재 콜카운트와 전체 콜건수를 업데이트 한다.
        self.currentCount = mdata.currentCount # 현재 콜카운트
        self.total_count = self.dl_count + self.ul_count + self.nr_count # 전체 콜건수
        
        # 단말기의 상태를 업데이트 한다.
        # 상태 - 'POWERON', 'START_F', 'START_M', 'MEASURING', 'END'
        # 2022.03.11 - 측정시작 메시지 분리 반영 (전체대상 측정시작: START_F, 해당지역 측정시작: START_M)
        if self.total_count <= 1:
            self.status = "START_M" 
        else:
            self.status = "MEASURING"

        # 최종 위치보고시간을 업데이트 한다.
        self.last_updated = mdata.meastime

        # 단말기의 정보를 데이터베이스에 저장한다.
        self.save()

    # ---------------------------------------------------------------------------------------------
    # 측정 단말기가 최조 생성될 때 한번만 처리하기 위한 함수
    # - 해당 위치(위도,경도)에 대한 주소지를 행정동으로 변환하여 업데이트 한다.
    # - 측정 데이터의 userInfo2를 확인하여 모풀로지를 매핑하여 지정한다.
    # ---------------------------------------------------------------------------------------------
    def update_initial_data(self):
        '''측정 단말기가 생성될 때 최초 한번만 수행한다.'''
        try: 
            # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
            if self.longitude and self.latitude:
                rest_api_key = settings.KAKAO_REST_API_KEY
                kakao = KakaoLocalAPI(rest_api_key)
                input_coord = "WGS84" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
                output_coord = "TM" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

                result = kakao.geo_coord2regioncode(self.longitude, self.latitude, input_coord, output_coord)
                # [ 리턴값 형식 ]
                # print("out_measuring_range():", result)
                # {'meta': {'total_count': 2},
                # 'documents': [{'region_type': 'B',
                # 'code': '4824012400',
                # 'address_name': '경상남도 사천시 노룡동',
                # 'region_1depth_name': '경상남도',
                # 'region_2depth_name': '사천시',
                # 'region_3depth_name': '노룡동', <-- 주소지 동
                # 'region_4depth_name': '',
                # 'x': 296184.5342265043,
                # 'y': 165683.29710986698},
                # {'region_type': 'H',
                # 'code': '4824059500',
                # 'address_name': '경상남도 사천시 남양동',
                # 'region_1depth_name': '경상남도',
                # 'region_2depth_name': '사천시',
                # 'region_3depth_name': '남양동', <-- 행정구역
                # 'region_4depth_name': '',
                # 'x': 297008.1130364056,
                # 'y': 164008.47612447804}]}

                region_1depth_name = result['documents'][1]['region_1depth_name'] # 시/도
                region_2depth_name = result['documents'][1]['region_2depth_name'] # 구/군
                region_3depth_name = result['documents'][1]['region_3depth_name'] # 행정동(읍/동/면)

                self.siDo = region_1depth_name # 시/도
                self.guGun = region_2depth_name # 구/군
                self.addressDetail = region_3depth_name # 행정동(읍/동/면)

            # 측정자 입력값2(userInfo2)에 따라 모폴로지와 관리대상여부를 결정한다.
            # 2022.03.14 - 다른 모듈에서도 사용할 수 있도록 클래스 밖으로 별도 함수로 선언함
            #
            # morphology = None # 모풀로지
            # manage = False # 관리대상 여부
            # if self.userInfo2:
            #     # 모풀로지 DB 테이블에서 정보를 가져와서 해당 측정 데이터에 대한 모풀로지를 재지정한다. 
            #     for mp in MorphologyMap.objects.all():
            #         if mp.wordsCond == '시작단어':
            #             if self.userInfo2.startswith(mp.words):
            #                 morphology = mp.morphology
            #                 manage = mp.manage
            #                 break
            #         elif mp.wordsCond == '포함단어':
            #             if self.userInfo2.find(mp.words) >= 0:
            #                 morphology = mp.morphology
            #                 manage = mp.manage
            #                 break
            morphology = get_morphology(self.userInfo2)
            self.morphology = morphology
            self.manage = morphology.manage

            # 측정 단말기 정보를 저장한다.
            self.save()

        except Exception as e:
            print("update_initial_data():", str(e))
            raise Exception("update_initial_data(): %s" % e) 



###################################################################################################
# 실시간 측정 데이터(콜 단위)
# -------------------------------------------------------------------------------------------------
# 2022.03.10 - 다른 항목 조건을 고려하거나 연산을 해서 가져오는 속성값을 가져오기 위한 함수들 정의(get)
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
        null=True, blank=True, verbose_name="콜카운트"
    )  # 현재 콜카운트
    ispId = models.CharField(
        max_length=10, null=True, blank=True
    )  # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(
        max_length=100, null=True, blank=True
    )  # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="측정자 입력값1")  # 입력된 주소정보
    userInfo2 = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="측정자 입력값2"
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

    # 전화번호 뒤에서 4자리
    def get_phone_no_sht(self):
        return str(self.phone_no)[-4:]

    # DL
    def get_dl(self):
        if self.downloadBandwidth and self.downloadBandwidth > 0:
            return f"{self.downloadBandwidth:.1f}"
        else:
            return '-'

    # UL
    def get_ul(self):
        if self.uploadBandwidth and self.uploadBandwidth > 0:
            return f"{self.uploadBandwidth:.1f}"
        else:
            return '-'


    # PCI
    def get_pci(self):
        if self.networkId == '5G':
            return self.NR_PCI
        else:
            return self.p_pci

    # RSRP
    def get_rsrp(self):
        if self.networkId == '5G':
            return self.NR_RSRP
        else:
            return self.p_rsrp

    # SINR
    def get_sinr(self):
        if self.networkId == '5G':
            return self.NR_SINR
        else:
            return self.p_SINR

    # 측정시간(예: 09:37)
    def get_time(self):
        if self.meastime:
            meastime_s = str(self.meastime)
            return f"{meastime_s[8:10]}:{meastime_s[10:12]}"
        else:
            return ''

    # 측정위치(예: 경상남도 사천시 노룡동)
    def get_address(self):
        if self.addressDetail and self.addressDetail != None:
            return f"{self.siDo} {self.guGun} {self.addressDetail.split(' ')[0]}"
        else:
            # 2022.03.10 - NR인 경우 주소정보(siDo, guGun, addressDetail)가 널(Null)임
            # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
            rest_api_key = settings.KAKAO_REST_API_KEY
            kakao = KakaoLocalAPI(rest_api_key)
            input_coord = "WGS84" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
            output_coord = "TM" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

            result = kakao.geo_coord2regioncode(self.longitude,self.latitude, input_coord, output_coord)
            # [ 리턴값 형식 ]
            # print("out_measuring_range():", result)
            # {'meta': {'total_count': 2},
            # 'documents': [{'region_type': 'B',
            # 'code': '4824012400',
            # 'address_name': '경상남도 사천시 노룡동',
            # 'region_1depth_name': '경상남도',
            # 'region_2depth_name': '사천시',
            # 'region_3depth_name': '노룡동', <-- 주소지 동
            # 'region_4depth_name': '',
            # 'x': 296184.5342265043,
            # 'y': 165683.29710986698},
            # {'region_type': 'H',
            # 'code': '4824059500',
            # 'address_name': '경상남도 사천시 남양동',
            # 'region_1depth_name': '경상남도',
            # 'region_2depth_name': '사천시',
            # 'region_3depth_name': '남양동', <-- 행정구역
            # 'region_4depth_name': '',
            # 'x': 297008.1130364056,
            # 'y': 164008.47612447804}]}
            region_1depth_name = result['documents'][0]['region_1depth_name']
            region_2depth_name = result['documents'][0]['region_2depth_name']
            region_3depth_name = result['documents'][0]['region_3depth_name']

            return ' '.join([region_1depth_name, region_2depth_name, region_3depth_name])
        

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
        return f"{self.phone_no}/{self.networkId}/{self.meastime}/{self.currentCount}/{self.downloadBandwidth}/{self.uploadBandwidth}/"


###################################################################################################
# 전송 메시지 클래스
# 2022.02.25 - 의존성으로 마이그레이트 및 롤백 시 오류가 자주 발생하여 모니터 앱으로 옮겨 왔음
# 2022.02.27 - 메시지 유형을 메시지(SMS)와 이벤트(EVENT)로 구분할 수 있도록 항목 추가
###################################################################################################
class Message(models.Model):
    '''전송 메시지'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, null=True) # 메시지 전송시 측정단말의 상태
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
# 생성된 메시지 타입에 따라서 크로샷 또는 텔레그램으로 전송하는 함수
#--------------------------------------------------------------------------------------------------
def send_message(sender, **kwargs):
    '''생성된 메시지를 크로샷 또는 텔레그램으로 전송하는 함수'''
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
        send_sms()

# -------------------------------------------------------------------------------------------------
# 전송 메시지가 저장된 후 메시지 전송 모듈을 호출한다(SIGNAL). 
#--------------------------------------------------------------------------------------------------
post_save.connect(send_message, sender=Message)


