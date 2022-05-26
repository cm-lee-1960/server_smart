from distutils.util import change_root

from django.db import models
from monitor.models import *

from management.models import Center

from operator import itemgetter
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime, timedelta, timezone
import random

from message.tele_msg import TelegramBot  # 텔레그램 메시지 전송 클래스
from message.xmcs_msg import send_sms  # 2022.03.04 크로샷 메시지 전송 함수 호출

###############################################################################################################################################################################
#04.20 일일보고 사후측정 데이터
###############################################################################################################################################################################

class PostMeasure5G(models.Model):
    #새로만들기5G
    district = models.CharField(null=True,  blank=True,max_length=10)
    number = models.IntegerField(null=True, default=0)
    lasttotal5g = models.IntegerField(null=True, default=0)
    kttotaltotal5g = models.IntegerField(null=True, default=0)
    kttotalposttotal5g = models.IntegerField(null=True, default=0)
    skttotalposttotal5g = models.IntegerField(null=True, default=0)
    lgtotalposttotal5g =models.IntegerField(null=True, default=0)
     #KT 종합 순위
    ktranktotal5g = models.IntegerField(null=True, default=0)
    kthjdtotal5g = models.IntegerField(null=True, default=0)
    kthjdposttotal5g = models.IntegerField(null=True, default=0)
    skthjdposttotal5g = models.IntegerField(null=True, default=0)
    lghjdposttotal5g = models.IntegerField(null=True, default=0)
    #KT 행정동 순위
    ktrankhjdtotal5g =models.IntegerField(null=True, default=0)
    #KT 본 다중이용시설/교통/아파트/대학 결과
    ktsidetotal5g = models.IntegerField(null=True, default=0)
    #KT 사후 다중이용시설/교통/아파트/대학 결과
    ktsideposttotal5g = models.IntegerField(null=True, default=0)
    #S사 사후 다중이용시설/교통/아파트/대학 결과
    sktsideposttotal5g = models.IntegerField(null=True, default=0)
    #L사 사후 다중이용시설/교통/아파트/대학 결과
    lgsideposttotal5g = models.IntegerField(null=True, default=0)
    #KT 다중이용시설/교통/아파트/대학 순위
    ktranksidetotal5g = models.IntegerField(null=True, default=0)
  
class PostMeasureLTE(models.Model):    
    #새로만들기LTE
    district = models.CharField(null=True,  blank=True,max_length=10)
    number = models.IntegerField(null=True, default=0)
    lasttotallte = models.IntegerField(null=True, default=0)
    ktdllte = models.IntegerField(null=True, default=0)
    ktpostdllte = models.IntegerField(null=True, default=0)
    sktpostdllte = models.IntegerField(null=True, default=0)
    lgpostdllte =models.IntegerField(null=True, default=0)
    ktullte = models.IntegerField(null=True, default=0)
    ktpostullte = models.IntegerField(null=True, default=0)
    sktpostullte = models.IntegerField(null=True, default=0)
    lgpostullte = models.IntegerField(null=True, default=0)
   
###############################################################################################################################################################################
#3.16 측정대상 모델(수정완료)(클래스명 변경 필요, MeasPlan으로 변경예정)
###############################################################################################################################################################################
class MeasPlan(models.Model):
    planYear = models.IntegerField(null=True, default=0) # 계획년도 
    nsahjd5G = models.IntegerField(null=True, default=0) # 5G NSA - 행정동
    nsadg5G = models.IntegerField(null=True, default=0) # - 5G NSA 다중이용시설/교통인프라
    sa5G = models.IntegerField(null=True, default=0) #SA  5G
    public5G = models.IntegerField(null=True, default=0) # 공동망
    cvdg5G = models.IntegerField(null=True, default=0) # - 커버리지 다중시설 교통인프라
    cvjs5G = models.IntegerField(null=True, default=0) # 커버리지 중소시설
    
    bctLTE = models.IntegerField(null=True, default=0) # LTE - 대도시 
    mctLTE = models.IntegerField(null=True, default=0) # - 중소도시
    sctLTE = models.IntegerField(null=True, default=0) # - 농어촌
    ibLTE = models.IntegerField(null=True, default=0) # - 인빌딩
    tmLTE = models.IntegerField(null=True, default=0) # - 테마
    cvLTE = models.IntegerField(null=True, default=0) # - 커버리지
    
    syWiFi = models.IntegerField(null=True, default=0) # WiFi - 상용
    gbWiFi = models.IntegerField(null=True, default=0) # - 개방
    publicWiFi = models.IntegerField(null=True, default=0) # 공공
    
    dsrWeak = models.IntegerField(null=True, default=0) # 취약지역 - 등산로
    yghrWeak = models.IntegerField(null=True, default=0) # - 여객항로
    yidsWeak = models.IntegerField(null=True, default=0) # 유인도서
    hadrWeak = models.IntegerField(null=True, default=0) # 해안도로
    
    totalnsa5G = models.IntegerField(null=True, default=0)
    total5G = models.IntegerField(null=True, default=0)
    totalLTE = models.IntegerField(null=True, default=0)
    totalWiFi = models.IntegerField(null=True, default=0)
    totalWeakArea = models.IntegerField(null=True, default=0)
    total = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name


