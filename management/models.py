from django.utils import timezone
from django.db import models
from operator import itemgetter

########################################################################################################################
# 환경설정 관리 관련 클래스
#
# [ 관리정보 리스트 ]
#  * 센터정보(Center): 운용본부 및 전국 14개 센터정보를 관리함
#  * 모풀로지(Morphology): 모폴로지를 관리함(행정동, 테마, 인빌딩, 커버리지, 취약지구 등)
#  * 모폴로지 맵(MorphologyMap): 측정 데이터 내에 있는 부정확한 모풀로지를 수정하여 맵핑정보를 관리함
#  * 전송실패 기준(SendFailure): 품질불량에 따른 전송실패 기준 정보를 관리함
#  * 속도저하 기준(LowThroughput): 상황에 따라 변경되는 속도저하 기준 정보를 관리함
#  * 금일 측정조(MeasureingTeam): 당일 측정을 수행하는 측정조 현황을 입력 관리(측정 시작메시지에 포함됨)
#  * 측정 보고주기(ReportCycle): 측정 보고주기를 DB화 함(3, 10, 27, 37, 57)
#  * 행정동 경계구역(AddressRegion): 지도맵에 현재 측정하고 있는 행정동 경계구역을 표시하기 위한 폴리건 데이터(JSON)
#  * 센터별 관할지역(CenterManageArea): 지역센터별 관리대상 주소 정보
#  * 측정단말 사전정보(phoneInfo): 측정단말에 대한 사전 정보
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.05 - 기본 모폴로지를 모폴로지와 모폴로지 맵으로 클래스를 분리함
#              즉, 기존에 하드코딩 되어 있는 '행정동', '테마', '인빌딩', '커버리지' 등을 DB로 등로관리 할 수 있도록 함
#            - 측정 보고주기를 하드코딩에서 DB화 함
# 2022.03.12 - 지도맵에 현재 측정하고 있는 행정동 경계구역을 표시하기 위한 폴리건 데이터 모델(JSON) 추가
# 2022.03.18 - 센터별 관할지역(CenterManageArea) 맵핑 정보 추가
# 2022.03.28 - 센터정보 모델에 센터영문명(centerEngName) 항목 추가
# 2022.04.28 - 측정단말에 대한 사전 정보 추가
# 2022.05.18 - 센터정보 전송번호를 대표번호로 변경
#            - 측정단말 사전정보(PhoneInfo)에 위치정보(시/도, 군,구, 상세주소, 위도, 경도), 파워온/오프 항목 추가
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 센터정보 클래스
# ----------------------------------------------------------------------------------------------------------------------
class Center(models.Model):
    """ 센터 정보
        - 운용본부 및 전국 14개 센터정보를 관리한다.
    """
    centerName = models.CharField(max_length=100, verbose_name="센터명")
    centerEngName = models.CharField(max_length=100, null=True, blank=True, verbose_name="센터영문명")
    channelId = models.CharField(max_length=25, verbose_name="채널ID")
    senderNum = models.CharField(max_length=25, null=True, blank=True, verbose_name="대표번호")  ## 문자메시지 전송 시 발신번호
    permissionLevel = models.IntegerField(default=1, verbose_name="권한레벨")
    recipientOfficer = models.CharField(max_length=30, null=True, blank=True, verbose_name="수신 임원")  ## 보고 메시지를 위함
    active = models.BooleanField(default=True, verbose_name="상태")
    class Meta:
        verbose_name = ('센터정보')
        verbose_name_plural = ('센터정보')

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return self.centerName

# ----------------------------------------------------------------------------------------------------------------------
# 모풀로지 정보관리 클래스
# 측정 데이터에서 넘어오는 모폴로지 정보를 기준으로 재정의
# MessureCallData.userinfo2 --> Morphology.morphology : 맵핑정보 관리
# ----------------------------------------------------------------------------------------------------------------------
class Morphology(models.Model):
    """ 모폴로지 정보
        - 행정동, 테마, 인빌딩, 커버리지, 취약지구 등 모폴로지 정보를 관리한다.
    """
    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    morphology = models.CharField(max_length=100, null=True, blank=True,verbose_name='모풀로지')
    manage = models.BooleanField(default=False, verbose_name='관리대상')  # 관리대상 여부
    class Meta:
        verbose_name = ('모풀로지')
        verbose_name_plural = ('모풀로지')

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return self.morphology


