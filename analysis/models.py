from distutils.util import change_root
from django.utils import timezone
from django.db import models

from management.models import Center

###############################################################################################################################################################################
#3.16 측정대상 모델(수정완료)(클래스명 변경 필요, MeasPlan으로 변경예정)
###############################################################################################################################################################################
class MeasPlan(models.Model):
    planYear = models.IntegerField(null=True, default=0) # 계획년도 
    hjd5G = models.IntegerField(null=True, default=0) # 5G - 행정동
    dg5G = models.IntegerField(null=True, default=0) # - 다중이용시설/교통인프라
    cv5G = models.IntegerField(null=True, default=0) # - 커버리지
    
    bctLTE = models.IntegerField(null=True, default=0) # LTE - 대도시 
    mctLTE = models.IntegerField(null=True, default=0) # - 중소도시
    sctLTE = models.IntegerField(null=True, default=0) # - 농어촌
    ibLTE = models.IntegerField(null=True, default=0) # - 인빌딩
    tmLTE = models.IntegerField(null=True, default=0) # - 테마
    cvLTE = models.IntegerField(null=True, default=0) # - 커버리지
    
    syWiFi = models.IntegerField(null=True, default=0) # WiFi - 상용
    gbWiFi = models.IntegerField(null=True, default=0) # - 개방
    
    dsrWeak = models.IntegerField(null=True, default=0) # 취약지역 - 등산로
    yghrWeak = models.IntegerField(null=True, default=0) # - 
    yidsWeak = models.IntegerField(null=True, default=0)
    hadrWeak = models.IntegerField(null=True, default=0)
    total5G = models.IntegerField(null=True, default=0)
    totalLTE = models.IntegerField(null=True, default=0)
    totalWiFi = models.IntegerField(null=True, default=0)
    totalWeakArea = models.IntegerField(null=True, default=0)
    total = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name


###############################################################################################################################################################################
#3.16 측정완료대상 모델(수정완료)(클래스명 변경 필요, MeasPlan으로 변경예정)
###############################################################################################################################################################################
class MeasResult(models.Model):
    date = models.DateField(default=timezone.now, blank = True)
    measinfo = models.CharField(max_length=30, null=True, blank=True)
    networkId = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    area = models.CharField(max_length=30, null=True, blank=True)
    molph_level0 = models.CharField(max_length=30, null=True, blank=True)
    molph_level1 = models.CharField(max_length=30, null=True, blank=True)
   
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-date']



###############################################################################################################################################################################
#3.17 일일보고 추가 메세지 등록모델(수정중)
###############################################################################################################################################################################

class ReportMessage(models.Model):
    msg5G = models.CharField(max_length=50, null=True, blank=True)
    msgLTE = models.CharField(max_length=50, null=True, blank=True)
    msgWiFi = models.CharField(max_length=50, null=True, blank=True)
    msgWeak = models.CharField(max_length=50, null=True, blank=True)
    msg5Gafter = models.CharField(max_length=50, null=True, blank=True)
    msgLTEafter = models.CharField(max_length=50, null=True, blank=True)


###############################################################################################################################################################################
#3.17 일일보고 작년 측정 결과 등록 모델 5G(수정중)
###############################################################################################################################################################################

