from distutils.util import change_root

from django.db import models
from monitor.models import *

from management.models import Center

from operator import itemgetter
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
import random

from message.tele_msg import TelegramBot  # 텔레그램 메시지 전송 클래스
from message.xmcs_msg import send_sms  # 2022.03.04 크로샷 메시지 전송 함수 호출

###############################################################################################################################################################################
#04.20 일일보고 사후측정 데이터
###############################################################################################################################################################################

class PostMeasure5G(models.Model):
    district_choice = (('서울','서울'),('인천','인천'),('부산','부산'),('울산','울산'),('대구','대구'),('광주','광주'),('대전','대전'),('경기','경기'),('강원','강원'),('경남','경남'),
                       ('경북','경북'),('전남','전남'),('전북','전북'),('충남','충남'),('충북','충북'),('세종','세종'),('고속도로','고속도로'),('지하철','지하철'),('전국','전국'),)
    measdate = models.DateField(default=timezone.now, verbose_name="측정일자", help_text="측정일자를 반드시 입력해야 합니다.")
    district = models.CharField(max_length=50,null=True,  blank=True, verbose_name="지역",choices=district_choice)
    name = models.CharField(max_length=50,null=True,  blank=True, verbose_name="측정국소")
    measkt_dl = models.FloatField(null=True, default=0,verbose_name="KT(DL)")
    measkt_ul = models.FloatField(null=True, default=0,verbose_name="KT(UL)")
    measkt_rsrp = models.FloatField(null=True, default=0,verbose_name="KT(RSRP)")
    measkt_lte = models.FloatField(null=True, default=0,verbose_name="KT(LTE대역)")
    postmeaskt_dl = models.FloatField(null=True, default=0,verbose_name="사후KT(DL)")
    postmeaskt_ul = models.FloatField(null=True, default=0,verbose_name="사후KT(UL)")
    postmeaskt_rsrp = models.FloatField(null=True, default=0,verbose_name="사후KT(RSRP)")
    postmeaskt_lte = models.FloatField(null=True, default=0,verbose_name="사후KT(LTE대역)")
    postmeasskt_dl = models.FloatField(null=True, default=0,verbose_name="사후SKT(DL)")
    postmeasskt_ul = models.FloatField(null=True, default=0,verbose_name="사후SKT(UL)")
    postmeasskt_rsrp = models.FloatField(null=True, default=0,verbose_name="사후SKT(RSRP)")
    postmeasskt_lte = models.FloatField(null=True, default=0,verbose_name="사후SKT(LTE대역)")
    postmeaslg_dl = models.FloatField(null=True, default=0,verbose_name="사후LG(DL)")
    postmeaslg_ul = models.FloatField(null=True, default=0,verbose_name="사후LG(UL)")
    postmeaslg_rsrp = models.FloatField(null=True, default=0,verbose_name="사후LG(RSRP)")
    postmeaslg_lte = models.FloatField(null=True, default=0,verbose_name="사후LG(LTE대역)")
    class Meta:
        verbose_name = ('사후측정(5G)')
        verbose_name_plural = ('사후측정(5G)')
        
    
    def __str__(self):
        return f"{self.name}"
  
