from operator import itemgetter
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from .geo import KakaoLocalAPI
from message.tele_msg import TelegramBot  # 텔레그램 메시지 전송 클래스
from message.xmcs_msg import send_sms  # 2022.03.04 크로샷 메시지 전송 함수 호출
from management.models import Center, Morphology, MorphologyMap, CenterManageArea

# import logging
# logger = logging.getLogger(__name__)

########################################################################################################################
# 측정 단말그룹 정보
#               ┏ ------┓
#   ┌ ----------┴---┐   | - update_initial_data() : 객체생성시 한번 수행
#   |  PhoneGroup   |<- ┛   * 측정조
#   |  (단말그룹)   |       * 측정유형(5G,LTE,3G,WiFi)
#   ┗ --------------┛       * # 관할센터
#
# ----------------------------------------------------------------------------------------------------------------------
# 2022.02.25 - 해당지역에 단말이 첫번째 측정을 시작했을 때 측정시작(START) 메시지를 한번 전송한다.
# 2022.03.06 - 측정 데이터에 통신사(ispId)가 널(NULL)인 값이 들어와서 동일하게 모델의 해당 항목에 널을 허용함
# 2022.03.11 - 단말그룹에 묶여 있는 측정 단말기들이 당일 이전에 측정이 있었는지 확인하고 있었다면 그때 단말그룹 측정조 값을
#              가져와서 업데이트 하는 모듈 추가
# 2022.03.16 - 주기보고 모듈을 복잡도를 낮추기 위해서 단말그룹에 DL/UL 콜카운트와 LTE전환 콜카운트를 가져감
#              DL콜카운트, UL콜가운트, DL LTE전환 콜카운트, UL LTE전환 콜카운트
# 2022.03.17 - 측정종료 및 측정마감 시 코드 복잡성을 낮추기 위해서 단말그룰에 측정유형(networkId)을 가져감
# 2022.03.18 - 측정마감 모델(MeasuringDayClose)  추가
# 2022.03.19 - 관할센터(Center) 외래키 항목 추가
# 2022.03.22 - 단말그룹에 관리대상 여부 항목 추가
# 2022.03.28 - 단말그룹에 DL평균속도, UL평균속도, DL LTE전환율, UL LTE전환율, LTE 전환율, 이벤트발생건수 항목 추가
#
########################################################################################################################
class PhoneGroup(models.Model):
    """측정 단말기 그룹정보"""
    MEASURINGTEAM_CHOICES = (
        ("1조", "1조"),
        ("2조", "2조"),
        ("3조", "3조"),
        ("4조", "4조"),
        ("5조", "5조"),
    )
    ISPID_CHOICES = (
        ("45008", "KT"),
        ("45005", "SKT"),
        ("45006", "LGU+"),
    )

    measdate = models.CharField(max_length=10, verbose_name="측정일자")
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    userInfo2 = models.CharField(max_length=100, verbose_name="측정자 입력값2")
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name="유형")  # 네트워크ID(5G, LTE, 3G, WiFi)
    center = models.ForeignKey(Center, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="센터")
    morphology = models.ForeignKey(Morphology, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="모풀로지")
    measuringTeam = models.CharField(max_length=20, null=True, blank=True, \
                                     choices=sorted(MEASURINGTEAM_CHOICES, key=itemgetter(0)), verbose_name='측정조')
    ispId = models.CharField(max_length=10, null=True, blank=True, choices=ISPID_CHOICES, \
                             verbose_name="통신사")  # 한국:450 / KT:08, SKT:05, LGU+:60
    downloadBandwidth = models.FloatField(null=True, default=0.0, verbose_name="DL속도")
    uploadBandwidth = models.FloatField(null=True, default=0.0, verbose_name="UL속도")
    dl_count = models.IntegerField(null=True, default=0, verbose_name="DL콜수")  # 다운로드 콜수
    ul_count = models.IntegerField(null=True, default=0, verbose_name="UL콜수")  # 업로드 콜수
    dl_nr_count = models.IntegerField(null=True, default=0)  # 5G->NR 전환 콜수(DL)
    ul_nr_count = models.IntegerField(null=True, default=0)  # 5G->NR 전환 콜수(UL)
    dl_nr_percent = models.FloatField(null=True, default=0.0, verbose_name="DL LTE전환율") # DL LTE전환율
    ul_nr_percent = models.FloatField(null=True, default=0.0, verbose_name="UL LTE전환율") # UL LTE전환율
    nr_percent = models.FloatField(null=True, default=0.0, verbose_name="LTE전환율")  # LTE전환율
    event_count = models.IntegerField(null=True, default=0, verbose_name="이벤트")  # 이벤트발생건수
    manage = models.BooleanField(default=False, verbose_name="관리대상")  # 관리대상 여부
    active = models.BooleanField(default=True, verbose_name="상태")
    last_updated = models.BigIntegerField(null=True, blank=True, verbose_name="최종보고시간")  # 최종 위치보고시간

    class Meta:
        verbose_name = "단말 그룹"
        verbose_name_plural = "단말 그룹"

    def __str__(self):
        return f"{self.measdate} / {self.userInfo1} / {self.morphology}"

    # 해당 단말그룹의 측정조를 업데이트 한다.
    def update_initial_data(self):
        """ 단말그룹이 생성될 때 한번만 업데이트를 수핸한다.
            - 업데이트 항목: 측정조, 측정유형(5G,LTE,3G,WiFi), 관할센터
        """
        phone_list = [p.phone_no for p in self.phone_set.all()]
        qs = Phone.objects.filter(measdate=self.measdate, phone_no__in=phone_list).exclude(phoneGroup=self)
        if qs.exists():
            measuringTeam = None
            for p in qs:
                # print(p, p.phoneGroup.id, p.phoneGroup.measuringTeam)
                if p.phoneGroup.measuringTeam and p.phoneGroup.measuringTeam != None:
                    measuringTeam = p.phoneGroup.measuringTeam
                    break
            self.measuringTeam = measuringTeam

        # 2022.03.17 - 측정종료 및 측정마감 시 코드 복잡성을 낮추기 위해 측정유형(networkId)을 가져감
        #            - 단말그룹에 묶여 있는 측정 단말의 측정유형을 가져와서 업데이트 한다.
        # 2022.03.19 - 관할센터를 업데이트 한다.
        qs = self.phone_set.all()
        if qs.exists():
            self.networkId = qs[0].networkId  # 측정유형(5G,LTE,3G,WiFi)
            self.center = qs[0].center  # 관할센터

        # 단말그룹 정보를 업데이트 한다.
        self.save()

    # 다운로드(DL) 콜카운트를 하나 증가시킨다.
    def add_dl_count(self):
        """DL 콜카운트를 증가시킨다."""
        self.dl_count += 1
        self.save()

    # 업로드(UL) 콜카운트를 하나 증가시킨다.
    def add_ul_count(self):
        """UL 콜카운트를 증가시킨다."""
        self.ul_count += 1
        self.save()

    # 다운로드(DL) LTE전환 콜카운트를 하나 증가시킨다.
    def add_dl_nr_count(self):
        """LTE전환 DL 콜카운트를 증가시킨다."""
        self.dl_nr_count += 1
        self.save()

    # 다운로드(UL) LTE전환 콜카운트를 하나 증가시킨다.
    def add_ul_nr_count(self):
        """LTE전환 UL 콜카운트를 증가시킨다."""
        self.ul_nr_count += 1
        self.save()

    # 측정조를 반환한다.
    def get_measuringTeam(self):
        """측정조를 반환한다."""
        return self.measuringTeam if self.measuringTeam is not None else ''


