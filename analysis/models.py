from distutils.util import change_root
from django.utils import timezone
from django.db import models

from management.models import Center

###############################################################################################################################################################################
#04.20 일일보고 사후측정 데이터
###############################################################################################################################################################################

class PostMeasure5G(models.Model):
    #작년결과
    lasttotal = models.FloatField(null=True, default=0)
    lastseoul = models.FloatField(null=True, default=0)
    lastincheon = models.FloatField(null=True, default=0)
    lastulsan = models.FloatField(null=True, default=0)
    lastdaegu = models.FloatField(null=True, default=0)
    lastgwangju = models.FloatField(null=True, default=0)
    lastdaejun = models.FloatField(null=True, default=0)
    lastgyunggi = models.FloatField(null=True, default=0)
    lastgyungbuk = models.FloatField(null=True, default=0)
    lastjunnam = models.FloatField(null=True, default=0)
    lastjunbuk = models.FloatField(null=True, default=0)
    lastchungnam = models.FloatField(null=True, default=0)
    lastchungbuk = models.FloatField(null=True, default=0)
    lastsejong = models.FloatField(null=True, default=0)
    #KT 본 종합 결과
    kttotaltotal = models.FloatField(null=True, default=0)
    kttotalseoul = models.FloatField(null=True, default=0)
    kttotalincheon = models.FloatField(null=True, default=0)
    kttotalulsan = models.FloatField(null=True, default=0)
    kttotaldaegu = models.FloatField(null=True, default=0)
    kttotalgwangju = models.FloatField(null=True, default=0)
    kttotaldaejun = models.FloatField(null=True, default=0)
    kttotalgyunggi = models.FloatField(null=True, default=0)
    kttotalgyungbuk = models.FloatField(null=True, default=0)
    kttotaljunnam = models.FloatField(null=True, default=0)
    kttotaljunbuk = models.FloatField(null=True, default=0)
    kttotalchungnam = models.FloatField(null=True, default=0)
    kttotalchungbuk = models.FloatField(null=True, default=0)
    kttotalsejong = models.FloatField(null=True, default=0)
    #KT 사후 종합 결과
    kttotalposttotal = models.FloatField(null=True, default=0)
    kttotalpostseoul = models.FloatField(null=True, default=0)
    kttotalpostincheon = models.FloatField(null=True, default=0)
    kttotalpostulsan = models.FloatField(null=True, default=0)
    kttotalpostdaegu = models.FloatField(null=True, default=0)
    kttotalpostgwangju = models.FloatField(null=True, default=0)
    kttotalpostdaejun = models.FloatField(null=True, default=0)
    kttotalpostgyunggi = models.FloatField(null=True, default=0)
    kttotalpostgyungbuk = models.FloatField(null=True, default=0)
    kttotalpostjunnam = models.FloatField(null=True, default=0)
    kttotalpostjunbuk = models.FloatField(null=True, default=0)
    kttotalpostchungnam = models.FloatField(null=True, default=0)
    kttotalpostchungbuk = models.FloatField(null=True, default=0)
    kttotalpostsejong = models.FloatField(null=True, default=0)
    #S사 사후 종합 결과
    skttotalposttotal = models.FloatField(null=True, default=0)
    skttotalpostseoul = models.FloatField(null=True, default=0)
    skttotalpostincheon = models.FloatField(null=True, default=0)
    skttotalpostulsan = models.FloatField(null=True, default=0)
    skttotalpostdaegu = models.FloatField(null=True, default=0)
    skttotalpostgwangju = models.FloatField(null=True, default=0)
    skttotalpostdaejun = models.FloatField(null=True, default=0)
    skttotalpostgyunggi = models.FloatField(null=True, default=0)
    skttotalpostgyungbuk = models.FloatField(null=True, default=0)
    skttotalpostjunnam = models.FloatField(null=True, default=0)
    skttotalpostjunbuk = models.FloatField(null=True, default=0)
    skttotalpostchungnam = models.FloatField(null=True, default=0)
    skttotalpostchungbuk = models.FloatField(null=True, default=0)
    skttotalpostsejong = models.FloatField(null=True, default=0)
    #L사 사후 종합 결과
    lgtotalposttotal = models.FloatField(null=True, default=0)
    lgtotalpostseoul = models.FloatField(null=True, default=0)
    lgtotalpostincheon = models.FloatField(null=True, default=0)
    lgtotalpostulsan = models.FloatField(null=True, default=0)
    lgtotalpostdaegu = models.FloatField(null=True, default=0)
    lgtotalpostgwangju = models.FloatField(null=True, default=0)
    lgtotalpostdaejun = models.FloatField(null=True, default=0)
    lgtotalpostgyunggi = models.FloatField(null=True, default=0)
    lgtotalpostgyungbuk = models.FloatField(null=True, default=0)
    lgtotalpostjunnam = models.FloatField(null=True, default=0)
    lgtotalpostjunbuk = models.FloatField(null=True, default=0)
    lgtotalpostchungnam = models.FloatField(null=True, default=0)
    lgtotalpostchungbuk = models.FloatField(null=True, default=0)
    lgtotalpostsejong = models.FloatField(null=True, default=0)
    #KT 본 행정동 결과
    kthjdtotal = models.FloatField(null=True, default=0)
    kthjdseoul = models.FloatField(null=True, default=0)
    kthjdincheon = models.FloatField(null=True, default=0)
    kthjdulsan = models.FloatField(null=True, default=0)
    kthjddaegu = models.FloatField(null=True, default=0)
    kthjdgwangju = models.FloatField(null=True, default=0)
    kthjddaejun = models.FloatField(null=True, default=0)
    kthjdgyunggi = models.FloatField(null=True, default=0)
    kthjdgyungbuk = models.FloatField(null=True, default=0)
    kthjdjunnam = models.FloatField(null=True, default=0)
    kthjdjunbuk = models.FloatField(null=True, default=0)
    kthjdchungnam = models.FloatField(null=True, default=0)
    kthjdchungbuk = models.FloatField(null=True, default=0)
    kthjdsejong = models.FloatField(null=True, default=0)
    #KT 사후 행정동 결과
    kthjdposttotal = models.FloatField(null=True, default=0)
    kthjdpostseoul = models.FloatField(null=True, default=0)
    kthjdpostincheon = models.FloatField(null=True, default=0)
    kthjdpostulsan = models.FloatField(null=True, default=0)
    kthjdpostdaegu = models.FloatField(null=True, default=0)
    kthjdpostgwangju = models.FloatField(null=True, default=0)
    kthjdpostdaejun = models.FloatField(null=True, default=0)
    kthjdpostgyunggi = models.FloatField(null=True, default=0)
    kthjdpostgyungbuk = models.FloatField(null=True, default=0)
    kthjdpostjunnam = models.FloatField(null=True, default=0)
    kthjdpostjunbuk = models.FloatField(null=True, default=0)
    kthjdpostchungnam = models.FloatField(null=True, default=0)
    kthjdpostchungbuk = models.FloatField(null=True, default=0)
    kthjdpostsejong = models.FloatField(null=True, default=0)
    #S사 사후 행정동 결과
    skthjdposttotal = models.FloatField(null=True, default=0)
    skthjdpostseoul = models.FloatField(null=True, default=0)
    skthjdpostincheon = models.FloatField(null=True, default=0)
    skthjdpostulsan = models.FloatField(null=True, default=0)
    skthjdpostdaegu = models.FloatField(null=True, default=0)
    skthjdpostgwangju = models.FloatField(null=True, default=0)
    skthjdpostdaejun = models.FloatField(null=True, default=0)
    skthjdpostgyunggi = models.FloatField(null=True, default=0)
    skthjdpostgyungbuk = models.FloatField(null=True, default=0)
    skthjdpostjunnam = models.FloatField(null=True, default=0)
    skthjdpostjunbuk = models.FloatField(null=True, default=0)
    skthjdpostchungnam = models.FloatField(null=True, default=0)
    skthjdpostchungbuk = models.FloatField(null=True, default=0)
    skthjdpostsejong = models.FloatField(null=True, default=0)
    #L사 사후 행정동 결과
    lghjdposttotal = models.FloatField(null=True, default=0)
    lghjdpostseoul = models.FloatField(null=True, default=0)
    lghjdpostincheon = models.FloatField(null=True, default=0)
    lghjdpostulsan = models.FloatField(null=True, default=0)
    lghjdpostdaegu = models.FloatField(null=True, default=0)
    lghjdpostgwangju = models.FloatField(null=True, default=0)
    lghjdpostdaejun = models.FloatField(null=True, default=0)
    lghjdpostgyunggi = models.FloatField(null=True, default=0)
    lghjdpostgyungbuk = models.FloatField(null=True, default=0)
    lghjdpostjunnam = models.FloatField(null=True, default=0)
    lghjdpostjunbuk = models.FloatField(null=True, default=0)
    lghjdpostchungnam = models.FloatField(null=True, default=0)
    lghjdpostchungbuk = models.FloatField(null=True, default=0)
    lghjdpostsejong = models.FloatField(null=True, default=0)
    #KT 본 다중이용시설/교통/아파트/대학 결과
    ktsidetotal = models.FloatField(null=True, default=0)
    ktsideseoul = models.FloatField(null=True, default=0)
    ktsideincheon = models.FloatField(null=True, default=0)
    ktsideulsan = models.FloatField(null=True, default=0)
    ktsidedaegu = models.FloatField(null=True, default=0)
    ktsidegwangju = models.FloatField(null=True, default=0)
    ktsidedaejun = models.FloatField(null=True, default=0)
    ktsidegyunggi = models.FloatField(null=True, default=0)
    ktsidegyungbuk = models.FloatField(null=True, default=0)
    ktsidejunnam = models.FloatField(null=True, default=0)
    ktsidejunbuk = models.FloatField(null=True, default=0)
    ktsidechungnam = models.FloatField(null=True, default=0)
    ktsidechungbuk = models.FloatField(null=True, default=0)
    ktsidesejong = models.FloatField(null=True, default=0)
    #KT 사후 다중이용시설/교통/아파트/대학 결과
    ktsideposttotal = models.FloatField(null=True, default=0)
    ktsidepostseoul = models.FloatField(null=True, default=0)
    ktsidepostincheon = models.FloatField(null=True, default=0)
    ktsidepostulsan = models.FloatField(null=True, default=0)
    ktsidepostdaegu = models.FloatField(null=True, default=0)
    ktsidepostgwangju = models.FloatField(null=True, default=0)
    ktsidepostdaejun = models.FloatField(null=True, default=0)
    ktsidepostgyunggi = models.FloatField(null=True, default=0)
    ktsidepostgyungbuk = models.FloatField(null=True, default=0)
    ktsidepostjunnam = models.FloatField(null=True, default=0)
    ktsidepostjunbuk = models.FloatField(null=True, default=0)
    ktsidepostchungnam = models.FloatField(null=True, default=0)
    ktsidepostchungbuk = models.FloatField(null=True, default=0)
    ktsidepostsejong = models.FloatField(null=True, default=0)
    #S사 사후 다중이용시설/교통/아파트/대학 결과
    sktsideposttotal = models.FloatField(null=True, default=0)
    sktsidepostseoul = models.FloatField(null=True, default=0)
    sktsidepostincheon = models.FloatField(null=True, default=0)
    sktsidepostulsan = models.FloatField(null=True, default=0)
    sktsidepostdaegu = models.FloatField(null=True, default=0)
    sktsidepostgwangju = models.FloatField(null=True, default=0)
    sktsidepostdaejun = models.FloatField(null=True, default=0)
    sktsidepostgyunggi = models.FloatField(null=True, default=0)
    sktsidepostgyungbuk = models.FloatField(null=True, default=0)
    sktsidepostjunnam = models.FloatField(null=True, default=0)
    sktsidepostjunbuk = models.FloatField(null=True, default=0)
    sktsidepostchungnam = models.FloatField(null=True, default=0)
    sktsidepostchungbuk = models.FloatField(null=True, default=0)
    sktsidepostsejong = models.FloatField(null=True, default=0)
    #L사 사후 다중이용시설/교통/아파트/대학 결과
    lgsideposttotal = models.FloatField(null=True, default=0)
    lgsidepostseoul = models.FloatField(null=True, default=0)
    lgsidepostincheon = models.FloatField(null=True, default=0)
    lgsidepostulsan = models.FloatField(null=True, default=0)
    lgsidepostdaegu = models.FloatField(null=True, default=0)
    lgsidepostgwangju = models.FloatField(null=True, default=0)
    lgsidepostdaejun = models.FloatField(null=True, default=0)
    lgsidepostgyunggi = models.FloatField(null=True, default=0)
    lgsidepostgyungbuk = models.FloatField(null=True, default=0)
    lgsidepostjunnam = models.FloatField(null=True, default=0)
    lgsidepostjunbuk = models.FloatField(null=True, default=0)
    lgsidepostchungnam = models.FloatField(null=True, default=0)
    lgsidepostchungbuk = models.FloatField(null=True, default=0)
    lgsidepostsejong = models.FloatField(null=True, default=0)
    #KT 종합 순위
    ktranktotal = models.FloatField(null=True, default=0)
    ktrankseoul = models.FloatField(null=True, default=0)
    ktrankincheon = models.FloatField(null=True, default=0)
    ktrankulsan = models.FloatField(null=True, default=0)
    ktrankdaegu = models.FloatField(null=True, default=0)
    ktrankgwangju = models.FloatField(null=True, default=0)
    ktrankdaejun = models.FloatField(null=True, default=0)
    ktrankgyunggi = models.FloatField(null=True, default=0)
    ktrankgyungbuk = models.FloatField(null=True, default=0)
    ktrankjunnam = models.FloatField(null=True, default=0)
    ktrankjunbuk = models.FloatField(null=True, default=0)
    ktrankchungnam = models.FloatField(null=True, default=0)
    ktrankchungbuk = models.FloatField(null=True, default=0)
    ktranksejong = models.FloatField(null=True, default=0)
    #KT 행정동 순위
    ktrankhjdtotal = models.FloatField(null=True, default=0)
    ktrankhjdseoul = models.FloatField(null=True, default=0)
    ktrankhjdincheon = models.FloatField(null=True, default=0)
    ktrankhjdulsan = models.FloatField(null=True, default=0)
    ktrankhjddaegu = models.FloatField(null=True, default=0)
    ktrankhjdgwangju = models.FloatField(null=True, default=0)
    ktrankhjddaejun = models.FloatField(null=True, default=0)
    ktrankhjdgyunggi = models.FloatField(null=True, default=0)
    ktrankhjdgyungbuk = models.FloatField(null=True, default=0)
    ktrankhjdjunnam = models.FloatField(null=True, default=0)
    ktrankhjdjunbuk = models.FloatField(null=True, default=0)
    ktrankhjdchungnam = models.FloatField(null=True, default=0)
    ktrankhjdchungbuk = models.FloatField(null=True, default=0)
    ktrankhjdsejong = models.FloatField(null=True, default=0)
    #KT 다중이용시설/교통/아파트/대학 순위
    ktranksidetotal = models.FloatField(null=True, default=0)
    ktranksideseoul = models.FloatField(null=True, default=0)
    ktranksideincheon = models.FloatField(null=True, default=0)
    ktranksideulsan = models.FloatField(null=True, default=0)
    ktranksidedaegu = models.FloatField(null=True, default=0)
    ktranksidegwangju = models.FloatField(null=True, default=0)
    ktranksidedaejun = models.FloatField(null=True, default=0)
    ktranksidegyunggi = models.FloatField(null=True, default=0)
    ktranksidegyungbuk = models.FloatField(null=True, default=0)
    ktranksidejunnam = models.FloatField(null=True, default=0)
    ktranksidejunbuk = models.FloatField(null=True, default=0)
    ktranksidechungnam = models.FloatField(null=True, default=0)
    ktranksidechungbuk = models.FloatField(null=True, default=0)
    ktranksidesejong = models.FloatField(null=True, default=0)
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
#4.25 일일보고 작년 측정 결과 등록 모델 WiFi(수정중)
###############################################################################################################################################################################