# ----------------------------------------------------------------------------------------------------------------------
# 모풀로지 맵 정보관리 클래스
# ----------------------------------------------------------------------------------------------------------------------
class MorphologyMap(models.Model):
    """ 모폴로지 맵핑 정보
        - 측정자 입력값2(userInfo2)에 따라서 모폴로지를 맵핑하는 정보를 관리한다.
        - 예) 행- 시작단어 -> 행정동
             테- 시작단어 -> 테마
             인- 시작단어 -> 인빌딩
             커- 시작단어 -> 커버리지
             커버리지 포함단어 -> 커버리지
             W- 시작단어 -> 인빌딩
    """
    WORDSCOND_CHOICES = (('시작단어','시작단어'), ('포함단어','포함단어'))

    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    words = models.CharField(max_length=200, null=True, blank=True,
                             verbose_name="단어") # 모폴로지 판단 컬럼2 : 특정 단어 포함
    wordsCond = models.CharField(max_length=20, null=True, blank=True, choices=WORDSCOND_CHOICES, verbose_name='조건')
    morphology = models.ForeignKey(Morphology, on_delete=models.DO_NOTHING, verbose_name="모풀로지")
    manage = models.BooleanField(default=False, verbose_name='관리대상')  # 관리대상 여부
    class Meta:
        verbose_name = ('모풀로지 맵')
        verbose_name_plural = ('모풀로지 맵')

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return f"{self.center.centerName} / {self.words} / {self.wordsCond} / {self.morphology.morphology}"


# ----------------------------------------------------------------------------------------------------------------------
# 전송실패(Send Failure) 기준관리 클래스
# ----------------------------------------------------------------------------------------------------------------------
class SendFailure(models.Model):
    """ 전송실패 기준 정보
        - 품질불량에 따른 전송실패 기준 정보를 관리한다.
        - 품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
        - 품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
    """
    AREAIND__CHOICES = (('NORM','보통지역'), ('WEEK', '취약지역'))
    NETWORKID_CHOICES = (('5G','5G'), ('LTE','LTE'), ('3G','3G'), ('WiFi','WiFi'))
    DATATYPE_CHOICES = (('DL','DL'), ('UL','UL'))

    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    areaInd = models.CharField(max_length=10, choices=AREAIND__CHOICES, verbose_name='지역구분')
    networkId = models.CharField(max_length=10, null=True, blank=True, choices=NETWORKID_CHOICES,
                                 verbose_name='단말유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    dataType = models.CharField(max_length=10, choices=DATATYPE_CHOICES, verbose_name='데이터유형') # 데이터유형(DL, UL)
    bandwidth = models.FloatField(null=True, default=0.0, verbose_name='속도')

    class Meta:
        verbose_name = ('전송실패 기준')
        verbose_name_plural = ('전송실패 기준')

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return f"{self.center.centerName} / {self.areaInd} / {self.networkId} / {self.dataType} / {self.bandwidth}"


# ----------------------------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 기준관리 클래스
# ----------------------------------------------------------------------------------------------------------------------
class LowThroughput(models.Model):
    """ 속도저하 기준 정보
        - 상황에 따라 변경되는 속도저하 기준 정보를 관리한다.
    """
    AREAIND__CHOICES = (('NORM','보통지역'), ('WEEK', '취약지역'))
    NETWORKID_CHOICES = (('5G','5G'), ('LTE','LTE'), ('3G','3G'), ('WiFi','WiFi'))
    DATATYPE_CHOICES = (('DL','DL'), ('UL','UL'))

    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    areaInd = models.CharField(max_length=10, choices=AREAIND__CHOICES, verbose_name='지역구분')
    networkId = models.CharField(max_length=10, null=True, blank=True, choices=NETWORKID_CHOICES,
                                 verbose_name='단말유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    dataType = models.CharField(max_length=10, choices=DATATYPE_CHOICES, verbose_name='데이터유형') # 데이터유형(DL, UL)
    bandwidth = models.FloatField(null=True, default=0.0, verbose_name='속도')

    class Meta:
        verbose_name = ('속도저하 기준')
        verbose_name_plural = ('속도저하 기준')

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return f"{self.center.centerName} / {self.areaInd} / {self.networkId} / {self.dataType} / {self.bandwidth}"


# ----------------------------------------------------------------------------------------------------------------------
# 금일측정조 데이터
# ----------------------------------------------------------------------------------------------------------------------
class MeasureingTeam(models.Model):
    """ 금일 측정조 정보
        - 금일 측정조에 대한 정보를 등록 관리한다.
        - 당일 측정시작 메시지 전송시 등록된 금일 측정조에 대한 내용을 포함하여 메시지를 전송한다.
        - 예) ㅇ 금일측정조
              - 5G/LTE 품질 3개조
              - LTE/3G 취약지역 품질 1개조
              - WiFi 품질 1개조
    """
    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    measdate = models.DateField(default=timezone.now, verbose_name="측정일자", help_text="측정일자를 반드시 입력해야 합니다.")
    message = models.TextField(verbose_name="금일 측정조")

    class Meta:
        verbose_name = "금일 측정조"
        verbose_name_plural = "금일 측정조"


# ----------------------------------------------------------------------------------------------------------------------
# 금일측정조 데이터
# ----------------------------------------------------------------------------------------------------------------------
class ReportCycle(models.Model):
    """ 측정 보고주기 정보
        - 측정진행 메시지의 보고주기를 등록 관리한다.
        - 콤마(,)로 분리하여 등록한다
        - 예) 3, 10, 27, 37, 57
    """
    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    reportCycle = models.CharField(max_length=100, verbose_name="보고주기")

    class Meta:
        verbose_name = "측정 보고주기"
        verbose_name_plural = "측정 보고주기"

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return f"{self.center.centerName} / {self.reportCycle}"


# --------------------------------------------------------------------------------------------------------------------
# 행정동 데이터 클래스
# 2022.03.16 - 측정위치 지도맵 제공 기능 취소 (주간보고)
# --------------------------------------------------------------------------------------------------------------------
class AddressRegion(models.Model):
    """ 행정동 경계구역 정보
        - 각각 행정구역에 대한 폴리건 정보를 관리한다.
        - 예) '서울특별시 종로구 이화동' - JSON 데이터
    """
    addressDetail = models.CharField(max_length=100)  # 주소상세
    json_data = models.JSONField(default=dict)


# ----------------------------------------------------------------------------------------------------------------------
# 행정동 데이터 클래스
# ----------------------------------------------------------------------------------------------------------------------
class CenterManageArea(models.Model):
    """센터별 관할지역(CenterManageArea) 맵핑 정보"""
    siDo = models.CharField(max_length=100, null=True, blank=True, verbose_name='시,도')  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True, verbose_name='구,군')  # 구,군
    eupDong = models.CharField(max_length=100, null=True, blank=True, verbose_name='읍,면,동')  # 읍,동
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="주소상세")  # 주소상세
    addrType = models.CharField(max_length=50, null=True, blank=True, verbose_name='도시유형')  # 도시유형
    bonbu = models.CharField(max_length=50, null=True, blank=True, verbose_name='본부')  # 본부
    opCenter = models.CharField(max_length=50, null=True, blank=True, verbose_name='운용센터')  # 운용센터
    team = models.CharField(max_length=50, null=True, blank=True, verbose_name='부서')  # 도시유형
    center = models.ForeignKey(Center, null=True, on_delete=models.DO_NOTHING, verbose_name="센터") # 센터
    
    class Meta:
        verbose_name = "센터별 관할구역"
        verbose_name_plural = "센터별 관할구역"

    # 인스턴스 정보를 출력한다.
    def __str__(self):
        return f"{self.address} / {self.center.centerName}"


