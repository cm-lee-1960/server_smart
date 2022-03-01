from django.db import models

###################################################################################################
# 모폴러지 정보관리 클래스
# 측정 데이터에서 넘어오는 모폴로지 정보를 기준으로 재정의
# MessureCallData.userinfo2 --> Morphology.morphology : 맵핑정보 관리
###################################################################################################
class Morphology(models.Model):
    MORPHOLOGY_CHOICES = {('행정동','행정동'), ('인빌딩', '인빌딩'), ('테마','테마'), ('취약지구', '취약지구'), \
                            ('커버리지','커버리지')}

    userInfo2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='모폴러지(측정데이터)') # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    morphology = models.CharField(max_length=100, null=True, blank=True, choices=MORPHOLOGY_CHOICES,\
        verbose_name='모폴러지')
    class Meta:
        verbose_name = ('모폴러지')
        verbose_name_plural = ('모폴러지')

###################################################################################################
# 전송실패(Send Failure) 기준관리 클래스
###################################################################################################
class SendFailure(models.Model):
    AREAIND__CHOICES = {('NORM','보통지역'), ('WEEK', '취약지역')}
    NETWORKID_CHOICES = {('5G','5G'), ('LTE','LTE'), ('3G','3G'), ('WiFi','WiFi')}
    DATATYPE_CHOICES = {('DL','DL'), ('UP','UL')}

    areaInd = models.CharField(max_length=10, choices=AREAIND__CHOICES, verbose_name='지역구분')
    networkId = models.CharField(max_length=10, null=True, blank=True, choices=NETWORKID_CHOICES, verbose_name='단말유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    dataType = models.CharField(max_length=10, choices=DATATYPE_CHOICES, verbose_name='데이터유형') # 데이터유형(DL, UL)
    bandwidth = models.FloatField(null=True, default=0.0, verbose_name='속도')

    class Meta:
        verbose_name = ('전송실패 기준')
        verbose_name_plural = ('전송실패 기준')

###################################################################################################
# 속도저하(Low Throughput) 기준관리 클래스
###################################################################################################
class LowThroughput(models.Model):
    NETWORKID_CHOICES = {('5G','5G'), ('LTE','LTE'), ('3G','3G'), ('WiFi','WiFi')}
    DATATYPE_CHOICES = {('DL','DL'), ('UP','UL')}

    networkId = models.CharField(max_length=10, null=True, blank=True, choices=NETWORKID_CHOICES, verbose_name='단말유형') # 네트워크ID(5G, LTE, 3G, WiFi)
    dataType = models.CharField(max_length=10, choices=DATATYPE_CHOICES, verbose_name='데이터유형') # 데이터유형(DL, UL)
    bandwidth = models.FloatField(null=True, default=0.0, verbose_name='속도')

    class Meta:
        verbose_name = ('속도저하 기준')
        verbose_name_plural = ('속도저하 기준')

###################################################################################################
# 센터정보 클래스
###################################################################################################
class CenterInfo(models.Model):


    class Meta:
        verbose_name = ('센터정보')
        verbose_name_plural = ('센터정보')
