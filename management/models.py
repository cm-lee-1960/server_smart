
from datetime import datetime
from django.db import models

###################################################################################################
# 환경설정 관리 관련 클래스
# - 모폴러지, 전송실패 기준, 속도저하 기준, 금일 측정조, 센터정보
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 센터정보 클래스
# -------------------------------------------------------------------------------------------------
class Center(models.Model):
    centerName = models.CharField(max_length=100, verbose_name="센터명")
    channelId = models.CharField(max_length=25, verbose_name="채널ID")
    permissionLevel = models.IntegerField(default=1, verbose_name="권한레벨")
    active = models.BooleanField(default=True, verbose_name="상태")
    class Meta:
        verbose_name = ('센터정보')
        verbose_name_plural = ('센터정보')

    def __str__(self):
        return self.centerName

# -------------------------------------------------------------------------------------------------
# 모폴러지 정보관리 클래스
# 측정 데이터에서 넘어오는 모폴로지 정보를 기준으로 재정의
# MessureCallData.userinfo2 --> Morphology.morphology : 맵핑정보 관리
# -------------------------------------------------------------------------------------------------
class Morphology(models.Model):
    MORPHOLOGY_CHOICES = {('행정동','행정동'), ('인빌딩', '인빌딩'), ('테마','테마'), ('취약지구', '취약지구'), \
                            ('커버리지','커버리지')}
    WORDSCOND_CHOICES = {('시작단어','시작단어'), ('포함단어','포함단어')}

    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    words = models.CharField(max_length=200, null=True, blank=True, verbose_name="단어") # 모폴로지 판단 컬럼2 : 특정 단어 포함
    wordsCond = models.CharField(max_length=20, null=True, blank=True, choices=WORDSCOND_CHOICES, verbose_name='조건')
    morphology = models.CharField(max_length=100, null=True, blank=True, choices=MORPHOLOGY_CHOICES,\
        verbose_name='모폴러지')
    manage = models.BooleanField(default=False, verbose_name='관리대상')  # 관리대상 여부
    class Meta:
        verbose_name = ('모폴러지')
        verbose_name_plural = ('모폴러지')

# -------------------------------------------------------------------------------------------------
# 전송실패(Send Failure) 기준관리 클래스
# -------------------------------------------------------------------------------------------------
class SendFailure(models.Model):
    AREAIND__CHOICES = {('NORM','보통지역'), ('WEEK', '취약지역')}
    NETWORKID_CHOICES = {('5G','5G'), ('LTE','LTE'), ('3G','3G'), ('WiFi','WiFi')}
    DATATYPE_CHOICES = {('DL','DL'), ('UL','UL')}

    areaInd = models.CharField(max_length=10, choices=AREAIND__CHOICES, verbose_name='지역구분')
    networkId = models.CharField(max_length=10, null=True, blank=True, choices=NETWORKID_CHOICES, verbose_name='단말유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    dataType = models.CharField(max_length=10, choices=DATATYPE_CHOICES, verbose_name='데이터유형') # 데이터유형(DL, UL)
    bandwidth = models.FloatField(null=True, default=0.0, verbose_name='속도')

    class Meta:
        verbose_name = ('전송실패 기준')
        verbose_name_plural = ('전송실패 기준')

# -------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 기준관리 클래스
# -------------------------------------------------------------------------------------------------
class LowThroughput(models.Model):
    AREAIND__CHOICES = {('NORM','보통지역'), ('WEEK', '취약지역')}
    NETWORKID_CHOICES = {('5G','5G'), ('LTE','LTE'), ('3G','3G'), ('WiFi','WiFi')}
    DATATYPE_CHOICES = {('DL','DL'), ('UL','UL')}

    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    areaInd = models.CharField(max_length=10, choices=AREAIND__CHOICES, verbose_name='지역구분')
    networkId = models.CharField(max_length=10, null=True, blank=True, choices=NETWORKID_CHOICES, verbose_name='단말유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    dataType = models.CharField(max_length=10, choices=DATATYPE_CHOICES, verbose_name='데이터유형') # 데이터유형(DL, UL)
    bandwidth = models.FloatField(null=True, default=0.0, verbose_name='속도')

    class Meta:
        verbose_name = ('속도저하 기준')
        verbose_name_plural = ('속도저하 기준')


# -------------------------------------------------------------------------------------------------
# 금일측정조 데이터
# -------------------------------------------------------------------------------------------------
class MeasureingTeam(models.Model):
    center = models.ForeignKey(Center, on_delete=models.DO_NOTHING, verbose_name="센터")
    measdate = models.DateField(default=datetime.now, verbose_name="측정일자", help_text="측정일자를 반드시 입력해야 합니다.")
    message = models.TextField(verbose_name="금일 측정조")

    class Meta:
        verbose_name = "금일 측정조"
        verbose_name_plural = "금일 측정조"