# ----------------------------------------------------------------------------------------------------------------------
# 채팅방 멤버 리스트 관리 클래스
# ----------------------------------------------------------------------------------------------------------------------
class ChatMemberList(models.Model):
    """ 채팅방 멤버 리스트
        - 허용(allowed) 컬럼이 False 인 대상이 추방 대상자
    """
    userchatId = models.CharField(max_length=25, verbose_name="채팅ID")  # 텔레그램 가입 시 가지는 고유 Chat ID (ex:5295955513)
    firstName = models.CharField(max_length=100, null=True, blank=True, verbose_name="First Name")  # 유저가 지정한, 본인의 first name
    lastName = models.CharField(max_length=100, null=True, blank=True, verbose_name="Last Name")  # 유저가 지정한, 본인의 last name
    userName = models.CharField(max_length=100, null=True, blank=True, verbose_name="User Name")  # 유저가 지정한, 본인의 username
    center = models.ForeignKey(Center, null=True, on_delete=models.DO_NOTHING, verbose_name="센터")  # 유저가 속한 센터
    chatId = models.CharField(max_length=25, null=True, blank=True, verbose_name="채팅방ID")  # 유저가 속한 채팅방 chat id
    allowed = models.BooleanField(default=False, verbose_name="허용")  # 허용된 유저인지 여부
    isBot = models.BooleanField(default=False, verbose_name="Is Bot")  # 봇(관리자)인지 아닌지 여부
    join = models.BooleanField(null=True, blank=True, verbose_name="참여")  # 현재 채팅방에 참여 중인지 여부
    
    class Meta:
        verbose_name = ('채팅방 멤버 리스트')
        verbose_name_plural = ('채팅방 멤버 리스트')