# ----------------------------------------------------------------------------------------------------------------------
# 측정자 입력값2(userInfo2)로 모폴로지를 확인한다.
# 2022.03.15 - 측정자 입력값(userInfo2)가 입력오류가 자주 발생하므로 모폴로지를 찾지 못하는 경우 "행정동"으로 초기화 함
# ----------------------------------------------------------------------------------------------------------------------
def get_morphology(userInfo2: str) -> Morphology:
    """ 측정자 입력값2로 모폴로지를 반환한다.
        - 모폴로지를 찾을 수 없는 경우 기본값으로 '행정동'을 반환한다.
        - 파리미터: 측정자 입력값2(문자열)
        - 반환값: 모폴러지(Morphology)
    """
    # 측정자 입력값2(userInfo2)에 따라 모폴로지를 결정한다.
    morphology = Morphology.objects.filter(morphology='행정동')[0]  # 초기값 설정
    if userInfo2 and userInfo2 is not None:
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


########################################################################################################################
# 측정단말 정보
# * 측정중인 단말을 관리한다.
# * 측정이 종료되면 해당 측정 단말기 정보를 삭제한다. (Active or Inactive 관리도 가능)
#               ┏ ------┓
#   ┌ ----------┴---┐   | - update_initial_data() : 객체생성시 한번 수행
#   |     Phon      |<- ┛  * 행정동, 모폴로지, 관할센터, 관리대상 여부
#   |  (측정단말)   ┣-- ┓
#   ┗ -----------∧--┛   | - update_phone(mdata): 실시간 측정데이터로 측정단말 정보를 업데이트 수행
#                |      |
#                ┗------┛
# ----------------------------------------------------------------------------------------------------------------------
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
# 2022.03.19 - 관할센터(Center) 외래키 항목 추가
# 2022.03.28 - 단말그룹의 이벤트발생 건수를 업데이트 하는 코드를 추가함
#
########################################################################################################################
class Phone(models.Model):
    """측정 단말기 정보"""

    ISPID_CHOICES = (
        ("45008", "KT"),
        ("45005", "SKT"),
        ("45006", "LGU+"),
    )
    STATUS_CHOICES = (
        ("POWERON", "PowerOn"),
        ("START_F", "측정시작"),
        ("START_M", "측정시작"),
        ("MEASURING", "측정중"),
        ("END", "측정종료"),
    )
    MEASTYPE_CHOICES = (
        ("DL", "DL"),
        ("UL", "UL")
    )

    phoneGroup = models.ForeignKey(PhoneGroup, on_delete=models.DO_NOTHING)
    measdate = models.CharField(max_length=10, verbose_name="측정일자")
    starttime = models.CharField(max_length=10, verbose_name="측정시작시간")  # 측정시작시간
    phone_no = models.BigIntegerField(verbose_name="측정단말")
    meastype = models.CharField(max_length=10, null=True, blank=True, choices=MEASTYPE_CHOICES, verbose_name="측정유형")
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    userInfo2 = models.CharField(max_length=100, verbose_name="측정자 입력값2")
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name="유형")  # 네트워크ID(5G, LTE, 3G, WiFi)
    ispId = models.CharField(max_length=10, null=True, blank=True, choices=ISPID_CHOICES, \
                             verbose_name="통신사")  # 한국:450 / KT:08, SKT:05, LGU+:60
    downloadBandwidth = models.FloatField(null=True, default=0.0, verbose_name="DL")
    uploadBandwidth = models.FloatField(null=True, default=0.0, verbose_name="UL")
    dl_count = models.IntegerField(null=True, default=0, verbose_name="DL콜수")  # 다운로드 콜수
    ul_count = models.IntegerField(null=True, default=0, verbose_name="UL콜수")  # 업로드 콜수
    nr_count = models.IntegerField(null=True, default=0, verbose_name="LTE전환콜수")  # 5G->NR 전환 콜수
    status = models.CharField(max_length=10, null=True, choices=STATUS_CHOICES, verbose_name="진행단계")
    currentCount = models.IntegerField(null=True, blank=True, verbose_name="현재 콜카운트")
    total_count = models.IntegerField(null=True, default=0, verbose_name="콜 카운트")
    siDo = models.CharField(max_length=100, null=True, blank=True, verbose_name="시,도")  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True, verbose_name="군,구")  # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True, verbose_name="상세주소")  # 주소상세
    latitude = models.FloatField(null=True, blank=True, verbose_name="위도")  # 위도
    longitude = models.FloatField(null=True, blank=True, verbose_name="경도")  # 경도
    last_updated = models.BigIntegerField(null=True, blank=True, verbose_name="최종보고시간")  # 최종 위치보고시간
    center = models.ForeignKey(Center, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="센터")
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
        """전화번호 끝 4자리를 반환한다."""
        return str(self.phone_no)[-4:]

    # ------------------------------------------------------------------------------------------------------------------
    # 모델을 DB에 저장하는 함수(오버라이딩)
    # - 모델을 DB에 저장하기 전에 처리해야 하는 것들을 작선하다.
    # * 모풀로지가 변경되는 경우 측정 단말기의 관래대상 여부를 자동으로 변경한다.
    # ------------------------------------------------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """측정단말 정보를 저장한다."""
        qs = Morphology.objects.filter(morphology=self.morphology)
        if qs.exists():
            self.manage = qs[0].manage
        else:
            self.manage = False
        super(Phone, self).save(*args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    # 측정 단말기의 통계정보를 업데이트 하는 합수
    # - DL/UL 평균속도, 콜수, 진행상태, 최종 위치보고시간 등
    # ------------------------------------------------------------------------------------------------------------------
    def update_phone(self, mdata):
        """ 측정단말의 통계정보를 업데이트 한다.
            - 업데이트 항목: 평균속도, 콜 카운트, 측정단말 상태, 최종 위치보고시간
            - NR(5G->LTE전환)인 경우 평균속도에는 반영하지 않고, 콜 카운트에는 반영한다.
            - 파라미터
              . mdata: 측정 데이터(콜단위) (MeasureCallData)
            - 반환값: 없음
        """
        # UL/DL 평균속도 산출시 NR(5G->LTE전환) 데이터는 제외한다.
        # 2022.02.26 - 측정 데이터를 가져와서 재계산 방식에서 수신 받은 한건에 대해서 누적 재계산한다.
        # 2022.03.16 - 주기보고 모듈을 복잡도를 낮추기 위해서 단말그룹에 DL/UL 콜카운트와 LTE전환 콜카운트를 가져감
        #              측정단말 정보 업데이트 시 단말그룹의 콜카운트 관련 정보도 함께 업데이트 함
        phoneGroup = self.phoneGroup # 단말그룹
        if mdata.networkId == 'NR':
            # DL속도 및 UL속도가 0(Zero)이면 NR 콜카운트에서 제외함
            if mdata.downloadBandwidth and mdata.downloadBandwidth > 0:
                self.nr_count += 1
                phoneGroup.dl_nr_count += 1
            elif mdata.uploadBandwidth and mdata.uploadBandwidth > 0:
                self.nr_count += 1
                phoneGroup.ul_nr_count += 1
        else:
            # DL 평균속도 계산
            if mdata.downloadBandwidth and mdata.downloadBandwidth > 0:
                self.downloadBandwidth = round(
                    ((self.downloadBandwidth * self.dl_count) + mdata.downloadBandwidth) / (self.dl_count + 1), 3)
                self.meastype = 'DL'
                self.dl_count += 1
                # 단말그룹 - DL평균속도, DL콜카운트
                phoneGroup.downloadBandwidth = round(
                    ((phoneGroup.downloadBandwidth * phoneGroup.dl_count) + mdata.downloadBandwidth) / (phoneGroup.dl_count + 1), 3)
                phoneGroup.dl_count += 1
            # UP 평균속도 계산
            if mdata.uploadBandwidth and mdata.uploadBandwidth > 0:
                self.uploadBandwidth = round(
                    ((self.uploadBandwidth * self.ul_count) + mdata.uploadBandwidth) / (self.ul_count + 1), 3)
                self.meastype = 'UL'
                self.ul_count += 1
                # 단말그룹 - UL평균속도, UL콜카운트
                phoneGroup.uploadBandwidth = round(
                    ((phoneGroup.uploadBandwidth * phoneGroup.ul_count) + mdata.uploadBandwidth) / (phoneGroup.ul_count + 1), 3)
                phoneGroup.ul_count += 1

        # 현재 콜카운트와 전체 콜건수를 업데이트 한다.
        self.currentCount = mdata.currentCount  # 현재 콜카운트
        self.total_count = self.dl_count + self.ul_count + self.nr_count  # 전체 콜건수

        # 단말그룹 - DL LTE전환율, UL LTE전환율, LTE전환율
        if phoneGroup.dl_count > 0:
            phoneGroup.dl_nr_percent = round(phoneGroup.dl_nr_count / (phoneGroup.dl_count + phoneGroup.dl_nr_count) * 100,1)
        if phoneGroup.ul_count > 0:
            phoneGroup.ul_nr_percent = round(phoneGroup.ul_nr_count / (phoneGroup.ul_count + phoneGroup.ul_nr_count) * 100,1)
        if phoneGroup.dl_count > 0 or phoneGroup.ul_count > 0:
            phoneGroup.nr_percent = round((phoneGroup.dl_nr_count + phoneGroup.ul_nr_count) / \
                (phoneGroup.dl_count + phoneGroup.dl_nr_count + phoneGroup.ul_count + phoneGroup.ul_nr_count) * 100,1)

        # 단말기의 상태를 업데이트 한다.
        # 상태 - 'POWERON', 'START_F', 'START_M', 'MEASURING', 'END'
        # 2022.03.11 - 측정시작 메시지 분리 반영 (전체대상 측정시작: START_F, 해당지역 측정시작: START_M)
        if self.total_count <= 1:
            self.status = "START_M"
        else:
            self.status = "MEASURING"

        # 최종 위치보고시간을 업데이트 한다.
        self.last_updated = mdata.meastime
        phoneGroup.last_updated = mdata.meastime

        # 측정단말, 단말그룹 정보를 데이터베이스에 저장한다.
        self.save() # 측정단말
        phoneGroup.save() # 단말그룹

    # ------------------------------------------------------------------------------------------------------------------
    # 측정 단말기가 최조 생성될 때 한번만 처리하기 위한 함수
    # - 해당 위치(위도,경도)에 대한 주소지를 행정동으로 변환하여 업데이트 한다.
    # - 측정 데이터의 userInfo2를 확인하여 모풀로지를 매핑하여 지정한다.
    # 2022.03.19 - 센터별 관할구역 맵핑 정보를 통해 관할센터를 업데이트 한다.
    # ------------------------------------------------------------------------------------------------------------------
    def update_initial_data(self):
        """ 측정 단말기가 생성될 때 최초 한번만 단말정보를 업데이트 한다.
            - 업데이트 항목: 측정시작 위치에 대한 행정동, 모폴러지, 관할센터
            - 파라미터: 없음
            - 반환값: 없음
        """
        try:
            # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
            if self.longitude and self.latitude:
                rest_api_key = settings.KAKAO_REST_API_KEY
                kakao = KakaoLocalAPI(rest_api_key)
                input_coord = "WGS84"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
                output_coord = "TM"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

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

                region_1depth_name = result['documents'][1]['region_1depth_name']  # 시/도
                region_2depth_name = result['documents'][1]['region_2depth_name']  # 구/군
                region_3depth_name = result['documents'][1]['region_3depth_name']  # 행정동(읍/동/면)

                self.siDo = region_1depth_name  # 시/도
                self.guGun = region_2depth_name  # 구/군
                self.addressDetail = region_3depth_name  # 행정동(읍/동/면)

            # 모폴로지와 관리대상 여부를 설정한다.
            morphology = get_morphology(self.userInfo2) # 측정자 입력값2
            self.morphology = morphology # 모폴로지
            self.manage = morphology.manage # 관리대상 여부

            # 센터별 관할구역 매핑정보를 통해 관할센터를 업데이트 한다.
            qs = CenterManageArea.objects.filter(siDo=self.siDo, guGun=self.guGun)
            if qs.exists():
                self.center = qs[0].center  # 관할센터

            # 측정 단말기 정보를 저장한다.
            self.save()

        except Exception as e:
            print("update_initial_data():", str(e))
            raise Exception("update_initial_data(): %s" % e)


########################################################################################################################
# 실시간 측정 데이터(콜 단위)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.10 - 다른 항목 조건을 고려하거나 연산을 해서 가져오는 속성값을 가져오기 위한 함수들 정의(get)
# 2022.03.15 - 주소 반환시 시/도와 구/군이 동일한 경우 한번만 주소값에 반환하도록 수정함
########################################################################################################################
class MeasureCallData(models.Model):
    """실시간 측정 데이터(콜 단위) 정보"""

    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(null=True, blank=True, verbose_name="전화번호")  # 전화번호
    meastime = models.BigIntegerField(null=True, blank=True, verbose_name="측정시간")  # 측정시간
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name="유형")  # 네트워크ID(5G, LTE, 3G, WiFi)
    groupId = models.CharField(max_length=100, null=True, blank=True)  # 그룹ID
    currentTime = models.CharField(max_length=100, null=True, blank=True)  # 현재시간
    timeline = models.CharField(max_length=100, null=True, blank=True)  # 타입라인
    cellId = models.CharField(max_length=100, null=True, blank=True, verbose_name="셀ID")  # 셀ID
    currentCount = models.IntegerField(null=True, blank=True, verbose_name="콜카운트")  # 현재 콜카운트
    ispId = models.CharField(max_length=10, null=True, blank=True)  # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(max_length=100, null=True, blank=True)  # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="측정자 입력값1")  # 입력된 주소정보
    userInfo2 = models.CharField(max_length=100, null=True, blank=True, \
                                 verbose_name="측정자 입력값2")  # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    siDo = models.CharField(max_length=100, null=True, blank=True)  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True)  # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True, verbose_name="주소상세")  # 주소상세
    udpJitter = models.FloatField(null=True, blank=True)  # 지연시간
    downloadBandwidth = models.FloatField(null=True, blank=True, verbose_name="DL")  # DL속도
    uploadBandwidth = models.FloatField(null=True, blank=True, verbose_name="UL")  # UP속도
    sinr = models.FloatField(null=True, blank=True)  # SINR
    isWifi = models.CharField(max_length=100, null=True, blank=True)  # 와이파이 사용여부
    latitude = models.FloatField(null=True, blank=True)  # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도
    bandType = models.CharField(max_length=16, null=True, blank=True)  # CA(ex.1CL2-> 1CA(20M), 3CL4->3CA(40M))
    p_dl_earfcn = models.IntegerField(null=True, blank=True)  # P 주파수
    p_pci = models.IntegerField(null=True, blank=True)  # P PCI
    p_rsrp = models.FloatField(null=True, blank=True)  # P RSRP
    p_SINR = models.FloatField(null=True, blank=True)  # P SINR
    NR_EARFCN = models.IntegerField(null=True, blank=True)  # 5G 주파수
    NR_PCI = models.IntegerField(null=True, blank=True)  # 5G CI
    NR_RSRP = models.FloatField(null=True, blank=True)  # 5G PCI
    NR_SINR = models.FloatField(null=True, blank=True)  # 5G SINR
    # before_lat = models.FloatField(null=True, blank=True) # 이전 위도 - 의미없음(위도와 동일)
    # before_lon = models.FloatField(null=True, blank=True) # 이전 경도 - 의미없음(경도와 동일)

    # 전화번호 뒤에서 4자리를 반환한다.
    def get_phone_no_sht(self):
        """전화번호 끝 4자리를 리턴한다."""
        return str(self.phone_no)[-4:]

    # DL 속도를 반환한다.
    def get_dl(self):
        """DL 속도를 반환한다."""
        if self.downloadBandwidth is not None and self.downloadBandwidth > 0:
            return f"{self.downloadBandwidth:.1f}"
        else:
            return '-'

    # UL 속도를 반환한다.
    def get_ul(self):
        """UL 속도를 반환한다."""
        if self.uploadBandwidth is not None and self.uploadBandwidth > 0:
            return f"{self.uploadBandwidth:.1f}"
        else:
            return '-'

    # PCI를 반환한다.
    def get_pci(self):
        """PCI를 반환한다."""
        if self.networkId == '5G':
            return self.NR_PCI
        else:
            return self.p_pci

    # RSRP를 반환한다.
    def get_rsrp(self):
        """RSRP 값을 반환한다."""
        if self.networkId is not None and self.networkId == '5G':
            return self.NR_RSRP
        else:
            return self.p_rsrp

    # SINR를 반환한다.
    def get_sinr(self):
        """SINR 값을 리턴한다."""
        if self.networkId is not None and self.networkId == '5G':
            return self.NR_SINR
        else:
            return self.p_SINR

    # 측정시간을 반환한다(예: 09:37).
    def get_time(self):
        """ 측정시간을 반환한다.
            - 예) 09:30
        """
        if self.meastime:
            meastime_s = str(self.meastime)
            return f"{meastime_s[8:10]}:{meastime_s[10:12]}"
        else:
            return ''

    # 측정위치를 반환한다(예: 경상남도 사천시 노룡동).
    def get_address(self) -> str:
        """ 측정위치에 대한 주소를 반환한다.
            - 시/도, 군/구가 동일한 경우 한번만 표시한다.
              . 서울특벌시 서욽특벌시 가산동 -> 서울특별시 가산동
            - 측정위치의 위도와 경도는 있는데, 주소가 널(Null)인 경우 주소를 찾아서 반환한다.
            - 파라미터: 없음
            - 반환값: 주소(문자열)

        """
        if self.addressDetail is not None:
            if self.siDo in self.guGun:
                address = f"{self.guGun} {self.addressDetail.split(' ')[0]}"
            else:
                address = f"{self.siDo} {self.guGun} {self.addressDetail.split(' ')[0]}"
            return address
        else:
            # 2022.03.10 - NR인 경우 주소정보(siDo, guGun, addressDetail)가 널(Null)임
            # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
            rest_api_key = settings.KAKAO_REST_API_KEY
            kakao = KakaoLocalAPI(rest_api_key)
            input_coord = "WGS84"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
            output_coord = "TM"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

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
            region_1depth_name = result['documents'][0]['region_1depth_name']
            region_2depth_name = result['documents'][0]['region_2depth_name']
            region_3depth_name = result['documents'][0]['region_3depth_name']

            return ' '.join([region_1depth_name, region_2depth_name, region_3depth_name])

    class Meta:
        verbose_name = "측정 데이터(콜단위)"
        verbose_name_plural = "측정 데이터(콜단위)"

    def __str__(self):
        return f"{self.phone_no}/{self.networkId}/{self.meastime}/{self.currentCount}/{self.downloadBandwidth}/{self.uploadBandwidth}"