class MeasLastyear5G(models.Model):
    bctDL = models.FloatField(null=True, default=0)
    bctUL = models.FloatField(null=True, default=0)
    bctLTE = models.FloatField(null=True, default=0)
    bctsucc = models.FloatField(null=True, default=0)
    bctdelay = models.FloatField(null=True, default=0)

    mctDL = models.FloatField(null=True, default=0)
    mctUL = models.FloatField(null=True, default=0)
    mctLTE = models.FloatField(null=True, default=0)
    mctsucc = models.FloatField(null=True, default=0)
    mctdelay = models.FloatField(null=True, default=0)

    totalctDL = models.FloatField(null=True, default=0)
    totalctUL = models.FloatField(null=True, default=0)
    totalctLTE = models.FloatField(null=True, default=0)
    totalctsucc = models.FloatField(null=True, default=0)
    totalctdelay = models.FloatField(null=True, default=0)

    djDL = models.FloatField(null=True, default=0)
    djUL = models.FloatField(null=True, default=0)
    djLTE = models.FloatField(null=True, default=0)
    djsucc = models.FloatField(null=True, default=0)
    djdelay = models.FloatField(null=True, default=0)

    aptDL = models.FloatField(null=True, default=0)
    aptUL = models.FloatField(null=True, default=0)
    aptLTE = models.FloatField(null=True, default=0)
    aptsucc = models.FloatField(null=True, default=0)
    aptdelay = models.FloatField(null=True, default=0)

    univDL = models.FloatField(null=True, default=0)
    univUL = models.FloatField(null=True, default=0)
    univLTE = models.FloatField(null=True, default=0)
    univsucc = models.FloatField(null=True, default=0)
    univdelay = models.FloatField(null=True, default=0)

    trafficDL = models.FloatField(null=True, default=0)
    trafficUL = models.FloatField(null=True, default=0)
    trafficLTE = models.FloatField(null=True, default=0)
    trafficsucc = models.FloatField(null=True, default=0)
    trafficdelay = models.FloatField(null=True, default=0)

    areatotalDL = models.FloatField(null=True, default=0)
    areatotalUL = models.FloatField(null=True, default=0)
    areatotalLTE = models.FloatField(null=True, default=0)
    areatotalsucc = models.FloatField(null=True, default=0)
    areatotaldelay = models.FloatField(null=True, default=0)


###############################################################################################################################################################################
#3.17 일일보고 작년 측정 결과 등록 모델 LTE(수정중)
###############################################################################################################################################################################

class MeasLastyearLTE(models.Model):
    bctDL = models.FloatField(null=True, default=0)
    bctUL = models.FloatField(null=True, default=0)
    bctsucc = models.FloatField(null=True, default=0)
    bctdelay = models.FloatField(null=True, default=0)

    mctDL = models.FloatField(null=True, default=0)
    mctUL = models.FloatField(null=True, default=0)
    mctsucc = models.FloatField(null=True, default=0)
    mctdelay = models.FloatField(null=True, default=0)

    sctDL = models.FloatField(null=True, default=0)
    sctUL = models.FloatField(null=True, default=0)
    sctsucc = models.FloatField(null=True, default=0)
    sctdelay = models.FloatField(null=True, default=0)

    totalctDL = models.FloatField(null=True, default=0)
    totalctUL = models.FloatField(null=True, default=0)
    totalctsucc = models.FloatField(null=True, default=0)
    totalctdelay = models.FloatField(null=True, default=0)

    ibDL = models.FloatField(null=True, default=0)
    ibUL = models.FloatField(null=True, default=0)
    ibsucc = models.FloatField(null=True, default=0)
    ibdelay = models.FloatField(null=True, default=0)

    tmDL = models.FloatField(null=True, default=0)
    tmUL = models.FloatField(null=True, default=0)
    tmsucc = models.FloatField(null=True, default=0)
    tmdelay = models.FloatField(null=True, default=0)

    areatotalDL = models.FloatField(null=True, default=0)
    areatotalUL = models.FloatField(null=True, default=0)
    areatotalsucc = models.FloatField(null=True, default=0)
    areatotaldelay = models.FloatField(null=True, default=0)
    
###############################################################################################################################################################################
#3.28 이창민 임시 모델 생성
###############################################################################################################################################################################
class imsiweb(models.Model):
    Center = models.CharField(max_length=30, null=True, blank=True)
    group = models.CharField(max_length=30, null=True, blank=True)
    phonenum = models.CharField(max_length=30, null=True, blank=True)
    userinfo1 = models.CharField(max_length=30, null=True, blank=True)
    mor = models.CharField(max_length=30, null=True, blank=True)
    network = models.CharField(max_length=30, null=True, blank=True)
    DL_Call = models.IntegerField(null=True, blank=True)
    DL_TH = models.FloatField(null=True, blank=True)
    UL_Call = models.IntegerField(null=True, blank=True)
    UL_TH = models.FloatField(null=True, blank=True)
    changelte = models.FloatField(null=True, blank=True)
    event_num = models.IntegerField(null=True, blank=True)
    meastime_last = models.DateField(default=timezone.now, blank = True)
    active = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return self.Center
    class Meta:
        ordering = ['-active']