class PostMeasureLTE(models.Model):    
    district_choice = (('서울','서울'),('인천','인천'),('부산','부산'),('울산','울산'),('대구','대구'),('광주','광주'),('대전','대전'),('경기','경기'),('강원','강원'),('경남','경남'),
                       ('경북','경북'),('전남','전남'),('전북','전북'),('충남','충남'),('충북','충북'),('세종','세종'),('고속도로','고속도로'),('지하철','지하철'),('전국','전국'),)
    measdate = models.DateField(default=timezone.now, verbose_name="측정일자", help_text="측정일자를 반드시 입력해야 합니다.")
    district = models.CharField(max_length=50,null=True,  blank=True, verbose_name="지역",choices=district_choice)
    name = models.CharField(max_length=50,null=True,  blank=True, verbose_name="측정국소")
    measkt_dl = models.FloatField(null=True, default=0,verbose_name="KT(DL)")
    measkt_ul = models.FloatField(null=True, default=0,verbose_name="KT(UL)")
    measkt_rsrp = models.FloatField(null=True, default=0,verbose_name="KT(RSRP)")
    measkt_sinr = models.FloatField(null=True, default=0,verbose_name="KT(SINR)")
    postmeaskt_dl = models.FloatField(null=True, default=0,verbose_name="사후KT(DL)")
    postmeaskt_ul = models.FloatField(null=True, default=0,verbose_name="사후KT(UL)")
    postmeaskt_rsrp = models.FloatField(null=True, default=0,verbose_name="사후KT(RSRP)")
    postmeaskt_sinr = models.FloatField(null=True, default=0,verbose_name="사후KT(SINR)")
    postmeasskt_dl = models.FloatField(null=True, default=0,verbose_name="사후SKT(DL)")
    postmeasskt_ul = models.FloatField(null=True, default=0,verbose_name="사후SKT(UL)")
    postmeasskt_rsrp = models.FloatField(null=True, default=0,verbose_name="사후SKT(RSRP)")
    postmeasskt_sinr = models.FloatField(null=True, default=0,verbose_name="사후SKT(SINR)")
    postmeaslg_dl = models.FloatField(null=True, default=0,verbose_name="사후LG(DL)")
    postmeaslg_ul = models.FloatField(null=True, default=0,verbose_name="사후LG(UL)")
    postmeaslg_rsrp = models.FloatField(null=True, default=0,verbose_name="사후LG(RSRP)")
    postmeaslg_sinr = models.FloatField(null=True, default=0,verbose_name="사후LG(SINR)")
    
    class Meta:
        verbose_name = ('사후측정(LTE)')
        verbose_name_plural = ('사후측정(LTE)')
        
    
    def __str__(self):
        return f"{self.name}"
    
###############################################################################################################################################################################
#3.16 측정대상 모델(수정완료)(클래스명 변경 필요, MeasPlan으로 변경예정)
###############################################################################################################################################################################
class MeasPlan(models.Model):
    planYear = models.IntegerField(null=True, default=0, verbose_name="계획년도") # 계획년도 
    
    nsahjd5G = models.IntegerField(null=True, default=0, verbose_name="5G 행정동") # 5G NSA - 행정동
    nsadg5G = models.IntegerField(null=True, default=0, verbose_name="5G 다중이용시설/교통인프라") # - 5G NSA 다중이용시설/교통인프라
    sa5G = models.IntegerField(null=True, default=0, verbose_name="5G SA") #SA  5G
    nsapublic5G = models.IntegerField(null=True, default=0, verbose_name="5G 공동망") # 공동망
    cv5G = models.IntegerField(null=True, default=0, verbose_name="5G 커버리지") # - 커버리지 5G
    totalnsa5G = models.IntegerField(null=True, default=0, verbose_name="5G NSA Total")
    total5G = models.IntegerField(null=True, default=0, verbose_name="5G Total")
    
    bctLTE = models.IntegerField(null=True, default=0, verbose_name="LTE 대도시") # LTE - 대도시 
    mctLTE = models.IntegerField(null=True, default=0, verbose_name="LTE 중소도시") # - 중소도시
    sctLTE = models.IntegerField(null=True, default=0, verbose_name="LTE 농어촌") # - 농어촌
    ibLTE = models.IntegerField(null=True, default=0, verbose_name="LTE 인빌딩") # - 인빌딩
    tmLTE = models.IntegerField(null=True, default=0, verbose_name="LTE 테마") # - 테마
    cvLTE = models.IntegerField(null=True, default=0, verbose_name="LTE 커버리지") # - 커버리지
    totalLTE = models.IntegerField(null=True, default=0, verbose_name="LTE Total")
    
    syWiFi = models.IntegerField(null=True, default=0, verbose_name="WiFi 상용") # WiFi - 상용
    gbWiFi = models.IntegerField(null=True, default=0, verbose_name="WiFi 개방") # - 개방
    publicWiFi = models.IntegerField(null=True, default=0, verbose_name="WiFi 공공") # 공공
    totalWiFi = models.IntegerField(null=True, default=0, verbose_name="WiFi Total")
    
    dsrWeak = models.IntegerField(null=True, default=0, verbose_name="취약지역 등산로") # 취약지역 - 등산로
    yghrWeak = models.IntegerField(null=True, default=0, verbose_name="취약지역 여객항로") # - 여객항로
    yidsWeak = models.IntegerField(null=True, default=0, verbose_name="취약지역 유인도서") # 유인도서
    hadrWeak = models.IntegerField(null=True, default=0, verbose_name="취약지역 해안도로") # 해안도로
    totalWeakArea = models.IntegerField(null=True, default=0, verbose_name="취약지역 Total")
    
    total = models.IntegerField(null=True, default=0, verbose_name="Total")

    class Meta:
        verbose_name = ('대상등록')
        verbose_name_plural = ('대상등록')
        
    
    def __str__(self):
        return f"{self.planYear}년도"