########################################################################################################################
# 실시간 측정 데이터(초 단위)
########################################################################################################################
class MeasureSecondData(models.Model):
    """실시간 측정 데이터(초 단위) 정보"""

    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    dataType = models.CharField(max_length=10)
    phone_no = models.BigIntegerField(null=True, blank=True)  # 전화번호
    meastime = models.BigIntegerField(null=True, blank=True)  # 측정시간
    neworkid = models.CharField(max_length=100, null=True, blank=True)  # 네트워크ID(5G, LTE, 3G, WiFi)
    groupId = models.CharField(max_length=100, null=True, blank=True)  # 그룹ID
    currentTime = models.CharField(max_length=100, null=True, blank=True)  # 현재시간
    timeline = models.CharField(max_length=100, null=True, blank=True)  # 타입라인
    cellId = models.CharField(max_length=100, null=True, blank=True)  # 셀ID
    currentCount = models.IntegerField(null=True, blank=True)  # 현재 콜카운트
    ispId = models.CharField(max_length=10, null=True, blank=True)  # 한국:450 / KT:08, SKT:05, LGU+:60
    testNetworkType = models.CharField(max_length=100, null=True, blank=True)  # 측정종류(speed, latency, web)
    userInfo1 = models.CharField(max_length=100, null=True, blank=True)  # 입력된 주소정보
    userInfo2 = models.CharField(max_length=100, null=True, blank=True)  # 측정위치(행정동, 테마, 인빌딩, 커버리지)
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
    bandType = models.CharField(max_length=16, null=True, blank=True)  # CA(ex.1CL2-> 1CA(20M), 3CL4->3CA(40M))
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


