from django.db.models import Avg, Max
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone, MeasuringDayClose
from analysis.models import *
import pandas as pd
import datetime
from django.db.models import Sum
from django.db.models import Q
###################################################################################################
# 일일보고 및 대상등록 관련 모듈
# -------------------------------------------------------------------------------------------------
# 2022-03-23 - 모듈 정리 및 주석 추가
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 일일보고 페이지
# - 실제 측정마감데이터로 교체(4.19)
#
# [ 고민해야 하는 사항 ]
#  - JSON형태의 컨텍스트를 만드는 코드 정규화
# -------------------------------------------------------------------------------------------------
district_list = ['서울','인천','부산','울산','대구','광주','대전','경기','강원','경남','경북','전남','전북','충남','충북','세종','전국']
center_list = ['서울강북','강원','경기북부','서울강남','경기남부','경기서부','부산','경남','대구','경북','전남','전북','충남','충북']
city_list = ["대도시",'중소도시','농어촌']
facility5g_list = ['대형점포','대학교','아파트','병원','영화관','공항','거리','시장','지하상가','놀이공원','도서관','전시시설','터미널']
traffic5g_list = ['지하철노선','고속도로','지하철역사','KTX.SRT역사','KTX.SRT노선']
inbuildinglte_list = ['대형점포','KTX.SRT역사','대형병원','터미널','지하철역사','공항','전시시설','지하상가']
themelte_list = ['지하철','전통시장','대학교','놀이공원','주요거리','고속도로','KTX.SRT노선']
def get_report_cntx():
    """ 일일보고 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
    #사후측정
    postmeas5g = PostMeasure5G.objects.all()
    postmeaslte = PostMeasureLTE.objects.all()

    regi = MeasPlan.objects.filter(planYear = "2022")
    firstdate = LastMeasDayClose.objects.last()
    lastdate = LastMeasDayClose.objects.first()
    reportmsg = ReportMessage.objects.all()
    
    sregi = LastMeasDayClose.objects.all()
    tregi = LastMeasDayClose.objects.filter(measdate = datetime.date.today())
    
    sregi5G1 = LastMeasDayClose.objects.filter(networkId = "5G NSA", morphology = "행정동").count()
    sregi5G2 = LastMeasDayClose.objects.filter(Q(networkId = "5G NSA")&(Q(morphology = "다중이용시설")|Q(morphology = "교통인프라"))).count()
    sregi5G3 = LastMeasDayClose.objects.filter(networkId = "5G NSA").count()
    sregi5G4 = LastMeasDayClose.objects.filter(networkId = "5G SA ").count()
    sregi5G5 = LastMeasDayClose.objects.filter(networkId = "5G 공동망").count()
    sregi5G6 = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망")) & Q(morphology = "커버리지") & Q(address = "다중이용시설/교통인프라")).count()
    sregi5G7 = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망")) & Q(morphology = "커버리지") & Q(address = "중소시설")).count()
    sregi5G8 = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망"))).count()
    
    tregi5G1 = LastMeasDayClose.objects.filter(networkId = "5G NSA", morphology = "행정동", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G2 = LastMeasDayClose.objects.filter(Q(networkId = "5G NSA")&(Q(morphology = "다중이용시설")|Q(morphology = "교통인프라"))&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    tregi5G3 = LastMeasDayClose.objects.filter(networkId = "5G NSA", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G4 = LastMeasDayClose.objects.filter(networkId = "5G SA ", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G5 = LastMeasDayClose.objects.filter(networkId = "5G 공동망", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G6 = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망")) & Q(morphology = "커버리지") & Q(address = "다중이용시설/교통인프라")&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    tregi5G7 = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망")) & Q(morphology = "커버리지") & Q(address = "중소시설")&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    tregi5G8 = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망"))&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    
    district5gcount = []
    for i in district_list:
        district5gcount.append(LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망"))&Q(district = i)).count())
    city5gcount = []
    for i in city_list:
        city5gcount.append(LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망"))&Q(address = i)).count())
    facility5gcount = []
    for i in facility5g_list:
        facility5gcount.append(LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망"))&Q(address = i)).count())
    sregiLTE1 = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시").count()
    sregiLTE2 = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시").count()
    sregiLTE3 = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌").count()
    sregiLTE4 = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩").count()
    sregiLTE5 = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "테마").count()
    sregiLTE6 = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "커버리지").count()
    sregiLTE = LastMeasDayClose.objects.filter(networkId = "LTE").count()
    
    tregiLTE1 = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), address = "대도시").count()
    tregiLTE2 = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), address = "중소도시").count()
    tregiLTE3 = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), address = "농어촌").count()
    tregiLTE4 = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), morphology = "인빌딩").count()
    tregiLTE5 = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), morphology = "테마").count()
    tregiLTE6 = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), morphology = "커버리지").count()
    tregiLTE = LastMeasDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d')).count()

    sregiWiFi1 = LastMeasDayClose.objects.filter(networkId = "WiFi", morphology = "상용").count()
    sregiWiFi2 = LastMeasDayClose.objects.filter(networkId = "WiFi", morphology = "개방").count()
    sregiWiFi3 = LastMeasDayClose.objects.filter(networkId = "WiFi", morphology = "공공").count()
    sregiWiFi = LastMeasDayClose.objects.filter(networkId = "WiFi").count()
    tregiWiFi1 = LastMeasDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d'), morphology = "상용").count()
    tregiWiFi2 = LastMeasDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d'), morphology = "개방").count()
    tregiWiFi3 = LastMeasDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d'), morphology = "공공").count()
    tregiWiFi = LastMeasDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d')).count()
    
    sregiweak1 = LastMeasDayClose.objects.filter(morphology = "취약지역", address = "등산로").count()
    sregiweak2 = LastMeasDayClose.objects.filter(morphology = "취약지역", address = "여객항로").count()
    sregiweak3 = LastMeasDayClose.objects.filter(morphology = "취약지역", address = "유인도서").count()
    sregiweak4 = LastMeasDayClose.objects.filter(morphology = "취약지역", address = "해안도로").count()
    sregiweak = LastMeasDayClose.objects.filter(morphology = "취약지역").count()
    tregiweak1 = LastMeasDayClose.objects.filter(morphology = "취약지역",  measdate = datetime.date.today(), address = "등산로").count()
    tregiweak2 = LastMeasDayClose.objects.filter(morphology = "취약지역",  measdate = datetime.date.today(), address = "여객항로").count()
    tregiweak3 = LastMeasDayClose.objects.filter(morphology = "취약지역",  measdate = datetime.date.today(), address = "유인도서").count()
    tregiweak4 = LastMeasDayClose.objects.filter(morphology = "취약지역",  measdate = datetime.date.today(), address = "해안도로").count()
    tregiweak = LastMeasDayClose.objects.filter(morphology = "취약지역",  measdate = datetime.date.today()).count()
    

    hjd5gseoul = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "서울").count()
    hjd5gincheon = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "인천").count()
    hjd5gulsan = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "울산").count()
    hjd5gdaegu = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "대구").count()
    hjd5ggwangju = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "광주").count()
    hjd5gdaejun = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "대전").count()
    hjd5ggyunggi = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "경기").count()
    hjd5ggyungbuk = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "경북").count()
    hjd5gjunnam = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "전남").count()
    hjd5gjunbuk = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "전북").count()
    hjd5gchungnam = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "충남").count()
    hjd5gchungbuk = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "충북").count()
    hjd5gsejong = LastMeasDayClose.objects.filter(networkId = "5G", morphology = "행정동", district = "세종").count()

    dagyo5gseoul = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "서울")).count()
    dagyo5gincheon = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "인천")).count()
    dagyo5gulsan = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "울산")).count()
    dagyo5gdaegu = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "대구")).count()
    dagyo5ggwangju = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "광주")).count()
    dagyo5gdaejun = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "대전")).count()
    dagyo5ggyunggi = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "경기")).count()
    dagyo5ggyungbuk = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "경북")).count()
    dagyo5gjunnam = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "전남")).count()
    dagyo5gjunbuk = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "전북")).count()
    dagyo5gchungnam = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "충남")).count()
    dagyo5gchungbuk = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "충북")).count()
    dagyo5gsejong = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "세종")).count()
    dagyo5gsudo = LastMeasDayClose.objects.filter(Q(networkId = "5G")&(Q(morphology = "인빌딩")|Q(morphology = "테마"))&Q(district = "수도권")).count()


    # bigcityLTE = []
    # for i in district_list:
    #     bigcityLTE.append(LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = i).count())

    
    bigcityLTEseoul = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "서울").count()
    bigcityLTEincheon = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "인천").count()
    bigcityLTEulsan = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "울산").count()
    bigcityLTEdaegu = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "대구").count()
    bigcityLTEgwangju = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "광주").count()
    bigcityLTEdaejun = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "대전").count()
    bigcityLTEgyunggi = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "경기").count()
    bigcityLTEgyungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "경북").count()
    bigcityLTEjunnam = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "전남").count()
    bigcityLTEjunbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "전북").count()
    bigcityLTEchungnam = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "충남").count()
    bigcityLTEchungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "충북").count()
    bigcityLTEsejong = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "세종").count()
    bigcityLTEsudo = LastMeasDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "수도권").count()

    smallcityLTEseoul = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "서울").count()
    smallcityLTEincheon = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "인천").count()
    smallcityLTEulsan = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "울산").count()
    smallcityLTEdaegu = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "대구").count()
    smallcityLTEgwangju = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "광주").count()
    smallcityLTEdaejun = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "대전").count()
    smallcityLTEgyunggi = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "경기").count()
    smallcityLTEgyungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "경북").count()
    smallcityLTEjunnam = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "전남").count()
    smallcityLTEjunbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "전북").count()
    smallcityLTEchungnam = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "충남").count()
    smallcityLTEchungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "충북").count()
    smallcityLTEsejong = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "세종").count()
    smallcityLTEsudo = LastMeasDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "수도권").count()

    
    nongLTEseoul = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "서울").count()
    nongLTEincheon = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "인천").count()
    nongLTEulsan = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "울산").count()
    nongLTEdaegu = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "대구").count()
    nongLTEgwangju = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "광주").count()
    nongLTEdaejun = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "대전").count()
    nongLTEgyunggi = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "경기").count()
    nongLTEgyungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "경북").count()
    nongLTEjunnam = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "전남").count()
    nongLTEjunbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "전북").count()
    nongLTEchungnam = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "충남").count()
    nongLTEchungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "충북").count()
    nongLTEsejong = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "세종").count()
    nongLTEsudo = LastMeasDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "수도권").count()

    inbuildingLTEcdys = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "철도역사").count()
    inbuildingLTEdhbw = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "대형병원").count()
    inbuildingLTEbhj = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "백화점").count()
    inbuildingLTEtmn = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "터미널").count()
    inbuildingLTEgh = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "공항").count()
    inbuildingLTEdhjp = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "대형점포").count()
    inbuildingLTEjsj = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "전시장").count()
    inbuildingLTEjhcys = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "인빌딩", address = "지하철역사").count()

    themeLTEjunnam = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "테마", address = "대학교").count()
    themeLTEjunbuk = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "테마", address = "놀이공원").count()
    themeLTEchungnam = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "테마", address = "주요거리").count()
    themeLTEchungbuk = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "테마", address = "전통시장").count()
    themeLTEsejong = LastMeasDayClose.objects.filter(networkId = "LTE", morphology = "테마", address = "지하철노선").count()
    
    sangWiFiseoul = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "서울", plus = "").count()
    sangWiFiincheon = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "인천", plus = "").count()
    sangWiFiulsan = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "울산", plus = "").count()
    sangWiFidaegu = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대구", plus = "").count()
    sangWiFigwangju = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "광주", plus = "").count()
    sangWiFidaejun = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대전", plus = "").count()
    sangWiFigyunggi = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경기", plus = "").count()
    sangWiFigyungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경북", plus = "").count()
    sangWiFijunnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전남", plus = "").count()
    sangWiFijunbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전북", plus = "").count()
    sangWiFichungnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충남", plus = "").count()
    sangWiFichungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충북", plus = "").count()
    sangWiFisejong = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "세종", plus = "").count()
    sangWiFisudo = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "수도권", plus = "").count()

    trainsangWiFiseoul = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "서울", plus = "지하철").count()
    trainsangWiFiincheon = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "인천", plus = "지하철").count()
    trainsangWiFiulsan = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "울산", plus = "지하철").count()
    trainsangWiFidaegu = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대구", plus = "지하철").count()
    trainsangWiFigwangju = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "광주", plus = "지하철").count()
    trainsangWiFidaejun = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대전", plus = "지하철").count()
    trainsangWiFigyunggi = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경기", plus = "지하철").count()
    trainsangWiFigyungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경북", plus = "지하철").count()
    trainsangWiFijunnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전남", plus = "지하철").count()
    trainsangWiFijunbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전북", plus = "지하철").count()
    trainsangWiFichungnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충남", plus = "지하철").count()
    trainsangWiFichungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충북", plus = "지하철").count()
    trainsangWiFisejong = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "세종", plus = "지하철").count()
    trainsangWiFisudo = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "수도권", plus = "지하철").count()

    gaeWiFiseoul = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "서울", plus = "").count()
    gaeWiFiincheon = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "인천", plus = "").count()
    gaeWiFiulsan = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "울산", plus = "").count()
    gaeWiFidaegu = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대구", plus = "").count()
    gaeWiFigwangju = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "광주", plus = "").count()
    gaeWiFidaejun = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대전", plus = "").count()
    gaeWiFigyunggi = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경기", plus = "").count()
    gaeWiFigyungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경북", plus = "").count()
    gaeWiFijunnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전남", plus = "").count()
    gaeWiFijunbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전북", plus = "").count()
    gaeWiFichungnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충남", plus = "").count()
    gaeWiFichungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충북", plus = "").count()
    gaeWiFisejong = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "세종", plus = "").count()
    gaeWiFisudo = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "수도권", plus = "").count()

    
    # traingaeWiFi = []
    # for i in district_list:
    #     ##locals()[f'traingaeWiFi{i}'] = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = i, plus = "지하철").count()
    #     traingaeWiFi.append(LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = i, plus = "지하철").count())

    traingaeWiFiseoul = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "서울", plus = "지하철").count()
    traingaeWiFiincheon = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "인천", plus = "지하철").count()
    traingaeWiFiulsan = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "울산", plus = "지하철").count()
    traingaeWiFidaegu = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대구", plus = "지하철").count()
    traingaeWiFigwangju = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "광주", plus = "지하철").count()
    traingaeWiFidaejun = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대전", plus = "지하철").count()
    traingaeWiFigyunggi = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경기", plus = "지하철").count()
    traingaeWiFigyungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경북", plus = "지하철").count()
    traingaeWiFijunnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전남", plus = "지하철").count()
    traingaeWiFijunbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전북", plus = "지하철").count()
    traingaeWiFichungnam = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충남", plus = "지하철").count()
    traingaeWiFichungbuk = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충북", plus = "지하철").count()
    traingaeWiFisejong = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "세종", plus = "지하철").count()
    traingaeWiFisudo = LastMeasDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "수도권", plus = "지하철").count()

    weakseoul = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "서울").count()
    weakincheon = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "인천").count()
    weakulsan = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "울산").count()
    weakdaegu = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "대구").count()
    weakgwangju = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "광주").count()
    weakdaejun = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "대전").count()
    weakgyunggi = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "경기").count()
    weakgyungbuk = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "경북").count()
    weakjunnam = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "전남").count()
    weakjunbuk = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "전북").count()
    weakchungnam = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "충남").count()
    weakchungbuk = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "충북").count()
    weaksejong = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "세종").count()
    weaksudo = LastMeasDayClose.objects.filter(morphology = "취약지역", district = "수도권").count()
    
#작년 측정결과(과년도로 변경 예정)
    last5g = MeasLastyear5G.objects.all()
    lastlte = MeasLastyearLTE.objects.all()
    lastwifi = MeasLastyearWiFi.objects.all()
#5G 측정결과
    try:
        bct5gdl = round(LastMeasDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        bct5gdl = ""
    try:
        bct5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        bct5gul = ""
    try:
        bct5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        bct5glte = ""
    try:
        bct5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        bct5gsucc = ""
    try:
        bct5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        bct5gconn = ""
    try:
        bct5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        bct5gjitter = ""
    
    try:
        mct5gdl =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        mct5gdl = ""
    try:
        mct5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        mct5gul = ""
    try:
        mct5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        mct5glte = ""
    try:
        mct5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        mct5gsucc = ""
    try:
        mct5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        mct5gconn = ""
    try:
        mct5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        mct5gjitter = ""

    try:
        ct5gdl =  round(LastMeasDayClose.objects.filter(networkId = "5G",morphology="행정동").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        ct5gdl = ""
    try:
        ct5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", morphology="행정동").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        ct5gul = ""
    try:
        ct5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", morphology="행정동").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        ct5glte = ""
    try:
        ct5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", morphology="행정동").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        ct5gsucc = ""
    try:
        ct5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", morphology="행정동").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        ct5gconn = ""
    try:
        ct5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", morphology="행정동").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        ct5gjitter = ""

    try:
        dj5gdl =  round(LastMeasDayClose.objects.filter(networkId = "5G",plus="다중이용시설").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        dj5gdl = ""
    try:
        dj5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        dj5gul = ""
    try:
        dj5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        dj5glte = ""
    try:
        dj5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        dj5gsucc = ""
    try:
        dj5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        dj5gconn = ""
    try:
        dj5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        dj5gjitter = ""
    
    try:
        apt5gdl =  round(LastMeasDayClose.objects.filter(networkId = "5G",plus="아파트").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        apt5gdl = ""
    try:
        apt5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        apt5gul = ""
    try:
        apt5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        apt5glte = ""
    try:
        apt5gsucc = round(LastMeasDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        apt5gsucc = ""
    try:
        apt5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        apt5gconn = ""
    try:
        apt5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        apt5gjitter = ""

    try:
        univ5gdl =  round(LastMeasDayClose.objects.filter(networkId = "5G",plus="대학교").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        univ5gdl = ""
    try:
        univ5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        univ5gul = ""
    try:
        univ5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        univ5glte = ""
    try:
        univ5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        univ5gsucc = ""
    try:
        univ5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        univ5gconn = ""
    try:
        univ5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        univ5gjitter = ""

    try:
        traffic5gdl =  round(LastMeasDayClose.objects.filter(networkId = "5G",plus="교통인프라").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        traffic5gdl = ""
    try:
        traffic5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        traffic5gul = ""
    try:
        traffic5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        traffic5glte = ""
    try:
        traffic5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        traffic5gsucc = ""
    try:
        traffic5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        traffic5gconn = ""
    try:
        traffic5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        traffic5gjitter = ""

    try:
        total5gdl = round(LastMeasDayClose.objects.filter(networkId = "5G").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        total5gdl = ""
    try:
        total5gul =  round(LastMeasDayClose.objects.filter(networkId = "5G").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        total5gul = ""
    try:
        total5glte =  round(LastMeasDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        total5glte = ""
    try:
        total5gsucc =  round(LastMeasDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        total5gsucc = ""
    try:
        total5gconn =  round(LastMeasDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        total5gconn = ""
    try:
        total5gjitter =  round(LastMeasDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        total5gjitter = ""

#LTE 측정결과

    try:
        bctltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        bctltedl = ""
    try:
        bctlteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        bctlteul = ""
    try:
        bctltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        bctltesucc = ""
    try:
        bctltejitter =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        bctltejitter = ""

    try:
        mctltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        mctltedl = ""
    try:
        mctlteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        mctlteul = ""
    try:
        mctltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        mctltesucc = ""
    try:
        mctltejitter =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        mctltejitter = ""

    try:
        sctltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        sctltedl = ""
    try:
        sctlteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        sctlteul = ""
    try:
        sctltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        sctltesucc = ""
    try:
        sctltejitter =  round(LastMeasDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        sctltejitter = ""

    try:
        totalctltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="행정동").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalctltedl = ""
    try:
        totalctlteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="행정동").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalctlteul = ""
    try:
        totalctltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="행정동").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        totalctltesucc = ""
    try:
        totalctltejitter =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="행정동").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        totalctltejitter = ""

    try:
        inbuildingltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="인빌딩").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        inbuildingltedl = ""
    try:
        inbuildinglteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="인빌딩").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        inbuildinglteul = ""
    try:
        inbuildingltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="인빌딩").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        inbuildingltesucc = ""
    try:
        inbuildingltejitter =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="인빌딩").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        inbuildingltejitter = ""

    try:
        themeltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        themeltedl = ""
    try:
        themelteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        themelteul = ""
    try:
        themeltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        themeltesucc = ""
    try:
        themeltejitter = round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        themeltejitter = ""

    try:
        totalltedl =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalltedl = ""
    try:
        totallteul =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totallteul = ""
    try:
        totalltesucc =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        totalltesucc = ""
    try:
        totalltejitter =  round(LastMeasDayClose.objects.filter(networkId = "LTE", morphology="테마").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        totalltejitter = ""

    
#wifi 측정결과(종합)
    try:
        totalwifidl = round(LastMeasDayClose.objects.filter(networkId = "WiFi").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalwifidl = ""
    try:
        totalsywifidl = round(LastMeasDayClose.objects.filter(networkId = "WiFi", address = "상용").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalsywifidl = ""
    try:
        totalgbwifidl = round(LastMeasDayClose.objects.filter(networkId = "WiFi", address = "개방").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalgbwifidl = ""
    try:
        totalwifiul = round(LastMeasDayClose.objects.filter(networkId = "WiFi").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalwifiul = ""
    try:
        totalsywifiul = round(LastMeasDayClose.objects.filter(networkId = "WiFi", address = "상용").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalsywifiul = ""
    try:
        totalgbwifiul = round(LastMeasDayClose.objects.filter(networkId = "WiFi", address = "개방").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalgbwifiul = ""
#wifi 측정결과(센터별)
#wifi 측정결과(지역별)
#금일 측정 결과 
    tresult5g = LastMeasDayClose.objects.filter((Q(networkId = "5G NSA")|Q(networkId = "5G SA")|Q(networkId = "5G 공동망"))&Q(measdate = datetime.date.today().strftime('%Y%m%d')))
    tresultlte = LastMeasDayClose.objects.filter(networkId = "LTE", measdate = datetime.date.today())
    tresultwifi = LastMeasDayClose.objects.filter(networkId = "WiFi", measdate = datetime.date.today())
    tresultweak = LastMeasDayClose.objects.filter(networkId = "취약지역", measdate = datetime.date.today())
   
    context = {
    # 'bigcityLTE':bigcityLTE,
    'tresult5g':tresult5g,'tresultlte':tresultlte,'tresultwifi':tresultwifi,'tresultweak':tresultweak,
    'regi':regi, 'reportmsg':reportmsg,'sregi':sregi,'firstdate':firstdate,'lastdate':lastdate,
    'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G4':tregi5G4, 'tregi5G5':tregi5G5,'tregi5G6':tregi5G6,'tregi5G7':tregi5G7,'tregi5G8':tregi5G8,
    'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G4':sregi5G4,'sregi5G5':sregi5G5,'sregi5G6':sregi5G6,'sregi5G7':sregi5G7,'sregi5G8':sregi5G8,
    'sregiLTE1':sregiLTE1, 'sregiLTE2':sregiLTE2,'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,'sregiLTE':sregiLTE, 
    'tregiLTE1':tregiLTE1,'tregiLTE2':tregiLTE2, 'tregiLTE3':tregiLTE3,'tregiLTE4':tregiLTE4, 'tregiLTE5':tregiLTE5,'tregiLTE6':tregiLTE6, 'tregiLTE':tregiLTE,
    'sregiWiFi1':sregiWiFi1,'sregiWiFi2':sregiWiFi2,'sregiWiFi':sregiWiFi,'tregiWiFi1':tregiWiFi1,'tregiWiFi2':tregiWiFi2,'tregiWiFi':tregiWiFi,'sregiweak1':sregiweak1,
    'sregiweak2':sregiweak2,'sregiweak3':sregiweak3,'sregiweak4':sregiweak4,'sregiweak':sregiweak,'tregiweak1':tregiweak1,'tregiweak2':tregiweak2,'tregiweak3':tregiweak3,'tregiweak4':tregiweak4,
    'tregiweak':tregiweak,'hjd5gseoul':hjd5gseoul, 'hjd5gincheon':hjd5gincheon, 'hjd5gulsan':hjd5gulsan,"hjd5gseoul":hjd5gseoul,"hjd5gincheon":hjd5gincheon,
    "hjd5gulsan":hjd5gulsan,"hjd5gdaegu":hjd5gdaegu,"hjd5ggwangju":hjd5ggwangju,"hjd5gdaejun":hjd5gdaejun,"hjd5ggyunggi":hjd5ggyunggi,"hjd5ggyungbuk":hjd5ggyungbuk,
    "hjd5gjunnam":hjd5gjunnam,"hjd5gjunbuk":hjd5gjunbuk,"hjd5gchungnam":hjd5gchungnam,"hjd5gchungbuk":hjd5gchungbuk,"hjd5gsejong":hjd5gsejong,
    "dagyo5gseoul":dagyo5gseoul,"dagyo5gincheon":dagyo5gincheon,"dagyo5gulsan":dagyo5gulsan,"dagyo5gdaegu":dagyo5gdaegu,"dagyo5ggwangju":dagyo5ggwangju,
    "dagyo5gdaejun":dagyo5gdaejun,"dagyo5ggyunggi":dagyo5ggyunggi,"dagyo5ggyungbuk":dagyo5ggyungbuk,"dagyo5gjunnam":dagyo5gjunnam,"dagyo5gjunbuk":dagyo5gjunbuk,
    "dagyo5gchungnam":dagyo5gchungnam,"dagyo5gchungbuk":dagyo5gchungbuk,"dagyo5gsejong":dagyo5gsejong,"dagyo5gsudo":dagyo5gsudo,'bigcityLTEseoul':bigcityLTEseoul,
    'bigcityLTEincheon':bigcityLTEincheon,'bigcityLTEulsan':bigcityLTEulsan,'bigcityLTEdaegu':bigcityLTEdaegu,'bigcityLTEgwangju':bigcityLTEgwangju,
    'bigcityLTEdaejun':bigcityLTEdaejun,'bigcityLTEgyunggi':bigcityLTEgyunggi,'bigcityLTEgyungbuk':bigcityLTEgyungbuk,'bigcityLTEjunnam':bigcityLTEjunnam,
    'bigcityLTEjunbuk':bigcityLTEjunbuk,'bigcityLTEchungnam':bigcityLTEchungnam,'bigcityLTEchungbuk':bigcityLTEchungbuk,'bigcityLTEsejong':bigcityLTEsejong,
    'bigcityLTEsudo':bigcityLTEsudo,'smallcityLTEseoul':smallcityLTEseoul,'smallcityLTEincheon':smallcityLTEincheon,'smallcityLTEulsan':smallcityLTEulsan,
    'smallcityLTEdaegu':smallcityLTEdaegu,'smallcityLTEgwangju':smallcityLTEgwangju,'smallcityLTEdaejun':smallcityLTEdaejun,'smallcityLTEgyunggi':smallcityLTEgyunggi,
    'smallcityLTEgyungbuk':smallcityLTEgyungbuk,'smallcityLTEjunnam':smallcityLTEjunnam,'smallcityLTEjunbuk':smallcityLTEjunbuk,
    'smallcityLTEchungnam':smallcityLTEchungnam,'smallcityLTEchungbuk':smallcityLTEchungbuk,'smallcityLTEsejong':smallcityLTEsejong,'smallcityLTEsudo':smallcityLTEsudo,
    'nongLTEseoul':nongLTEseoul,'nongLTEincheon':nongLTEincheon,'nongLTEulsan':nongLTEulsan,'nongLTEdaegu':nongLTEdaegu,'nongLTEgwangju':nongLTEgwangju,
    'nongLTEdaejun':nongLTEdaejun,'nongLTEgyunggi':nongLTEgyunggi,'nongLTEgyungbuk':nongLTEgyungbuk,'nongLTEjunnam':nongLTEjunnam,'nongLTEjunbuk':nongLTEjunbuk,
    'nongLTEchungnam':nongLTEchungnam,'nongLTEchungbuk':nongLTEchungbuk,'nongLTEsejong':nongLTEsejong,'nongLTEsudo':nongLTEsudo,'inbuildingLTEcdys':inbuildingLTEcdys,
    'inbuildingLTEdhbw':inbuildingLTEdhbw,'inbuildingLTEbhj':inbuildingLTEbhj,'inbuildingLTEtmn':inbuildingLTEtmn,'inbuildingLTEgh':inbuildingLTEgh,
    'inbuildingLTEdhjp':inbuildingLTEdhjp,'inbuildingLTEjsj':inbuildingLTEjsj,'inbuildingLTEjhcys':inbuildingLTEjhcys,'themeLTEjunnam':themeLTEjunnam,
    'themeLTEjunbuk':themeLTEjunbuk,'themeLTEchungnam':themeLTEchungnam,'themeLTEchungbuk':themeLTEchungbuk,'themeLTEsejong':themeLTEsejong,
    'sangWiFiseoul':sangWiFiseoul,'sangWiFiincheon':sangWiFiincheon,'sangWiFiulsan':sangWiFiulsan,'sangWiFidaegu':sangWiFidaegu,'sangWiFigwangju':sangWiFigwangju,
    'sangWiFidaejun':sangWiFidaejun,'sangWiFigyunggi':sangWiFigyunggi,'sangWiFigyungbuk':sangWiFigyungbuk,'sangWiFijunnam':sangWiFijunnam,
    'sangWiFijunbuk':sangWiFijunbuk,'sangWiFichungnam':sangWiFichungnam,'sangWiFichungbuk':sangWiFichungbuk,'sangWiFisejong':sangWiFisejong,
    'sangWiFisudo':sangWiFisudo,'gaeWiFiseoul':gaeWiFiseoul,'gaeWiFiincheon':gaeWiFiincheon,'gaeWiFiulsan':gaeWiFiulsan,'gaeWiFidaegu':gaeWiFidaegu,
    'gaeWiFigwangju':gaeWiFigwangju,'gaeWiFidaejun':gaeWiFidaejun,'gaeWiFigyunggi':gaeWiFigyunggi,'gaeWiFigyungbuk':gaeWiFigyungbuk,'gaeWiFijunnam':gaeWiFijunnam,
    'gaeWiFijunbuk':gaeWiFijunbuk,'gaeWiFichungnam':gaeWiFichungnam,'gaeWiFichungbuk':gaeWiFichungbuk,'gaeWiFisejong':gaeWiFisejong,'gaeWiFisudo':gaeWiFisudo,
    'weakseoul':weakseoul,'weakincheon':weakincheon,'weakulsan':weakulsan,'weakdaegu':weakdaegu,'weakgwangju':weakgwangju,'weakdaejun':weakdaejun,
    'weakgyunggi':weakgyunggi,'weakgyungbuk':weakgyungbuk,'weakjunnam':weakjunnam,'weakjunbuk':weakjunbuk,'weakchungnam':weakchungnam,'weakchungbuk':weakchungbuk,
    'weaksejong':weaksejong,'weaksudo':weaksudo,'trainsangWiFiseoul':trainsangWiFiseoul,'trainsangWiFiincheon':trainsangWiFiincheon,
    'trainsangWiFiulsan':trainsangWiFiulsan,'trainsangWiFidaegu':trainsangWiFidaegu,'trainsangWiFigwangju':trainsangWiFigwangju,
    'trainsangWiFidaejun':trainsangWiFidaejun,'trainsangWiFigyunggi':trainsangWiFigyunggi,'trainsangWiFigyungbuk':trainsangWiFigyungbuk,
    'trainsangWiFijunnam':trainsangWiFijunnam,'trainsangWiFijunbuk':trainsangWiFijunbuk,'trainsangWiFichungnam':trainsangWiFichungnam,
    'trainsangWiFichungbuk':trainsangWiFichungbuk,'trainsangWiFisejong':trainsangWiFisejong,'trainsangWiFisudo':trainsangWiFisudo,
    'traingaeWiFiseoul':traingaeWiFiseoul,'traingaeWiFiincheon':traingaeWiFiincheon,'traingaeWiFiulsan':traingaeWiFiulsan,'traingaeWiFidaegu':traingaeWiFidaegu,
    'traingaeWiFigwangju':traingaeWiFigwangju,'traingaeWiFidaejun':traingaeWiFidaejun,'traingaeWiFigyunggi':traingaeWiFigyunggi,
    'traingaeWiFigyungbuk':traingaeWiFigyungbuk,'traingaeWiFijunnam':traingaeWiFijunnam,'traingaeWiFijunbuk':traingaeWiFijunbuk,
    'traingaeWiFichungnam':traingaeWiFichungnam,'traingaeWiFichungbuk':traingaeWiFichungbuk,'traingaeWiFisejong':traingaeWiFisejong,
    'traingaeWiFisudo':traingaeWiFisudo,
    'bct5gdl':bct5gdl, 'bct5gul':bct5gul,'bct5glte':bct5glte,'bct5gsucc':bct5gsucc,'bct5gconn':bct5gconn,'bct5gjitter':bct5gjitter,
    'mct5gdl':mct5gdl, 'mct5gul':mct5gul,'mct5glte':mct5glte,'mct5gsucc':mct5gsucc,'mct5gconn':mct5gconn,'mct5gjitter':mct5gjitter,
    'ct5gdl':ct5gdl, 'ct5gul':ct5gul,'ct5glte':ct5glte,'ct5gsucc':ct5gsucc,'ct5gconn':ct5gconn,'ct5gjitter':ct5gjitter,
    'dj5gdl':dj5gdl, 'dj5gul':dj5gul,'dj5glte':dj5glte,'dj5gsucc':dj5gsucc,'dj5gconn':dj5gconn,'dj5gjitter':dj5gjitter,
    'apt5gdl':apt5gdl, 'apt5gul':apt5gul,'apt5glte':apt5glte,'apt5gsucc':apt5gsucc,'apt5gconn':apt5gconn,'apt5gjitter':apt5gjitter,
    'univ5gdl':univ5gdl, 'univ5gul':univ5gul,'univ5glte':univ5glte,'univ5gsucc':univ5gsucc,'univ5gconn':univ5gconn,'univ5gjitter':univ5gjitter,
    'traffic5gdl':traffic5gdl, 'traffic5gul':traffic5gul,'traffic5glte':traffic5glte,'traffic5gsucc':traffic5gsucc,'traffic5gconn':traffic5gconn,'traffic5gjitter':traffic5gjitter,
    'total5gdl':total5gdl, 'total5gul':total5gul,'total5glte':total5glte,'total5gsucc':total5gsucc,'total5gconn':total5gconn,'total5gjitter':total5gjitter,
    'last5g':last5g, 'lastlte':lastlte,'lastwifi':lastwifi,
    'bctltedl':bctltedl,'bctlteul':bctlteul,'bctltesucc':bctltesucc, 'bctltejitter':bctltejitter,'mctltedl':mctltedl,'mctlteul':mctlteul,'mctltesucc':mctltesucc,'mctltejitter':mctltejitter,
    'sctltedl':sctltedl,'sctlteul':sctlteul,'sctltesucc':sctltesucc,'sctltejitter':sctltejitter,'totalctltedl':totalctltedl,'totalctlteul':totalctlteul,'totalctltesucc':totalctltesucc,'totalctltejitter':totalctltejitter,
    'inbuildingltedl':inbuildingltedl,'inbuildinglteul':inbuildinglteul,'inbuildingltesucc':inbuildingltesucc,'inbuildingltejitter':inbuildingltejitter, 'themeltedl':themeltedl,'themelteul':themelteul, 'themeltesucc':themeltesucc,'themeltejitter':themeltejitter, 
    'totalltedl':totalltedl,'totallteul':totallteul, 'totalltesucc':totalltesucc, 'totalltejitter':totalltejitter, 
    'postmeas5g':postmeas5g,'postmeaslte':postmeaslte,
    'totalwifidl':totalwifidl,'totalsywifidl':totalsywifidl,'totalgbwifidl':totalgbwifidl,'totalwifiul':totalwifiul,'totalsywifiul':totalsywifiul,'totalgbwifiul':totalgbwifiul,
    }

    return context

# -------------------------------------------------------------------------------------------------
# 대상등록 페이지 - 측정대상, 측정완료, 전년도결과, 추가기입사항
# [ 고민해야 하는 사항 ]
#  - JSON형태의 컨텍스트를 만드는 코드 정규화
# -------------------------------------------------------------------------------------------------
def get_measplan_cntx(request):
    """ 측정대상등록 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
    measplan = MeasPlan.objects.all()
    
    yy_text = request.GET.get('planYear')
    yy_list = MeasPlan.objects.filter(planYear=yy_text)
    
    

    context = {'measplan':measplan, 
    'yy_text':yy_text,'yy_list':yy_list,
    }

    return context