###############################################################################################################################################################################
#3.17 일일보고 추가 메세지 등록모델(수정중)
###############################################################################################################################################################################

class ReportMessage(models.Model):
    measdate = models.DateField(default=timezone.now, verbose_name="보고서 설명 날짜")
    msg5G = models.CharField(max_length=50, null=True, blank=True)
    msgLTE = models.CharField(max_length=50, null=True, blank=True)
    msgWiFi = models.CharField(max_length=50, null=True, blank=True)
    msgWeak = models.CharField(max_length=50, null=True, blank=True)
    msg5Gafter = models.CharField(max_length=50, null=True, blank=True)
    msgLTEafter = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = ('리포트 메시지')
        verbose_name_plural = ('리포트 메시지')

###############################################################################################################################################################################
#3.17 일일보고 작년 측정 결과 등록 모델 5G
###############################################################################################################################################################################

class MeasLastyear5G(models.Model):
    area_choice = (('대도시','대도시'),('중소도시','중소도시'),('행정동','행정동'),('다중이용시설','다중이용시설'),('아파트','아파트'),('대학교','대학교'),('교통인프라','교통인프라'),('종합','종합'),)
    measarea = models.CharField(max_length=50, null=True, blank=True,choices=area_choice,verbose_name="측정 모폴로지")
    
    DL = models.FloatField(null=True, default=0,verbose_name="전송속도(DL)")
    UL = models.FloatField(null=True, default=0,verbose_name="전송속도(UL)")
    LTEDL= models.FloatField(null=True, default=0,verbose_name="LTE 전환율(DL)")
    LTEUL = models.FloatField(null=True, default=0,verbose_name="LTE 전환율(UL)")
    delay = models.FloatField(null=True, default=0,verbose_name="지연시간")

    class Meta:
        verbose_name = ('모폴로지별 작년결과(5G)')
        verbose_name_plural = ('모폴로지별 작년결과(5G)')
        
    
    def __str__(self):
        return f"{self.measarea}"


###############################################################################################################################################################################
#3.17 일일보고 작년 측정 결과 등록 모델 LTE
###############################################################################################################################################################################

class MeasLastyearLTE(models.Model):
    area_choice = (('대도시','대도시'),('중소도시','중소도시'),('농어촌','농어촌'),('행정동','행정동'),('인빌딩','인빌딩'),('테마','테마'),('종합','종합'),)
    measarea = models.CharField(max_length=50, null=True, blank=True,choices=area_choice)
    
    DL = models.FloatField(null=True, default=0,verbose_name="전송속도(DL)")
    UL = models.FloatField(null=True, default=0,verbose_name="전송속도(UL)")
    delay = models.FloatField(null=True, default=0,verbose_name="지연시간")

    class Meta:
        verbose_name = ('모폴로지별 작년결과(LTE)')
        verbose_name_plural = ('모폴로지별 작년결과(LTE)')
        
    
    def __str__(self):
        return f"{self.measarea}"
    
###############################################################################################################################################################################
#3.17 일일보고 지역별 작년측정 DL
###############################################################################################################################################################################

class MeasLastyeardistrict(models.Model):
    nettype_choice = (("5G","5G"),("LTE","LTE"),("WiFi지하철","WiFi지하철"))
    district_choice = (('종합','종합'),('서울','서울'),('수도권','수도권'),('인천','인천'),('부산','부산'),('울산','울산'),('대구','대구'),('광주','광주'),('대전','대전'),('경기','경기'),('강원','강원'),('경남','경남'),
                       ('경북','경북'),('전남','전남'),('전북','전북'),('충남','충남'),('충북','충북'),('세종','세종'),('고속도로','고속도로'),('지하철','지하철'),('전국','전국'),)
    
    nettype = models.CharField(max_length=50, null=True, blank=True,choices=nettype_choice)
    district = models.CharField(max_length=50, null=True, blank=True,choices=district_choice) 
    KTDL = models.FloatField(null=True, default=0,verbose_name="KT 전송속도(DL)")
    KTUL = models.FloatField(null=True, default=0,verbose_name="KT 전송속도(UL)")
    SKTDL = models.FloatField(null=True, default=0,verbose_name="S사 전송속도(DL)")
    LGDL = models.FloatField(null=True, default=0,verbose_name="L사 전송속도(DL)")
    
    class Meta:
        verbose_name = ('지역별 3사 작년결과(DL)')
        verbose_name_plural = ('지역별 3사 작년결과(DL)')
        
    
    def __str__(self):
        return f"{self.nettype}/{self.district}"