########################################################################################################################
# 전송 메시지 클래스
#               ModelSignal
#               ┏ ------┓
#   ┌ ----------┴---┐   | post_save ------> send_message(sender, instance, created, **kwargs)
#   |    Message    |<- ┛ (SIGNAL)              |
#   | (전송메시지)  |                           |           ┌ --------------┐
#   ┗ --------------┛                           ┣---------->|  TelegramBot  |
#                                               |           ┗ --------------┛
#                                                           - send_message_bot()          Node.js
#                                               |           ┌ -----------------┐          ┌ -----------------┐
#                                               ┗ --------->| message.xmcs_msg |--------->| sms_api.js       |
#                                                           |                  |          | sms_broadcast.js |
#                                                           ┗ -----------------┛          ┗ -----------------┛
#                                                           - send_sms()
# ----------------------------------------------------------------------------------------------------------------------
# 2022.02.25 - 의존성으로 마이그레이트 및 롤백 시 오류가 자주 발생하여 모니터 앱으로 옮겨 왔음
# 2022.02.27 - 메시지 유형을 메시지(SMS)와 이벤트(EVENT)로 구분할 수 있도록 항목 추가
# 2022.03.27 - 메시지가 생성되었을 때만 처리하도록 코드를 수정함(created=True)
# 2022.03.29 - 전송 메시지 모델에 대한 흐름도 및 주석 추가
#
########################################################################################################################
class Message(models.Model):
    """전송 메시지 정보"""
    phone = models.ForeignKey(Phone, null=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, null=True)  # 메시지 전송시 측정단말의 상태
    measdate = models.CharField(max_length=10) # 측정일자(예: 20211101)
    sendType = models.CharField(max_length=10)  # 전송유형(TELE: 텔레그램, XMCS: 크로샷)
    #### 디버깅을 위해 임시로 만든 항목(향후 삭제예정) ###########
    userInfo1 = models.CharField(max_length=100, null=True, blank=True) # 측정자 입력값1
    currentCount = models.IntegerField(null=True, blank=True) # 현재 콜카운트
    phone_no = models.BigIntegerField(null=True, blank=True) # 측정단말 전화번호
    downloadBandwidth = models.FloatField(null=True, blank=True)  # DL속도
    uploadBandwidth = models.FloatField(null=True, blank=True)  # UP속도
    ##############################################################
    messageType = models.CharField(max_length=10)  # 메시지유형(SMS: 메시지, EVENT: 이벤트)
    message = models.TextField(default=False) # 메시지 내용
    channelId = models.CharField(max_length=25) # 채널ID
    # messageId = models.BigIntegerField(null=True, blank=True) # 메시지ID (메시지 회수할 때 사용)
    sended = models.BooleanField(default=True) # 전송여부
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')