# ----------------------------------------------------------------------------------------------------------------------
# 측정단말에 대한 사전정보
# ----------------------------------------------------------------------------------------------------------------------
class PhoneInfo(models.Model):
    """ 측정단말에 대한 사전정보 관리(유형, 측정조 등)"""
    MEASURINGTEAM_CHOICES = (
        ("1조", "1조"),
        ("2조", "2조"),
        ("3조", "3조"),
        ("4조", "4조"),
        ("5조", "5조"),
    )
    NETWORKID_CHOICES = (
        ("5G", "5G"),
        ("LTE", "LTE"),
        ("3G", "3G"),
        ("5G 커버리지", "5G 커버리지"),
        ("WiFi", "WiFi")
    )
    phone_no = models.BigIntegerField(verbose_name="측정단말")
    networkId = models.CharField(max_length=100, null=True, blank=True,
                                 choices=sorted(NETWORKID_CHOICES, key=itemgetter(0)), verbose_name="유형")  # 네트워크ID(5G, LTE, 3G, WiFi)
    measuringTeam = models.CharField(max_length=20, null=True, blank=True, \
                                     choices=sorted(MEASURINGTEAM_CHOICES, key=itemgetter(0)), verbose_name='측정조')
    siDo = models.CharField(max_length=100, null=True, blank=True, verbose_name="시,도")  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True, verbose_name="군,구")  # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True, verbose_name="상세주소")  # 주소상세
    latitude = models.FloatField(null=True, blank=True, verbose_name="위도")  # 위도
    longitude = models.FloatField(null=True, blank=True, verbose_name="경도")  # 경도
    power = models.BooleanField(null=True, default=False, verbose_name="파워온/오프")  # 파워온/오프


    @property
    def phone_no_str(self):
        """전화번호(문자열)를 반환한다."""
        # 1029213855
        phone_no_str = str(self.phone_no)
        return '0' + phone_no_str[:2] + '-' + phone_no_str[2:6] + '-' + phone_no_str[6:]

    class Meta:
        verbose_name = ("측정단말 사전정보")
        verbose_name_plural = ("측정단말 사전정보")

class MorphologyDetail(models.Model):
    """ 모폴로지 상세정보 """
    network_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="네트워크")
    main_class = models.CharField(max_length=100, null=True, blank=True, verbose_name="대분류")
    middle_class = models.CharField(max_length=100, null=True, blank=True, verbose_name="중분류")
    sub_class = models.CharField(max_length=100, null=True, blank=True, verbose_name="소분류")

    class Meta:
        verbose_name = ("모폴로지 상세")
        verbose_name_plural = ("모폴로지 상세")

# Large Category Medium Category Small Category


# ----------------------------------------------------------------------------------------------------------------------
# 메시지 자동전송 여부 클래스
# ----------------------------------------------------------------------------------------------------------------------
class MessageConfig(models.Model):
    """이벤트 메시지를 텔레그렘으로 전송할지 말지 여부 모델
        : 폰그룹 별로, 이벤트 종류마다 전송할지 말지"""
    # PhoneGroup = models.ForeignKey(PhoneGroup, null=True, on_delete=models.DO_NOTHING)
    eventFailure = models.BooleanField(default=True, verbose_name="전송실패") # 전송실패 이벤트
    eventLowThroughput = models.BooleanField(default=True, verbose_name="속도저하") # 속도저하 이벤트
    eventVoiceDrop = models.BooleanField(default=True, verbose_name="음성 콜 드랍") # 음성 콜 드랍 이벤트
    eventNR = models.BooleanField(default=True, verbose_name="LTE전환") # 5G->LTE 전환 이벤트
    evntOffZone = models.BooleanField(default=True, verbose_name="측정범위 벗어남") # 측정범위 벗어나는 이벤트
    eventStay = models.BooleanField(default=True, verbose_name="한 곳에 머뭄") # 측정콜 한군데 머무는 이벤트
    eventDuplication = models.BooleanField(default=True, verbose_name="중복측정") # 측정단말의 중복측정 이벤트
    START_F = models.BooleanField(default=True, verbose_name="최초시작") # 최초 측정시작 메시지
    START_M = models.BooleanField(default=True, verbose_name="지역시작") # 해당지역 측정시작 메시지
    MEASURING = models.BooleanField(default=True, verbose_name="주기보고") # 측정 주기보고 메시지
    END = models.BooleanField(default=True, verbose_name="측정종료") # 측정종료 메시지
    END_LAST = models.BooleanField(default=True, verbose_name="최종종료") # 마지막 단말 측정종료 메시지
    
    class Meta:
        verbose_name = ("메시지 자동전송 설정")
        verbose_name_plural = ("메시지 자동전송 설정")
