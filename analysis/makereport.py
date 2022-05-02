from django.db.models import Avg, Max
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone, MeasuringDayClose, TestDayClose
from analysis.models import MeasPlan, MeasResult, ReportMessage, MeasLastyear5G, MeasLastyearLTE, MeasLastyearWiFi, PostMeasure5G, PostMeasureLTE
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
    firstdate = TestDayClose.objects.last()
    lastdate = TestDayClose.objects.first()
    reportmsg = ReportMessage.objects.all()
    sregi = TestDayClose.objects.all()
    sregi5G1 = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동").count()
    sregi5G2 = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))).count()
    sregi5G3 = TestDayClose.objects.filter(networkId = "5G", mopo = "커버리지").count()
    sregi5G = TestDayClose.objects.filter(networkId = "5G").count()
    tregi5G1 = TestDayClose.objects.filter(networkId = "5G" , measdate = datetime.date.today(), mopo = "행정동").count()
    tregi5G2 = TestDayClose.objects.filter(Q(networkId = "5G")&Q(measdate = datetime.date.today())&(Q(mopo = "인빌딩")|Q(mopo = "테마"))).count()
    tregi5G3 = TestDayClose.objects.filter(networkId = "5G" , measdate = datetime.date.today(), mopo = "커버리지").count()
    tregi5G = TestDayClose.objects.filter(networkId = "5G" , measdate = datetime.date.today()).count()
    sregiLTE1 = TestDayClose.objects.filter(networkId = "LTE", address = "대도시").count()
    sregLTE2 = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시").count()
    sregiLTE3 = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌").count()
    sregiLTE4 = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩").count()
    sregiLTE5 = TestDayClose.objects.filter(networkId = "LTE", mopo = "테마").count()
    sregiLTE6 = TestDayClose.objects.filter(networkId = "LTE", mopo = "커버리지").count()
    sregiLTE = TestDayClose.objects.filter(networkId = "LTE").count()
    tregiLTE1 = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today(), address = "대도시").count()
    tregiLTE2 = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today(), address = "중소도시").count()
    tregiLTE3 = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today(), address = "농어촌").count()
    tregiLTE4 = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today(), mopo = "인빌딩").count()
    tregiLTE5 = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today(), mopo = "테마").count()
    tregiLTE6 = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today(), mopo = "커버리지").count()
    tregiLTE = TestDayClose.objects.filter(networkId = "LTE",  measdate = datetime.date.today()).count()

    sregiWiFi1 = TestDayClose.objects.filter(networkId = "WiFi", mopo = "상용").count()
    sregiWiFi2 = TestDayClose.objects.filter(networkId = "WiFi", mopo = "개방").count()
    sregiWiFi = TestDayClose.objects.filter(networkId = "WiFi").count()
    tregiWiFi1 = TestDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today(), mopo = "상용").count()
    tregiWiFi2 = TestDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today(), mopo = "개방").count()
    tregiWiFi = TestDayClose.objects.filter(networkId = "WiFi",  measdate = datetime.date.today()).count()
    
    sregiweak1 = TestDayClose.objects.filter(mopo = "취약지역", address = "등산로").count()
    sregiweak2 = TestDayClose.objects.filter(mopo = "취약지역", address = "여객항로").count()
    sregiweak3 = TestDayClose.objects.filter(mopo = "취약지역", address = "유인도서").count()
    sregiweak4 = TestDayClose.objects.filter(mopo = "취약지역", address = "해안도로").count()
    sregiweak = TestDayClose.objects.filter(mopo = "취약지역").count()
    tregiweak1 = TestDayClose.objects.filter(mopo = "취약지역",  measdate = datetime.date.today(), address = "등산로").count()
    tregiweak2 = TestDayClose.objects.filter(mopo = "취약지역",  measdate = datetime.date.today(), address = "여객항로").count()
    tregiweak3 = TestDayClose.objects.filter(mopo = "취약지역",  measdate = datetime.date.today(), address = "유인도서").count()
    tregiweak4 = TestDayClose.objects.filter(mopo = "취약지역",  measdate = datetime.date.today(), address = "해안도로").count()
    tregiweak = TestDayClose.objects.filter(mopo = "취약지역",  measdate = datetime.date.today()).count()
    
    hjd5gseoul = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "서울").count()
    hjd5gincheon = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "인천").count()
    hjd5gulsan = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "울산").count()
    hjd5gdaegu = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "대구").count()
    hjd5ggwangju = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "광주").count()
    hjd5gdaejun = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "대전").count()
    hjd5ggyunggi = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "경기").count()
    hjd5ggyungbuk = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "경북").count()
    hjd5gjunnam = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "전남").count()
    hjd5gjunbuk = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "전북").count()
    hjd5gchungnam = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "충남").count()
    hjd5gchungbuk = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "충북").count()
    hjd5gsejong = TestDayClose.objects.filter(networkId = "5G", mopo = "행정동", district = "세종").count()

    dagyo5gseoul = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "서울")).count()
    dagyo5gincheon = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "인천")).count()
    dagyo5gulsan = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "울산")).count()
    dagyo5gdaegu = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "대구")).count()
    dagyo5ggwangju = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "광주")).count()
    dagyo5gdaejun = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "대전")).count()
    dagyo5ggyunggi = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "경기")).count()
    dagyo5ggyungbuk = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "경북")).count()
    dagyo5gjunnam = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "전남")).count()
    dagyo5gjunbuk = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "전북")).count()
    dagyo5gchungnam = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "충남")).count()
    dagyo5gchungbuk = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "충북")).count()
    dagyo5gsejong = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "세종")).count()
    dagyo5gsudo = TestDayClose.objects.filter(Q(networkId = "5G")&(Q(mopo = "인빌딩")|Q(mopo = "테마"))&Q(district = "수도권")).count()

    bigcityLTEseoul = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "서울").count()
    bigcityLTEincheon = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "인천").count()
    bigcityLTEulsan = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "울산").count()
    bigcityLTEdaegu = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "대구").count()
    bigcityLTEgwangju = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "광주").count()
    bigcityLTEdaejun = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "대전").count()
    bigcityLTEgyunggi = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "경기").count()
    bigcityLTEgyungbuk = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "경북").count()
    bigcityLTEjunnam = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "전남").count()
    bigcityLTEjunbuk = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "전북").count()
    bigcityLTEchungnam = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "충남").count()
    bigcityLTEchungbuk = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "충북").count()
    bigcityLTEsejong = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "세종").count()
    bigcityLTEsudo = TestDayClose.objects.filter(networkId = "LTE", address = "대도시", district = "수도권").count()

    smallcityLTEseoul = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "서울").count()
    smallcityLTEincheon = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "인천").count()
    smallcityLTEulsan = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "울산").count()
    smallcityLTEdaegu = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "대구").count()
    smallcityLTEgwangju = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "광주").count()
    smallcityLTEdaejun = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "대전").count()
    smallcityLTEgyunggi = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "경기").count()
    smallcityLTEgyungbuk = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "경북").count()
    smallcityLTEjunnam = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "전남").count()
    smallcityLTEjunbuk = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "전북").count()
    smallcityLTEchungnam = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "충남").count()
    smallcityLTEchungbuk = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "충북").count()
    smallcityLTEsejong = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "세종").count()
    smallcityLTEsudo = TestDayClose.objects.filter(networkId = "LTE", address = "중소도시", district = "수도권").count()

    
    nongLTEseoul = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "서울").count()
    nongLTEincheon = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "인천").count()
    nongLTEulsan = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "울산").count()
    nongLTEdaegu = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "대구").count()
    nongLTEgwangju = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "광주").count()
    nongLTEdaejun = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "대전").count()
    nongLTEgyunggi = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "경기").count()
    nongLTEgyungbuk = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "경북").count()
    nongLTEjunnam = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "전남").count()
    nongLTEjunbuk = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "전북").count()
    nongLTEchungnam = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "충남").count()
    nongLTEchungbuk = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "충북").count()
    nongLTEsejong = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "세종").count()
    nongLTEsudo = TestDayClose.objects.filter(networkId = "LTE", address = "농어촌", district = "수도권").count()

    inbuildingLTEcdys = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "철도역사").count()
    inbuildingLTEdhbw = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "대형병원").count()
    inbuildingLTEbhj = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "백화점").count()
    inbuildingLTEtmn = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "터미널").count()
    inbuildingLTEgh = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "공항").count()
    inbuildingLTEdhjp = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "대형점포").count()
    inbuildingLTEjsj = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "전시장").count()
    inbuildingLTEjhcys = TestDayClose.objects.filter(networkId = "LTE", mopo = "인빌딩", address = "지하철역사").count()

    themeLTEjunnam = TestDayClose.objects.filter(networkId = "LTE", mopo = "테마", address = "대학교").count()
    themeLTEjunbuk = TestDayClose.objects.filter(networkId = "LTE", mopo = "테마", address = "놀이공원").count()
    themeLTEchungnam = TestDayClose.objects.filter(networkId = "LTE", mopo = "테마", address = "주요거리").count()
    themeLTEchungbuk = TestDayClose.objects.filter(networkId = "LTE", mopo = "테마", address = "전통시장").count()
    themeLTEsejong = TestDayClose.objects.filter(networkId = "LTE", mopo = "테마", address = "지하철노선").count()
    
    sangWiFiseoul = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "서울", plus = "").count()
    sangWiFiincheon = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "인천", plus = "").count()
    sangWiFiulsan = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "울산", plus = "").count()
    sangWiFidaegu = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대구", plus = "").count()
    sangWiFigwangju = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "광주", plus = "").count()
    sangWiFidaejun = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대전", plus = "").count()
    sangWiFigyunggi = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경기", plus = "").count()
    sangWiFigyungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경북", plus = "").count()
    sangWiFijunnam = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전남", plus = "").count()
    sangWiFijunbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전북", plus = "").count()
    sangWiFichungnam = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충남", plus = "").count()
    sangWiFichungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충북", plus = "").count()
    sangWiFisejong = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "세종", plus = "").count()
    sangWiFisudo = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "수도권", plus = "").count()

    trainsangWiFiseoul = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "서울", plus = "지하철").count()
    trainsangWiFiincheon = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "인천", plus = "지하철").count()
    trainsangWiFiulsan = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "울산", plus = "지하철").count()
    trainsangWiFidaegu = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대구", plus = "지하철").count()
    trainsangWiFigwangju = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "광주", plus = "지하철").count()
    trainsangWiFidaejun = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "대전", plus = "지하철").count()
    trainsangWiFigyunggi = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경기", plus = "지하철").count()
    trainsangWiFigyungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "경북", plus = "지하철").count()
    trainsangWiFijunnam = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전남", plus = "지하철").count()
    trainsangWiFijunbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "전북", plus = "지하철").count()
    trainsangWiFichungnam = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충남", plus = "지하철").count()
    trainsangWiFichungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "충북", plus = "지하철").count()
    trainsangWiFisejong = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "세종", plus = "지하철").count()
    trainsangWiFisudo = TestDayClose.objects.filter(networkId = "WiFi",address = "상용", district = "수도권", plus = "지하철").count()

    gaeWiFiseoul = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "서울", plus = "").count()
    gaeWiFiincheon = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "인천", plus = "").count()
    gaeWiFiulsan = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "울산", plus = "").count()
    gaeWiFidaegu = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대구", plus = "").count()
    gaeWiFigwangju = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "광주", plus = "").count()
    gaeWiFidaejun = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대전", plus = "").count()
    gaeWiFigyunggi = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경기", plus = "").count()
    gaeWiFigyungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경북", plus = "").count()
    gaeWiFijunnam = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전남", plus = "").count()
    gaeWiFijunbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전북", plus = "").count()
    gaeWiFichungnam = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충남", plus = "").count()
    gaeWiFichungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충북", plus = "").count()
    gaeWiFisejong = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "세종", plus = "").count()
    gaeWiFisudo = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "수도권", plus = "").count()

    traingaeWiFiseoul = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "서울", plus = "지하철").count()
    traingaeWiFiincheon = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "인천", plus = "지하철").count()
    traingaeWiFiulsan = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "울산", plus = "지하철").count()
    traingaeWiFidaegu = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대구", plus = "지하철").count()
    traingaeWiFigwangju = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "광주", plus = "지하철").count()
    traingaeWiFidaejun = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "대전", plus = "지하철").count()
    traingaeWiFigyunggi = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경기", plus = "지하철").count()
    traingaeWiFigyungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "경북", plus = "지하철").count()
    traingaeWiFijunnam = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전남", plus = "지하철").count()
    traingaeWiFijunbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "전북", plus = "지하철").count()
    traingaeWiFichungnam = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충남", plus = "지하철").count()
    traingaeWiFichungbuk = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "충북", plus = "지하철").count()
    traingaeWiFisejong = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "세종", plus = "지하철").count()
    traingaeWiFisudo = TestDayClose.objects.filter(networkId = "WiFi",address = "개방", district = "수도권", plus = "지하철").count()

    weakseoul = TestDayClose.objects.filter(mopo = "취약지역", district = "서울").count()
    weakincheon = TestDayClose.objects.filter(mopo = "취약지역", district = "인천").count()
    weakulsan = TestDayClose.objects.filter(mopo = "취약지역", district = "울산").count()
    weakdaegu = TestDayClose.objects.filter(mopo = "취약지역", district = "대구").count()
    weakgwangju = TestDayClose.objects.filter(mopo = "취약지역", district = "광주").count()
    weakdaejun = TestDayClose.objects.filter(mopo = "취약지역", district = "대전").count()
    weakgyunggi = TestDayClose.objects.filter(mopo = "취약지역", district = "경기").count()
    weakgyungbuk = TestDayClose.objects.filter(mopo = "취약지역", district = "경북").count()
    weakjunnam = TestDayClose.objects.filter(mopo = "취약지역", district = "전남").count()
    weakjunbuk = TestDayClose.objects.filter(mopo = "취약지역", district = "전북").count()
    weakchungnam = TestDayClose.objects.filter(mopo = "취약지역", district = "충남").count()
    weakchungbuk = TestDayClose.objects.filter(mopo = "취약지역", district = "충북").count()
    weaksejong = TestDayClose.objects.filter(mopo = "취약지역", district = "세종").count()
    weaksudo = TestDayClose.objects.filter(mopo = "취약지역", district = "수도권").count()
    