# ----------------------------------------------------------------------------------------------------------------------
# 생성된 메시지 타입에 따라서 크로샷 또는 텔레그램으로 전송하는 함수
# ----------------------------------------------------------------------------------------------------------------------
# def send_message(sender, **kwargs):
def send_message(sender, instance, created, **kwargs):
    """ 생성된 메시지를 크로샷 또는 텔레그램으로 전송하는 함수
        - 파라미터
          . sender: 메시지 모델 클래스
          . instance: 메시지 객체 (생성된 레코드 하나 데이터)
          . created: 신규생성 여부(True or False)
          . kwargs: 키워트 파라미터
        - 반환값: 없음
    """
    # 메시지가 생성되었을 때만 처리한다.
    if created:
        bot = TelegramBot()  ## 텔레그램 인스턴스 선언(3.3)
        # 텔레그램으로 메시지를 전송한다.
        if instance.sendType == 'TELE':
            bot.send_message_bot(instance.channelId, instance.message)
        # 크로샷으로 메시지를 전송한다.
        elif instance.sendType == 'XMCS':
            # 2022.03.04 - 크로샷 메시지 전송  --  node.js 파일 호출하여 전송
            # 현재 변수 전달(메시지/수신번호) 구현되어 있지 않아 /message/sms_broadcast.js에 설정된 내용/번호로만 전송
            # npm install request 명령어로 모듈 설치 후 사용 가능
            send_sms()
    else:
        # 메시지가 업데이트 되었을 때는 아무런 처리를 하지 않는다.
        pass