###############################################################################################################################################################################
#4.25 일일보고 작년 측정 결과 등록 모델 WiFi(수정중)
###############################################################################################################################################################################

class MeasLastyearWiFi(models.Model):
    type_choice = (('상용','상용'),('개방','개방'),('공공','공공'),('종합','종합'),)
    WiFitype = models.CharField(max_length=50, null=True, blank=True,choices=type_choice)
    
    DL = models.FloatField(null=True, default=0,verbose_name="전송속도(DL)")
    UL = models.FloatField(null=True, default=0,verbose_name="전송속도(UL)")
    
    class Meta:
        verbose_name = ('타입별 작년결과(WiFi)')
        verbose_name_plural = ('타입별 작년결과(WiFi)')
        
    
    def __str__(self):
        return f"{self.WiFitype}"
    
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


#def send_message_hj(sender, instance, created, **kwargs):
def send_message_hj(hoho, **kwargs):
    """ 생성된 메시지를 크로샷 또는 텔레그램으로 전송하는 함수
        - 파라미터
          . sender: 메시지 모델 클래스
          . instance: 메시지 객체 (생성된 레코드 하나 데이터)
          . created: 신규생성 여부(True or False)
          . kwargs: 키워트 파라미터
        - 반환값: 없음
    """
    for instance in hoho:
    # if created:
    #if instance.phoneGroup != None:  # 커버리지의 경우 PhoneGroup 미존재
        a = Phone.objects.filter(userInfo1 = instance.userInfo1, measdate = instance.measdate)
        b = PhoneGroup.objects.filter(id= instance.phoneGroup_id)
        c = MorphologyDetail.objects.filter(id = b[0].morphologyDetail_id)
        format_data = "%Y%m%d"

        qs = LastMeasDayClose.objects.create(
                    measdate =  datetime.strptime(instance.measdate, format_data).date(),  # 측정일자(예: 20211101)
                    userInfo1 = instance.userInfo1,
                    networkId = instance.networkId,  # 네트워크ID(5G, LTE, 3G, WiFi)
                    center = instance.center.centerName,
                    morphology = instance.morphology.morphology,
                    downloadBandwidth = instance.downloadBandwidth,  # DL속도 (초단위 데이터 평균)
                    uploadBandwidth = instance.uploadBandwidth,  # UP속도 (초단위 데이터 평균) 
                    dl_nr_percent = instance.dl_nr_percent,
                    ul_nr_percent = instance.ul_nr_percent ,
                    udpJitter = instance.udpJitter,  # 지연시간
                    siDo = a[0].siDo,
                    guGun = a[0].guGun,
                    addressDetail = a[0].addressDetail,
                    district = instance.phoneGroup.measureArea,
                    
        )
        if c.exists():
            qs.nettype, qs.mopho, qs.detailadd, qs.subadd = c[0].network_type, c[0].main_class, c[0].middle_class, c[0].sub_class
            qs.save()
    else:  # PhoneGroup이 None인 커버리지의 경우
        pass
       
    # else:
    #     # 메시지가 업데이트 되었을 때는 아무런 처리를 하지 않는다.
    #     pass



########################################################################################################################
# 허재 측정마감 테스트
########################################################################################################################