# ###############################################################################################################################################################################
# #3.16 측정완료대상 모델(수정완료)(클래스명 변경 필요, MeasPlan으로 변경예정)
# ###############################################################################################################################################################################
# class MeasResult(models.Model):
#     date = models.DateField(default=timezone.now, blank = True)
#     measinfo = models.CharField(max_length=30, null=True, blank=True)
#     networkId = models.CharField(max_length=30, null=True, blank=True)
#     district = models.CharField(max_length=30, null=True, blank=True)
#     area = models.CharField(max_length=30, null=True, blank=True)
#     molph_level0 = models.CharField(max_length=30, null=True, blank=True)
#     molph_level1 = models.CharField(max_length=30, null=True, blank=True)
   
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ['-date']



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

########################################################################################################################
# 허재 측정마감 테스트 (모델가져오기)
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 생성된 메시지 타입에 따라서 크로샷 또는 텔레그램으로 전송하는 함수
# ----------------------------------------------------------------------------------------------------------------------
# def send_message(sender, **kwargs):
def send_message_hj(sender, instance, created, **kwargs):
    """ 생성된 메시지를 크로샷 또는 텔레그램으로 전송하는 함수
        - 파라미터
          . sender: 메시지 모델 클래스
          . instance: 메시지 객체 (생성된 레코드 하나 데이터)
          . created: 신규생성 여부(True or False)
          . kwargs: 키워트 파라미터
        - 반환값: 없음
    """
    
    if created:
        if instance.phoneGroup != None:  # 커버리지의 경우 PhoneGroup 미존재
            a = Phone.objects.filter(phoneGroup = instance.phoneGroup, userInfo1 = instance.userInfo1, measdate = instance.measdate)
            b = PhoneGroup.objects.filter(id= instance.phoneGroup_id)
            c = MorphologyDetail.objects.filter(id = b[0].morphologyDetail_id)

            if instance.total_count == 0:  ## lte전환율 계산
                lte_percent = 0
            else:
                lte_percent = (instance.dl_nr_percent * instance.dl_nr_count) + (instance.ul_nr_percent * instance.ul_nr_count) / instance.total_count # 5G->LTE 전환 전환율(ul)

          
            qs = LastMeasDayClose.objects.create(
                        measdate =  instance.measdate,  # 측정일자(예: 20211101)
                        phoneGroup = instance.phoneGroup_id,  # 단말그룹
                        
                        userInfo1 = instance.userInfo1,
                        networkId = instance.networkId,  # 네트워크ID(5G, LTE, 3G, WiFi)
                        center = instance.center.centerName,
                        
                        morphology = instance.morphology.morphology,
                        
                        downloadBandwidth = instance.downloadBandwidth,  # DL속도 (초단위 데이터 평균)
                        uploadBandwidth = instance.uploadBandwidth,  # UP속도 (초단위 데이터 평균)
                        lte_percent = lte_percent,  # 5G->LTE 전환 전환율(ul)
                        connect_time = instance.connect_time,  # 접속시간
                        udpJitter = instance.udpJitter,  # 지연시간
                        success_rate = instance.success_rate,  # 전송성공율
                        siDo = a[0].siDo,
                        guGun = a[0].guGun,
                        addressDetail = a[0].addressDetail,
                        district = a[0].siDo,

                        mopho_id = b[0].morphologyDetail_id,
            )
            if c.exists():
                qs.nettype, qs.mopho, qs.detailadd, qs.subadd = c[0].network_type, c[0].main_class, c[0].middle_class, c[0].sub_class
                qs.save()
        else:  # PhoneGroup이 None인 커버리지의 경우
            pass
       
    else:
        # 메시지가 업데이트 되었을 때는 아무런 처리를 하지 않는다.
        pass