# ----------------------------------------------------------------------------------------------------------------------
# 전송 메시지가 저장된 후 메시지 전송 모듈을 호출한다(SIGNAL). 
# ----------------------------------------------------------------------------------------------------------------------
post_save.connect(send_message, sender=Message)


########################################################################################################################
# 측정마감 클래스
########################################################################################################################
class MeasuringDayClose(models.Model):
    """측정마감 클래스"""
    measdate = models.CharField(max_length=10, verbose_name='측정일자')  # 측정일자(예: 20211101)
    phoneGroup = models.ForeignKey(PhoneGroup, on_delete=models.DO_NOTHING, verbose_name='단말그룹')  # 단말그룹
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name="유형")  # 네트워크ID(5G, LTE, 3G, WiFi)
    center = models.ForeignKey(Center, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="센터")
    morphology = models.ForeignKey(Morphology, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="모풀로지")
    downloadBandwidth = models.FloatField(null=True, blank=True, verbose_name='DL')  # DL속도 (초단위 데이터 평균)
    uploadBandwidth = models.FloatField(null=True, blank=True, verbose_name='UL')  # UP속도 (초단위 데이터 평균)
    dl_count = models.IntegerField(null=True, default=0, verbose_name='DL콜카운트')  # 다운로드 콜수
    ul_count = models.IntegerField(null=True, default=0, verbose_name='UL콜카운트')  # 업로드 콜수
    dl_nr_count = models.IntegerField(null=True, default=0, verbose_name='DL NR 콜카운트')  # 5G->NR 전환 콜수
    ul_nr_count = models.IntegerField(null=True, default=0, verbose_name='UL NR 콜카운트')  # 5G->NR 전환 콜수
    dl_lte_transRate = models.FloatField(null=True, default=0.0, verbose_name='DL LTE전환율')  # 5G->NR 전환 전환율(dl)
    ul_lte_transRate = models.FloatField(null=True, default=0.0, verbose_name='UL LTE전환율')  # 5G->NR 전환 전환율(ul)
    connect_time = models.FloatField(null=True, default=0.0, verbose_name='접속시간')  # 접속시간
    udpJitter = models.FloatField(null=True, default=0.0, verbose_name='지연시간')  # 지연시간
    total_count = models.IntegerField(null=True, default=0, verbose_name='시도호수')  # 시도호수
    success_rate = models.FloatField(null=True, default=0.0, verbose_name='전송성공율')  # 전송성공율
    ##### 디버깅 항목 ########
    ca1_count = models.IntegerField(null=True, default=0, verbose_name='CA1 카운트')  # CA1 카운트
    ca2_count = models.IntegerField(null=True, default=0, verbose_name='CA2 카운트')  # CA2 카운트
    ca3_count = models.IntegerField(null=True, default=0, verbose_name='CA3 카운트')  # CA3 카운트
    ca4_count = models.IntegerField(null=True, default=0, verbose_name='CA4 카운트')  # CA4 카운트
    ###########################
    ca1_rate = models.FloatField(null=True, default=0, verbose_name='CA1 비율')  # CA1 비율
    ca2_rate = models.FloatField(null=True, default=0, verbose_name='CA2 비율')  # CA2 비율
    ca3_rate = models.FloatField(null=True, default=0, verbose_name='CA3 비율')  # CA3 비율
    ca4_rate = models.FloatField(null=True, default=0, verbose_name='CA4 비율')  # CA4 비율