class MeasLastyearWiFi(models.Model):
    totalwifidl = models.FloatField(null=True, default=0)
    sywifidl = models.FloatField(null=True, default=0)
    gbwifidl = models.FloatField(null=True, default=0)
    totalwifiul = models.FloatField(null=True, default=0)
    sywifiul = models.FloatField(null=True, default=0)
    gbwifiul = models.FloatField(null=True, default=0)  

###############################################################################################################################################################################
#3.28 이창민 임시 모델 생성
###############################################################################################################################################################################
# class imsiweb(models.Model):
#     Center = models.CharField(max_length=30, null=True, blank=True)
#     group = models.CharField(max_length=30, null=True, blank=True)
#     phonenum = models.CharField(max_length=30, null=True, blank=True)
#     userinfo1 = models.CharField(max_length=30, null=True, blank=True)
#     mor = models.CharField(max_length=30, null=True, blank=True)
#     network = models.CharField(max_length=30, null=True, blank=True)
#     DL_Call = models.IntegerField(null=True, blank=True)
#     DL_TH = models.FloatField(null=True, blank=True)
#     UL_Call = models.IntegerField(null=True, blank=True)
#     UL_TH = models.FloatField(null=True, blank=True)
#     changelte = models.FloatField(null=True, blank=True)
#     event_num = models.IntegerField(null=True, blank=True)
#     meastime_last = models.DateField(default=timezone.now, blank = True)
#     active = models.CharField(max_length=30, null=True, blank=True)
    
#     def __str__(self):
#         return self.Center
#     class Meta:
#         ordering = ['-active']