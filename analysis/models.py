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
        a = Phone.objects.filter(phoneGroup_id = instance.phoneGroup_id, userInfo1 = instance.userInfo1, measdate = instance.measdate)
        print("a 만들어짐")
        # if a[0].morphology_id == 1:
        #                 mopo = "행정동"
        #                 if "특별시" in a[0].siDo or "광역시" in a[0].siDo:
        #                         address = "대도시"
        #                 elif a[0].guGun.endswith("읍") or  a[0].guGun.endswith("면"):
        #                         address = "농어촌"
        #                 else:
        #                         address = "중소도시"
        # elif a[0].morphology_id == 2:
        #                 mopo = "테마"
        #                 if "병원" in a[0].userInfo1:
        #                     mopo = "인빌딩"
        #                     address = "대형병원"
        #                 elif "백화점" in a[0].userInfo1:
        #                     mopo = "인빌딩"
        #                     address = "백화점"
        #                 elif "터미널" in a[0].userInfo1:
        #                     mopo = "인빌딩"
        #                     address = "터미널"
        #                 elif "역" in a[0].userInfo1:
        #                     mopo = "인빌딩"
        #                     address = "역사"
        #                 elif "공항" in a[0].userInfo1:
        #                     mopo = "인빌딩"
        #                     address = "공항" 
        #                 elif "대학" in a[0].userInfo1 or "학생" in a[0].userInfo1:
        #                     mopo = "테마"
        #                     address = "대학교"
        #                 elif "공원" in a[0].userInfo1:
        #                     mopo = "테마"
        #                     address = "놀이공원"
        #                 elif "거리" in a[0].userInfo1:
        #                     mopo = "테마"
        #                     address = "주요거리" 
        #                 else:
        #                     address = "수정필요"           
        # elif a[0].morphology_id == 3:
        #                 mopo = "인빌딩"
        # elif a[0].morphology_id== 4:
        #                 mopo = "커버리지"
        # elif a[0].morphology_id== 5 or a[0].userInfo2 == "L" or a[0].userInfo2 == "3":
        #                 mopo = "취약지역"
        #                 if a[0].userInfo1.endswith("도"):
        #                     address = "유인도서"
        #                 elif a[0].userInfo1.endswith("산"):
        #                     address = "등산로"
        #                 elif "해안도로" in a[0].userInfo1:
        #                     address = "해안도로"
        #                 elif "-" in a[0].userInfo1:
        #                     address = "여객항로"
        #                 else: 
        #                     address = "-"
        # else:
        #                 pass
        # # 와이파이
        # if a[0].networkId == "WiFi":
        #                 if "개" in a[0].userInfo2: 
        #                     mopo = "개방"
        #                 elif "상" in a[0].userInfo2:
        #                     mopo = "상용"
        #                 elif "공" in a[0].userInfo2:
        #                     mopo = "공공"    
        #                 else:
        #                     mopo = "-" 
        # else:
        #                 pass
        # if "서울" in a[0].siDo or "서울" in a[0].guGun:
        #                 district = "서울"
        # elif "인천" in a[0].siDo or "인천" in a[0].guGun:
        #                 district = "인천"
        # elif "울산" in a[0].siDo or "울산" in a[0].guGun:
        #                 district = "울산"
        # elif "대구" in a[0].siDo or "대구" in a[0].guGun:
        #                 district = "대구"
        # elif "광주" in a[0].siDo or "광주" in a[0].guGun:
        #                 district = "광주"
        # elif "대전" in a[0].siDo or "대전" in a[0].guGun:
        #                 district = "대전"
        # elif "경기" in a[0].siDo or "경기" in a[0].guGun:
        #                 district = "경기"
        # elif "경상북" in a[0].siDo or "경상북" in a[0].guGun:
        #                 district = "경북"
        # elif "경상남" in a[0].siDo or "경상남" in a[0].guGun:
        #                 district = "경남"
        # elif "전라남" in a[0].siDo or "전라남" in a[0].guGun:
        #                 district = "전남"
        # elif "전라북" in a[0].siDo or "전라북" in a[0].guGun:
        #                 district = "전북"
        # elif "충청남" in a[0].siDo or "충청남" in a[0].guGun:
        #                 district = "충남"
        # elif "충청북" in a[0].siDo or "충청북" in a[0].guGun:
        #                 district = "충북"
        # elif "세종" in a[0].siDo or "세종" in a[0].guGun:
        #                 district = "세종"
        # else:
        #                 district = "수도권"
        # print("나이거보고싶다.")
        LastMeasDayClose.objects.create(
                    measdate =  instance.measdate,  # 측정일자(예: 20211101)
                    phoneGroup = instance.phoneGroup_id,  # 단말그룹
                    
                    userInfo1 = instance.userInfo1,
                    networkId = instance.networkId,  # 네트워크ID(5G, LTE, 3G, WiFi)
                    center = instance.center,
                    
                    morphology = instance.morphology,
                    
                    downloadBandwidth = instance.downloadBandwidth,  # DL속도 (초단위 데이터 평균)
                    uploadBandwidth = instance.uploadBandwidth,  # UP속도 (초단위 데이터 평균)
                    lte_percent = (instance.dl_nr_percent * instance.dl_nr_count + instance.ul_nr_percent * instance.ul_nr_count) / instance.total_count, # 5G->LTE 전환 전환율(ul)
                    connect_time = instance.connect_time,  # 접속시간
                    udpJitter = instance.udpJitter,  # 지연시간
                    success_rate = instance.success_rate,  # 전송성공율
                    siDo = a[0].siDo,
                    guGun = a[0].guGun,
                    addressDetail = a[0].addressDetail,
                    district = a[0].siDo,
                    mopo = instance.morphology,
                    address = "",
                )
        print("성공성공 들어왔다.")
        # # 2) 크로샷으로 메시지를 전송한다.
        # if instance.sendType == 'XMCS' or instance.sendType == 'ALL':
        #     # 2022.03.04 - 크로샷 메시지 전송  --  node.js 파일 호출하여 전송
        #     # 현재 변수 전달(메시지/수신번호) 구현되어 있지 않아 /message/sms_broadcast.js에 설정된 내용/번호로만 전송
        #     # npm install request 명령어로 모듈 설치 후 사용 가능
        #     send_sms()
    else:
        # 메시지가 업데이트 되었을 때는 아무런 처리를 하지 않는다.
        print("안대따")
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
    address = models.CharField(max_length=100, null=True, blank=True,verbose_name="상세지역",default='')
    mopo = models.CharField(max_length=100, null=True, blank=True,verbose_name="모폴로지명",default='')
    plus = models.CharField(max_length=100, null=True, blank=True,verbose_name="추가사항",default='')
    postktdl = models.FloatField(null=True, default=0)
    postsktdl= models.FloatField(null=True, default=0)
    postlgdl= models.FloatField(null=True, default=0)
    postktul= models.FloatField(null=True, default=0)
    postsktul= models.FloatField(null=True, default=0)
    postlgul= models.FloatField(null=True, default=0)
    
    class Meta:
        ordering = ['-measdate']