#작년 측정결과(과년도로 변경 예정)
    last5g = MeasLastyear5G.objects.all()
    lastlte = MeasLastyearLTE.objects.all()
    lastwifi = MeasLastyearWiFi.objects.all()
#5G 측정결과
    try:
        bct5gdl = round(TestDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        bct5gdl = ""
    try:
        bct5gul =  round(TestDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        bct5gul = ""
    try:
        bct5glte =  round(TestDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        bct5glte = ""
    try:
        bct5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        bct5gsucc = ""
    try:
        bct5gconn =  round(TestDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        bct5gconn = ""
    try:
        bct5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", address="대도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        bct5gjitter = ""
    
    try:
        mct5gdl =  round(TestDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        mct5gdl = ""
    try:
        mct5gul =  round(TestDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        mct5gul = ""
    try:
        mct5glte =  round(TestDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        mct5glte = ""
    try:
        mct5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        mct5gsucc = ""
    try:
        mct5gconn =  round(TestDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        mct5gconn = ""
    try:
        mct5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", address="중소도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        mct5gjitter = ""

    try:
        ct5gdl =  round(TestDayClose.objects.filter(networkId = "5G",mopo="행정동").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        ct5gdl = ""
    try:
        ct5gul =  round(TestDayClose.objects.filter(networkId = "5G", mopo="행정동").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        ct5gul = ""
    try:
        ct5glte =  round(TestDayClose.objects.filter(networkId = "5G", mopo="행정동").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        ct5glte = ""
    try:
        ct5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", mopo="행정동").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        ct5gsucc = ""
    try:
        ct5gconn =  round(TestDayClose.objects.filter(networkId = "5G", mopo="행정동").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        ct5gconn = ""
    try:
        ct5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", mopo="행정동").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        ct5gjitter = ""

    try:
        dj5gdl =  round(TestDayClose.objects.filter(networkId = "5G",plus="다중이용시설").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        dj5gdl = ""
    try:
        dj5gul =  round(TestDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        dj5gul = ""
    try:
        dj5glte =  round(TestDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        dj5glte = ""
    try:
        dj5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        dj5gsucc = ""
    try:
        dj5gconn =  round(TestDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        dj5gconn = ""
    try:
        dj5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", plus="다중이용시설").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        dj5gjitter = ""
    
    try:
        apt5gdl =  round(TestDayClose.objects.filter(networkId = "5G",plus="아파트").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        apt5gdl = ""
    try:
        apt5gul =  round(TestDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        apt5gul = ""
    try:
        apt5glte =  round(TestDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        apt5glte = ""
    try:
        apt5gsucc = round(TestDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        apt5gsucc = ""
    try:
        apt5gconn =  round(TestDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        apt5gconn = ""
    try:
        apt5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", plus="아파트").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        apt5gjitter = ""

    try:
        univ5gdl =  round(TestDayClose.objects.filter(networkId = "5G",plus="대학교").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        univ5gdl = ""
    try:
        univ5gul =  round(TestDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        univ5gul = ""
    try:
        univ5glte =  round(TestDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        univ5glte = ""
    try:
        univ5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        univ5gsucc = ""
    try:
        univ5gconn =  round(TestDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        univ5gconn = ""
    try:
        univ5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", plus="대학교").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        univ5gjitter = ""

    try:
        traffic5gdl =  round(TestDayClose.objects.filter(networkId = "5G",plus="교통인프라").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        traffic5gdl = ""
    try:
        traffic5gul =  round(TestDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        traffic5gul = ""
    try:
        traffic5glte =  round(TestDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        traffic5glte = ""
    try:
        traffic5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        traffic5gsucc = ""
    try:
        traffic5gconn =  round(TestDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        traffic5gconn = ""
    try:
        traffic5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", plus="교통인프라").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        traffic5gjitter = ""

    try:
        total5gdl = round(TestDayClose.objects.filter(networkId = "5G").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        total5gdl = ""
    try:
        total5gul =  round(TestDayClose.objects.filter(networkId = "5G").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        total5gul = ""
    try:
        total5glte =  round(TestDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("lte_percent"))["lte_percent__avg"],1)
    except:
        total5glte = ""
    try:
        total5gsucc =  round(TestDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        total5gsucc = ""
    try:
        total5gconn =  round(TestDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("connect_time"))["connect_time__avg"],1)
    except:
        total5gconn = ""
    try:
        total5gjitter =  round(TestDayClose.objects.filter(networkId = "5G", ).aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        total5gjitter = ""

#LTE 측정결과

    try:
        bctltedl =  round(TestDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        bctltedl = ""
    try:
        bctlteul =  round(TestDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        bctlteul = ""
    try:
        bctltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        bctltesucc = ""
    try:
        bctltejitter =  round(TestDayClose.objects.filter(networkId = "LTE", address="대도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        bctltejitter = ""

    try:
        mctltedl =  round(TestDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        mctltedl = ""
    try:
        mctlteul =  round(TestDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        mctlteul = ""
    try:
        mctltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        mctltesucc = ""
    try:
        mctltejitter =  round(TestDayClose.objects.filter(networkId = "LTE", address="중소도시").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        mctltejitter = ""

    try:
        sctltedl =  round(TestDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        sctltedl = ""
    try:
        sctlteul =  round(TestDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        sctlteul = ""
    try:
        sctltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        sctltesucc = ""
    try:
        sctltejitter =  round(TestDayClose.objects.filter(networkId = "LTE", address="농어촌").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        sctltejitter = ""

    try:
        totalctltedl =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="행정동").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalctltedl = ""
    try:
        totalctlteul =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="행정동").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalctlteul = ""
    try:
        totalctltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="행정동").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        totalctltesucc = ""
    try:
        totalctltejitter =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="행정동").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        totalctltejitter = ""

    try:
        inbuildingltedl =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="인빌딩").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        inbuildingltedl = ""
    try:
        inbuildinglteul =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="인빌딩").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        inbuildinglteul = ""
    try:
        inbuildingltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="인빌딩").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        inbuildingltesucc = ""
    try:
        inbuildingltejitter =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="인빌딩").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        inbuildingltejitter = ""

    try:
        themeltedl =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        themeltedl = ""
    try:
        themelteul =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        themelteul = ""
    try:
        themeltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        themeltesucc = ""
    try:
        themeltejitter = round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        themeltejitter = ""

    try:
        totalltedl =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalltedl = ""
    try:
        totallteul =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totallteul = ""
    try:
        totalltesucc =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("success_rate"))["success_rate__avg"],1)
    except:
        totalltesucc = ""
    try:
        totalltejitter =  round(TestDayClose.objects.filter(networkId = "LTE", mopo="테마").aggregate(Avg("udpJitter"))["udpJitter__avg"],1)
    except:
        totalltejitter = ""

    
#wifi 측정결과(종합)
    try:
        totalwifidl = round(TestDayClose.objects.filter(networkId = "WiFi").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalwifidl = ""
    try:
        totalsywifidl = round(TestDayClose.objects.filter(networkId = "WiFi", address = "상용").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalsywifidl = ""
    try:
        totalgbwifidl = round(TestDayClose.objects.filter(networkId = "WiFi", address = "개방").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalgbwifidl = ""
    try:
        totalwifiul = round(TestDayClose.objects.filter(networkId = "WiFi").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalwifiul = ""
    try:
        totalsywifiul = round(TestDayClose.objects.filter(networkId = "WiFi", address = "상용").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalsywifiul = ""
    try:
        totalgbwifiul = round(TestDayClose.objects.filter(networkId = "WiFi", address = "개방").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalgbwifiul = ""
#wifi 측정결과(센터별)
#wifi 측정결과(지역별)
    context = {
    'regi':regi, 'reportmsg':reportmsg,'sregi':sregi,'firstdate':firstdate,'lastdate':lastdate,
    'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G':tregi5G,'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G':sregi5G,
    'sregiLTE1':sregiLTE1, 'sregiLTE2':sregLTE2,'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,'sregiLTE':sregiLTE, 
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
def get_measresult_cntx(request):
    """ 측정대상등록 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
    measplan = MeasPlan.objects.all()
    
    yy_text = request.GET.get('planYear')
    yy_list = MeasPlan.objects.filter(planYear=yy_text)
    
    sregi = MeasResult.objects.all()

    sregi5G1 = MeasResult.objects.filter(networkId = "5G", area = "행정동").count()
    sregi5G2 = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라").count()
    sregi5G3 = MeasResult.objects.filter(networkId = "5G", area = "커버리지").count()
    sregi5G = MeasResult.objects.filter(networkId = "5G").count()
    tregi5G1 = MeasResult.objects.filter(networkId = "5G", date = datetime.date.today(), area = "행정동").count()
    tregi5G2 = MeasResult.objects.filter(networkId = "5G", date = datetime.date.today(), area = "다중이용시설/교통인프라").count()
    tregi5G3 = MeasResult.objects.filter(networkId = "5G", date = datetime.date.today(), area = "커버리지").count()
    tregi5G = MeasResult.objects.filter(networkId = "5G", date = datetime.date.today()).count()

    sregiLTE1 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시").count()
    sregLTE2 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시").count()
    sregiLTE3 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌").count()
    sregiLTE4 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩").count()
    sregiLTE5 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마").count()
    sregiLTE6 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "커버리지").count()
    sregiLTE = MeasResult.objects.filter(networkId = "LTE").count()
    tregiLTE1 = MeasResult.objects.filter(networkId = "LTE", date = datetime.date.today(), molph_level0 = "대도시").count()
    tregiLTE2 = MeasResult.objects.filter(networkId = "LTE", date = datetime.date.today(), molph_level0 = "중소도시").count()
    tregiLTE3 = MeasResult.objects.filter(networkId = "LTE", date = datetime.date.today(), molph_level0 = "농어촌").count()
    tregiLTE4 = MeasResult.objects.filter(networkId = "LTE", date = datetime.date.today(), molph_level0 = "인빌딩").count()
    tregiLTE5 = MeasResult.objects.filter(networkId = "LTE", date = datetime.date.today(), molph_level0 = "테마").count()
    tregiLTE6 = MeasResult.objects.filter(networkId = "LTE", date = datetime.date.today(), molph_level0 = "커버리지").count()
    tregiLTE = MeasResult.objects.filter(networkId = "LTE").count()

    sregiWiFi1 = MeasResult.objects.filter(networkId = "WiFi", area = "상용").count()
    sregiWiFi2 = MeasResult.objects.filter(networkId = "WiFi", area = "개방").count()
    sregiWiFi = MeasResult.objects.filter(networkId = "WiFi").count()
    tregiWiFi1 = MeasResult.objects.filter(networkId = "WiFi", date = datetime.date.today(), area = "상용").count()
    tregiWiFi2 = MeasResult.objects.filter(networkId = "WiFi", date = datetime.date.today(), area = "개방").count()
    tregiWiFi = MeasResult.objects.filter(networkId = "WiFi").count()
    
    sregiweak1 = MeasResult.objects.filter(networkId = "품질취약지역", area = "등산로").count()
    sregiweak2 = MeasResult.objects.filter(networkId = "품질취약지역", area = "여객항로").count()
    sregiweak3 = MeasResult.objects.filter(networkId = "품질취약지역", area = "유인도서").count()
    sregiweak4 = MeasResult.objects.filter(networkId = "품질취약지역", area = "해안도로").count()
    sregiweak = MeasResult.objects.filter(networkId = "품질취약지역").count()
    tregiweak1 = MeasResult.objects.filter(networkId = "품질취약지역", date = datetime.date.today(), area = "등산로").count()
    tregiweak2 = MeasResult.objects.filter(networkId = "품질취약지역", date = datetime.date.today(), area = "여객항로").count()
    tregiweak3 = MeasResult.objects.filter(networkId = "품질취약지역", date = datetime.date.today(), area = "유인도서").count()
    tregiweak4 = MeasResult.objects.filter(networkId = "품질취약지역", date = datetime.date.today(), area = "해안도로").count()
    tregiweak = MeasResult.objects.filter(networkId = "품질취약지역").count()

    reportmsg = ReportMessage.objects.all()

    measlastyear5G = MeasLastyear5G.objects.all()
    measlastyearLTE = MeasLastyearLTE.objects.all()

    context = {'measplan':measplan, 'sregi':sregi, 'reportmsg':reportmsg, 'measlastyear5G':measlastyear5G, 'measlastyearLTE':measlastyearLTE,
    'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G':tregi5G,'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G':sregi5G,
    'sregiLTE1':sregiLTE1, 'sregiLTE2':sregLTE2,'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,
    'sregiLTE':sregiLTE, 'tregiLTE1':tregiLTE1,'tregiLTE2':tregiLTE2, 'tregiLTE3':tregiLTE3,'tregiLTE4':tregiLTE4, 'tregiLTE5':tregiLTE5,'tregiLTE6':tregiLTE6,
    'tregiLTE':tregiLTE,'sregiWiFi1':sregiWiFi1,'sregiWiFi2':sregiWiFi2,'sregiWiFi':sregiWiFi,'tregiWiFi1':tregiWiFi1,'tregiWiFi2':tregiWiFi2,'tregiWiFi':tregiWiFi,
    'sregiweak1':sregiweak1,'sregiweak2':sregiweak2,'sregiweak3':sregiweak3,'sregiweak4':sregiweak4,'sregiweak':sregiweak,'tregiweak1':tregiweak1,
    'tregiweak2':tregiweak2,'tregiweak3':tregiweak3,'tregiweak4':tregiweak4,'tregiweak':tregiweak,
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
    
    measclose = TestDayClose.objects.all()
    
    

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
    measplan.hjd5G = request.POST['hjd5G']
    measplan.dg5G = request.POST['dg5G']
    measplan.cv5G = request.POST['cv5G']
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
    measplan.total5G = int(measplan.hjd5G)+ int(measplan.dg5G)+ int(measplan.cv5G)
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
  