class LastMeasDayClose(models.Model):
    """측정마감 클래스"""
    nettype_choice = (("5G NSA","5G NSA"),("5G SA","5G SA"),("5G 공동망","5G 공동망"),("LTE","LTE"),("WiFi","WiFi"),("품질취약지역","품질취약지역"),)
    mopho_choice = (("행정동","행정동"),("다중이용시설","다중이용시설"),("교통인프라","교통인프라"),("커버리지","커버리지"),("인빌딩","인빌딩"),("테마","테마"),("상용","상용"),("개방","개방"),("공공","공공"),("품질취약지역","품질취약지역"),)
    detailadd_choice = (("대도시","대도시"),("중소도시","중소도시"),("농어촌","농어촌"),("대형점포","대형점포"),("대학교","대학교"),("아파트","아파트"),("대형병원","대형병원"),("영화관","영화관"),("공항","공항"),
                        ("주요거리","주요거리"),("시장","시장"),("지하상가","지하상가"),("놀이공원","놀이공원"),("도서관","도서관"),("전시시설","전시시설"),("터미널","터미널"),("지하철노선","지하철노선"),("고속도로","고속도로"),
                        ("지하철역사","지하철역사"),("KTX,SRT역사","KTX,SRT역사"),("KTX,SRT노선","KTX,SRT노선"),("지하철","지하철"),("등산로","등산로"),("여객항로","여객항로"),("유인도서","유인도서"),("해안도로","해안도로"),)
    district_choice = (('서울','서울'),('인천','인천'),('부산','부산'),('울산','울산'),('대구','대구'),('광주','광주'),('대전','대전'),('경기','경기'),('강원','강원'),('경남','경남'),
                       ('경북','경북'),('전남','전남'),('전북','전북'),('충남','충남'),('충북','충북'),('세종','세종'),('고속도로','고속도로'),('지하철','지하철'),('전국','전국'),)
    center_choice = (('서울강북','서울강북'),('강원','강원'),('경기북부','경기북부'),('서울강남','서울강남'),('경기남부','경기남부'),('경기서부','경기서부'),('부산','부산'),
                       ('경남','경남'),('대구','대구'),('경북','경북'),('전남','전남'),('전북','전북'),('충남','충남'),('충북','충북'),)
    
    measdate = models.DateField(default=timezone.now, verbose_name="측정일자", help_text="측정일자를 반드시 입력해야 합니다.")
    userInfo1 = models.CharField(max_length=100, verbose_name="측정자 입력값1")
    networkId = models.CharField(max_length=100, null=True, blank=True, verbose_name="네트워크(raw)")  # 네트워크ID(5G, LTE, 3G, WiFi)
    nettype = models.CharField(max_length=100, null=True, blank=True,verbose_name="네트워크",default='',choices=nettype_choice)
    center = models.CharField(max_length=100,null=True, blank=True, verbose_name="센터", choices=center_choice)
    district = models.CharField(max_length=100, null=True, blank=True,verbose_name="지역",default='', choices=district_choice)
    morphology = models.CharField(max_length=100,null=True, blank=True, verbose_name="모풀로지(raw)")
    mopho = models.CharField(max_length=100, null=True, blank=True,verbose_name="모폴로지",default='', choices=mopho_choice)
    detailadd = models.CharField(max_length=100, null=True, blank=True,verbose_name="모폴로지2",default='', choices=detailadd_choice)
    subadd = models.CharField(max_length=100, null=True, blank=True,verbose_name="SA측정여부",default='')
    downloadBandwidth = models.FloatField(null=True, blank=True, verbose_name='DL')  # DL속도 (초단위 데이터 평균)
    uploadBandwidth = models.FloatField(null=True, blank=True, verbose_name='UL')  # UP속도 (초단위 데이터 평균)
    dl_nr_percent = models.FloatField(null=True, default=0.0, verbose_name='DL LTE전환율')  # 5G->NR 전환 전환율(dl)
    ul_nr_percent = models.FloatField(null=True, default=0.0, verbose_name='UL LTE전환율')  # 5G->NR 전환 전환율(ul)
    udpJitter = models.FloatField(null=True, default=0.0, verbose_name='지연시간')  # 지연시간
    ktlastdl = models.FloatField(null=True, blank=True, verbose_name='작년 KT DL')
    ktlastul = models.FloatField(null=True, blank=True, verbose_name='작년 KT UL')
    sktlastdl = models.FloatField(null=True, blank=True, verbose_name='작년 S사 DL')
    sktlastul = models.FloatField(null=True, blank=True, verbose_name='작년 S사 UL')
    lglastdl = models.FloatField(null=True, blank=True, verbose_name='작년 L사 DL')
    lglastul = models.FloatField(null=True, blank=True, verbose_name='작년 L사 UL')
    siDo = models.CharField(max_length=100, null=True, blank=True, verbose_name="시,도", default='')  # 시도
    guGun = models.CharField(max_length=100, null=True, blank=True, verbose_name="군,구", default='')  # 구,군
    addressDetail = models.CharField(max_length=100, null=True, blank=True, verbose_name="상세주소", default='')  # 주소상세
    plus = models.CharField(max_length=100, null=True, blank=True,verbose_name="추가사항",default='')
    
    
    
    class Meta:
        ordering = ['-measdate']
        verbose_name = ('측정결과')
        verbose_name_plural = ('측정결과')
        
    
    def __str__(self):
        return f"{self.userInfo1}"


# post_save.connect(send_message_hj, sender=MeasuringDayClose)