post_save.connect(send_message_hj, sender=MeasuringDayClose)



########
#   # 측정마감 테스트################################################################
#             hj = TestDayClose.objects.filter(measdate=phoneGroup.measdate, phoneGroup=phoneGroup)
#             a = Phone.objects.filter(phoneGroup_id = phoneGroup.id, userInfo1 = phoneGroup.userInfo1, userInfo2 = phoneGroup.userInfo2, measdate = phoneGroup.measdate)
#             siDo = a[0].siDo
#             guGun = a[0].guGun
#             addressDetail = a[0].addressDetail
#             if a[0].morphology_id == 1:
#                 mopo = "행정동"
#                 if "특별시" in a[0].siDo or "광역시" in a[0].siDo:
#                         address = "대도시"
#                 elif a[0].guGun.endswith("읍") or  a[0].guGun.endswith("면"):
#                         address = "농어촌"
#                 else:
#                         address = "중소도시"
#             elif a[0].morphology_id == 2:
#                 mopo = "테마"
#                 if "병원" in a[0].userInfo1:
#                     mopo = "인빌딩"
#                     address = "대형병원"
#                 elif "백화점" in a[0].userInfo1:
#                     mopo = "인빌딩"
#                     address = "백화점"
#                 elif "터미널" in a[0].userInfo1:
#                     mopo = "인빌딩"
#                     address = "터미널"
#                 elif "역" in a[0].userInfo1:
#                     mopo = "인빌딩"
#                     address = "역사"
#                 elif "공항" in a[0].userInfo1:
#                     mopo = "인빌딩"
#                     address = "공항" 
#                 elif "대학" in a[0].userInfo1 or "학생" in a[0].userInfo1:
#                     mopo = "테마"
#                     address = "대학교"
#                 elif "공원" in a[0].userInfo1:
#                     mopo = "테마"
#                     address = "놀이공원"
#                 elif "거리" in a[0].userInfo1:
#                     mopo = "테마"
#                     address = "주요거리" 
#                 else:
#                     address = "수정필요"           
#             elif a[0].morphology_id == 3:
#                 mopo = "인빌딩"
#             elif a[0].morphology_id== 4:
#                 mopo = "커버리지"
#             elif a[0].morphology_id== 5 or a[0].userInfo2 == "L" or a[0].userInfo2 == "3":
#                 mopo = "취약지역"
#                 if a[0].userInfo1.endswith("도"):
#                     address = "유인도서"
#                 elif a[0].userInfo1.endswith("산"):
#                     address = "등산로"
#                 elif "해안도로" in a[0].userInfo1:
#                     address = "해안도로"
#                 elif "-" in a[0].userInfo1:
#                     address = "여객항로"
#                 else: 
#                     address = "수정필요"
#             else:
#                 pass
#             if a[0].networkId == "WiFi":
#                 if "개" in a[0].userInfo2: 
#                     address = "개방"
#                 elif "상" in a[0].userInfo2:
#                     address = "상용"
#                 else:
#                     address = "수정필요" 
#             else:
#                 pass
#             if "서울" in a[0].siDo or "서울" in a[0].guGun:
#                 district = "서울"
#             elif "인천" in a[0].siDo or "인천" in a[0].guGun:
#                 district = "인천"
#             elif "울산" in a[0].siDo or "울산" in a[0].guGun:
#                 district = "울산"
#             elif "대구" in a[0].siDo or "대구" in a[0].guGun:
#                 district = "대구"
#             elif "광주" in a[0].siDo or "광주" in a[0].guGun:
#                 district = "광주"
#             elif "대전" in a[0].siDo or "대전" in a[0].guGun:
#                 district = "대전"
#             elif "경기" in a[0].siDo or "경기" in a[0].guGun:
#                 district = "경기"
#             elif "경상북" in a[0].siDo or "경상북" in a[0].guGun:
#                 district = "경북"
#             elif "경상남" in a[0].siDo or "경상남" in a[0].guGun:
#                 district = "경남"
#             elif "전라남" in a[0].siDo or "전라남" in a[0].guGun:
#                 district = "전남"
#             elif "전라북" in a[0].siDo or "전라북" in a[0].guGun:
#                 district = "전북"
#             elif "충청남" in a[0].siDo or "충청남" in a[0].guGun:
#                 district = "충남"
#             elif "충청북" in a[0].siDo or "충청북" in a[0].guGun:
#                 district = "충북"
#             elif "세종" in a[0].siDo or "세종" in a[0].guGun:
#                 district = "세종"
#             else:
#                 district = "수도권"
#             lte_percent = ((a[0].nr_count)/a[0].total_count)*100
#              # 직렬화 대상 필드를 지정한다.
#             # fields = ['center_id', 'morphology_id', 'measdate', 'userInfo1', 'userInfo2', 'networkId', \
#             #         'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count']
#             fields = ['center_id','measdate', 'userInfo1', 'networkId']
#             serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
#             if hj.exists():
#                 # 해당 단말그룹에 대한 측정종료 데이터를 데이터베이스에 저장한다.
#                 hj.update(**serializer.data)
                
                
#                 # 평균속도, 전환율, 총 콜 수는 새로이 계산한 값으로 저장한다.
                
#                 hj.update(downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], \
#                         uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
#                         # siDo = siDo, guGun = guGun, addressDetail = addressDetail,\
#                         # dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
#                         address=address, mopo=mopo,district=district,lte_percent=lte_percent)
#                         # total_count=total_count)
#             else:
                
#                 # 해당 단말그룹에 대한 측정종료 데이터를 업데이트 한다
#                 TestDayClose.objects.create(phoneGroup=phoneGroup, \
#                                                 # siDo =siDo, guGun = guGun, addressDetail =addressDetail, \
#                                                 downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], \
#                                                 uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
#                                                 # dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
#                                                 address=address, mopo=mopo,district=district,lte_percent=lte_percent, \
#                                                 # total_count=total_count, \
#                                                 **serializer.data)