# -------------------------------------------------------------------------------------------------
# 측정마감데이터 확인페이지
# 
#  
# -------------------------------------------------------------------------------------------------
def get_measclose_cntx(request):
    """ 측정대상등록 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
    
    measclose = LastMeasDayClose.objects.all()
    
    

    context = {'measclose':measclose,
    }

    return context


# -------------------------------------------------------------------------------------------------
# 측정완료 등록 및 수정
# -------------------------------------------------------------------------------------------------
def updage__measplan(request):
    """ 측정대상 계획을 저장하는 함수
        - 파라미터
          . request: HttpRequest
        - 반환값: 없음
    """
    measplan = MeasPlan() #빈 객체 생성
    measplan.planYear = request.POST['planYear']
    # measplan.hjd5G = request.POST['hjd5G']
    # measplan.dg5G = request.POST['dg5G']
    # measplan.cv5G = request.POST['cv5G']
    measplan.bctLTE = request.POST['bctLTE']
    measplan.mctLTE = request.POST['mctLTE']
    measplan.sctLTE = request.POST['sctLTE']
    measplan.ibLTE = request.POST['ibLTE']
    measplan.tmLTE = request.POST['tmLTE']
    measplan.cvLTE = request.POST['cvLTE']
    measplan.syWiFi = request.POST['syWiFi']
    measplan.gbWiFi = request.POST['gbWiFi']
    measplan.dsrWeak = request.POST['dsrWeak']
    measplan.yghrWeak = request.POST['yghrWeak']
    measplan.yidsWeak = request.POST['yidsWeak']
    measplan.hadrWeak = request.POST['hadrWeak']


    measplan.cvdg5G = request.POST['cvdg5G']
    measplan.cvjs5G = request.POST['cvjs5G']
    measplan.nsadg5G = request.POST['nsadg5G']
    measplan.nsahjd5G = request.POST['nsahjd5G']
    measplan.public5G = request.POST['public5G']
    measplan.sa5G = request.POST['sa5G']
    measplan.publicWiFi = request.POST['publicWiFi']
    
    measplan.totalnsa5G = int(measplan.nsadg5G)+ int(measplan.nsahjd5G)


    measplan.total5G = int(measplan.cvdg5G)+ int(measplan.cvjs5G)+ int(measplan.nsadg5G)+ int(measplan.nsahjd5G)+ int(measplan.public5G)+ int(measplan.sa5G)
    measplan.totalLTE = int(measplan.bctLTE)+ int(measplan.mctLTE)+ int(measplan.sctLTE)+ int(measplan.ibLTE)+ int(measplan.tmLTE)+ int(measplan.cvLTE)
    measplan.totalWiFi = int(measplan.syWiFi)+ int(measplan.gbWiFi)
    measplan.totalWeakArea = int(measplan.dsrWeak)+ int(measplan.yghrWeak)+ int(measplan.yidsWeak)+ int(measplan.hadrWeak)
    measplan.total = measplan.total5G + measplan.totalLTE + measplan.totalWiFi + measplan.totalWeakArea

    MeasPlan.objects.filter(planYear = measplan.planYear).delete()

    measplan.save()

    return


# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(5G)
# -------------------------------------------------------------------------------------------------
def update_measlastyear5G(request):
    """ 전년도 결과 등록 및 수정하는 함수
        - 파라미터
          . request: HttpRequest
        - 반환값: 없음
    """
    # 빈 객체를 생성한다.
    measlastyear5G = MeasLastyear5G()
    measlastyear5G.bctDL = request.POST['bctDL']
    measlastyear5G.bctUL = request.POST['bctUL']
    measlastyear5G.bctLTE = request.POST['bctLTE']
    measlastyear5G.bctsucc = request.POST['bctsucc']
    measlastyear5G.bctdelay = request.POST['bctdelay']

    measlastyear5G.mctDL = request.POST['mctDL']
    measlastyear5G.mctUL = request.POST['mctUL']
    measlastyear5G.mctLTE = request.POST['mctLTE']
    measlastyear5G.mctsucc = request.POST['mctsucc']
    measlastyear5G.mctdelay = request.POST['mctdelay']

    measlastyear5G.totalctDL = request.POST['totalctDL']
    measlastyear5G.totalctUL = request.POST['totalctUL']
    measlastyear5G.totalctLTE = request.POST['totalctLTE']
    measlastyear5G.totalctsucc = request.POST['totalctsucc']
    measlastyear5G.totalctdelay = request.POST['totalctdelay']

    measlastyear5G.djDL = request.POST['djDL']
    measlastyear5G.djUL = request.POST['djUL']
    measlastyear5G.djLTE = request.POST['djLTE']
    measlastyear5G.djsucc = request.POST['djsucc']
    measlastyear5G.djdelay = request.POST['djdelay']

    measlastyear5G.aptDL = request.POST['aptDL']
    measlastyear5G.aptUL = request.POST['aptUL']
    measlastyear5G.aptLTE = request.POST['aptLTE']
    measlastyear5G.aptsucc = request.POST['aptsucc']
    measlastyear5G.aptdelay = request.POST['aptdelay']

    measlastyear5G.univDL = request.POST['univDL']
    measlastyear5G.univUL = request.POST['univUL']
    measlastyear5G.univLTE = request.POST['univLTE']
    measlastyear5G.univsucc = request.POST['univsucc']
    measlastyear5G.univdelay = request.POST['univdelay']

    measlastyear5G.trafficDL = request.POST['trafficDL']
    measlastyear5G.trafficUL = request.POST['trafficUL']
    measlastyear5G.trafficLTE = request.POST['trafficLTE']
    measlastyear5G.trafficsucc = request.POST['trafficsucc']
    measlastyear5G.trafficdelay = request.POST['trafficdelay']

    measlastyear5G.areatotalDL = round((float(measlastyear5G.bctDL)+float(measlastyear5G.mctDL)+float(measlastyear5G.djDL)+float(measlastyear5G.aptDL)+float(measlastyear5G.univDL)+float(measlastyear5G.trafficDL))/6,1)
    measlastyear5G.areatotalUL = round((float(measlastyear5G.bctUL)+float(measlastyear5G.mctUL)+float(measlastyear5G.djUL)+float(measlastyear5G.aptUL)+float(measlastyear5G.univUL)+float(measlastyear5G.trafficUL))/6,1)
    measlastyear5G.areatotalLTE = round((float(measlastyear5G.bctLTE)+float(measlastyear5G.mctLTE)+float(measlastyear5G.djLTE)+float(measlastyear5G.aptLTE)+float(measlastyear5G.univLTE)+float(measlastyear5G.trafficLTE))/6,1)
    measlastyear5G.areatotalsucc = round((float(measlastyear5G.bctsucc)+float(measlastyear5G.mctsucc)+float(measlastyear5G.djsucc)+float(measlastyear5G.aptsucc)+float(measlastyear5G.univsucc)+float(measlastyear5G.trafficsucc))/6,1)
    measlastyear5G.areatotaldelay = round((float(measlastyear5G.bctdelay)+float(measlastyear5G.mctdelay)+float(measlastyear5G.djdelay)+float(measlastyear5G.aptdelay)+float(measlastyear5G.univdelay)+float(measlastyear5G.trafficdelay))/6,1)

    MeasLastyear5G.objects.all().delete()

    measlastyear5G.save()

    return
        

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(LTE)
# -------------------------------------------------------------------------------------------------
def update_measlastyearLTE(request):

    measlastyearLTE = MeasLastyearLTE() #빈 객체 생성
    measlastyearLTE.bctDL = request.POST['bctDL']
    measlastyearLTE.bctUL = request.POST['bctUL']

    measlastyearLTE.bctsucc = request.POST['bctsucc']
    measlastyearLTE.bctdelay = request.POST['bctdelay']

    measlastyearLTE.mctDL = request.POST['mctDL']
    measlastyearLTE.mctUL = request.POST['mctUL']

    measlastyearLTE.mctsucc = request.POST['mctsucc']
    measlastyearLTE.mctdelay = request.POST['mctdelay']

    measlastyearLTE.sctDL = request.POST['sctDL']
    measlastyearLTE.sctUL = request.POST['sctUL']

    measlastyearLTE.sctsucc = request.POST['sctsucc']
    measlastyearLTE.sctdelay = request.POST['sctdelay']

    measlastyearLTE.totalctDL = request.POST['totalctDL']
    measlastyearLTE.totalctUL = request.POST['totalctUL']

    measlastyearLTE.totalctsucc = request.POST['totalctsucc']
    measlastyearLTE.totalctdelay = request.POST['totalctdelay']

    measlastyearLTE.ibDL = request.POST['ibDL']
    measlastyearLTE.ibUL = request.POST['ibUL']

    measlastyearLTE.ibsucc = request.POST['ibsucc']
    measlastyearLTE.ibdelay = request.POST['ibdelay']

    measlastyearLTE.tmDL = request.POST['tmDL']
    measlastyearLTE.tmUL = request.POST['tmUL']

    measlastyearLTE.tmsucc = request.POST['tmsucc']
    measlastyearLTE.tmdelay = request.POST['tmdelay']

    measlastyearLTE.areatotalDL = round((float(measlastyearLTE.bctDL)+float(measlastyearLTE.mctDL)+float(measlastyearLTE.sctDL)+float(measlastyearLTE.ibDL)+float(measlastyearLTE.tmDL))/5,1)
    measlastyearLTE.areatotalUL = round((float(measlastyearLTE.bctUL)+float(measlastyearLTE.mctUL)+float(measlastyearLTE.sctUL)+float(measlastyearLTE.ibUL)+float(measlastyearLTE.tmUL))/5,1)
    measlastyearLTE.areatotalsucc = round((float(measlastyearLTE.bctsucc)+float(measlastyearLTE.mctsucc)+float(measlastyearLTE.sctsucc)+float(measlastyearLTE.ibsucc)+float(measlastyearLTE.tmsucc))/5,1)
    measlastyearLTE.areatotaldelay = round((float(measlastyearLTE.bctdelay)+float(measlastyearLTE.mctdelay)+float(measlastyearLTE.sctdelay)+float(measlastyearLTE.ibdelay)+float(measlastyearLTE.tmdelay))/5,1)

    MeasLastyearLTE.objects.all().delete()

    measlastyearLTE.save()
        
    return
  

