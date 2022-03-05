from django.db import models

###################################################################################################
# 모풀로지 정보관리 클래스
# 측정 데이터에서 넘어오는 모폴로지 정보를 기준으로 재정의
# MessureCallData.userinfo2 --> Morphology.morphology : 맵핑정보 관리
###################################################################################################
class Morphology(models.Model):
    MORPHOLOGY_CHOICES = {('행정동','행정동'), ('인빌딩', '인빌딩'), ('테마','테마'), ('취약지구', '취약지구'), \
                            ('커버리지','커버리지')}

    userInfo2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='모풀로지(측정데이터)') # 측정위치(행정동, 테마, 인빌딩, 커버리지)
    morphology = models.CharField(max_length=100, null=True, blank=True, choices=MORPHOLOGY_CHOICES,\
        verbose_name='모풀로지')
    class Meta:
        verbose_name = ('모풀로지')
        verbose_name_plural = ('모풀로지')


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


############################# 모폴로지 및 모폴로지 별 DL/UL 조건 세팅 (2.28, 박재찬) ###############################
class morph_settings(models.Model):
  '''모폴로지 DB(사용자 입력 가능)'''
  # 모폴로지 4종 : 테마/인빌딩/행정동/취약지구
  # 폰그룹 별로 모폴로지 할당 가능?
  MORPHOLOGY_CHOICES = {('행정동','행정동'), ('인빌딩', '인빌딩'), ('테마','테마'), ('취약지구', '취약지구'), ('커버리지','커버리지')}
  
  morph = models.CharField(max_length=100, null=True, blank=True, choices=MORPHOLOGY_CHOICES, verbose_name='모풀로지')
  fvg_dl_criteria = models.FloatField(null=True, blank=True, verbose_name="5G DL 이벤트 조건") # 5g dl lowthroughput 조건
  fvg_ul_criteria = models.FloatField(null=True, blank=True, verbose_name="5G UL 이벤트 조건") # 5g ul lowthroughput 조건
  lte_dl_criteria = models.FloatField(null=True, blank=True, verbose_name="LTE UL 이벤트 조건") # lte dl lowthroughput 조건
  lte_ul_criteria = models.FloatField(null=True, blank=True, verbose_name="LTE UL 이벤트 조건") # lte ul lowthroughput 조건
  thg_dl_criteria = models.FloatField(null=True, blank=True, verbose_name="3G UL 이벤트 조건") # 3g dl lowthroughput 조건
  thg_ul_criteria = models.FloatField(null=True, blank=True, verbose_name="3G UL 이벤트 조건") # 3g ul lowthroughput 조건
  wifi_dl_criteria = models.FloatField(null=True, blank=True, verbose_name="WiFi UL 이벤트 조건") # WiFi ul lowthroughput 조건
  wifi_ul_criteria = models.FloatField(null=True, blank=True, verbose_name="WiFi UL 이벤트 조건") # WiFi ul lowthroughput 조건
  
  morph_startswith = models.CharField(max_length=100, null=True, blank=True, verbose_name="모폴로지 조건(시작단어)") # 모폴로지 판단 컬럼1 : 시작단어
  morph_vulzone = models.CharField(max_length=500, null=True, blank=True, verbose_name="모폴로지 조건(포함)") # 모폴로지 판단 컬럼2 : 특정 단어 포함(,로 구분) 취약지구만 사용
  #morph_include = models.CharField(max_length=100, null=True, blank=True) # 모폴로지 판단 컬럼2 : 포함단어
  #morph_si_cond = models.CharField(max_length=10, choices=startwith_include_choices, blank=True) # 모폴로지 판단 컬럼 조건 : or/and