########################################################################################################################
# 허재 측정마감 테스트
########################################################################################################################

class LastMeasDayClose(models.Model):
    """측정마감 클래스"""
    measdate = models.CharField(max_length=10, verbose_name='측정일자')  # 측정일자(예: 20211101)
    phoneGroup = models.IntegerField(verbose_name='단말그룹')  # 단말그룹
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    # userInfo2 = models.CharField(max_length=100, verbose_name="측정자 입력값2")
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name="유형")  # 네트워크ID(5G, LTE, 3G, WiFi)
    center = models.CharField(max_length=100,null=True, blank=True, verbose_name="센터")
    morphology = models.CharField(max_length=100,null=True, blank=True, verbose_name="모풀로지")
    downloadBandwidth = models.FloatField(null=True, blank=True, verbose_name='DL')  # DL속도 (초단위 데이터 평균)
    uploadBandwidth = models.FloatField(null=True, blank=True, verbose_name='UL')  # UP속도 (초단위 데이터 평균)
    # dl_count = models.IntegerField(null=True, default=0, verbose_name='DL콜카운트')  # 다운로드 콜수
    # ul_count = models.IntegerField(null=True, default=0, verbose_name='UL콜카운트')  # 업로드 콜수
    # dl_nr_count = models.IntegerField(null=True, default=0, verbose_name='DL NR 콜카운트')  # 5G->NR 전환 콜수
    # ul_nr_count = models.IntegerField(null=True, default=0, verbose_name='UL NR 콜카운트')  # 5G->NR 전환 콜수
    # dl_nr_percent = models.FloatField(null=True, default=0.0, verbose_name='DL LTE전환율')  # 5G->NR 전환 전환율(dl)
    # ul_nr_percent = models.FloatField(null=True, default=0.0, verbose_name='UL LTE전환율')  # 5G->NR 전환 전환율(ul)
    # total_count = models.IntegerField(null=True, default=0)  # 총 콜수
    lte_percent = models.FloatField(null=True, default=0.0, verbose_name='LTE전환율') # 5G->LTE 전환 전환율(ul)
    connect_time = models.FloatField(null=True, default=0.0, verbose_name='접속시간')  # 접속시간
    udpJitter = models.FloatField(null=True, default=0.0, verbose_name='지연시간')  # 지연시간
    success_rate = models.FloatField(null=True, default=0.0, verbose_name='전송성공율')  # 전송성공율
    siDo = models.CharField(max_length=100, null=True, blank=True, verbose_name="시,도", default='')  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True, verbose_name="군,구", default='')  # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True, verbose_name="상세주소", default='')  # 주소상세
    district = models.CharField(max_length=100, null=True, blank=True,verbose_name="지역",default='')
    mopho = models.CharField(max_length=100, null=True, blank=True,verbose_name="모폴로지",default='')
    nettype = models.CharField(max_length=100, null=True, blank=True,verbose_name="네트타입",default='')
    plus = models.CharField(max_length=100, null=True, blank=True,verbose_name="추가사항",default='')
    postktdl = models.FloatField(null=True, default=0)
    postsktdl= models.FloatField(null=True, default=0)
    postlgdl= models.FloatField(null=True, default=0)
    postktul= models.FloatField(null=True, default=0)
    postsktul= models.FloatField(null=True, default=0)
    postlgul= models.FloatField(null=True, default=0)
    detailadd = models.CharField(max_length=100, null=True, blank=True,default='')
    subadd = models.CharField(max_length=100, null=True, blank=True,default='')
    mopho_id = models.IntegerField(null=True, blank=True,verbose_name='모폴로지아이디',default='999')
    class Meta:
        ordering = ['-measdate']

post_save.connect(send_message_hj, sender=MeasuringDayClose)



