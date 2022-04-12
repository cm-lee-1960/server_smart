# from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
# from monitor.models import Phone
# from .models import MeasPlan, MeasResult, ReportMessage, MeasLastyear5G, MeasLastyearLTE
# import pandas as pd
# import datetime
# from django.db.models import Sum


from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone
from analysis.models import MeasPlan, MeasResult, ReportMessage, MeasLastyear5G, MeasLastyearLTE
import pandas as pd
import datetime
from django.db.models import Sum

###################################################################################################
# 일일보고 및 대상등록 관련 모듈
# -------------------------------------------------------------------------------------------------
# 2022-03-23 - 모듈 정리 및 주석 추가
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 일일보고 페이지
# - 레포트 현황 페이지에 보여질 데이터를 가져와서 JSON으로 묶어서 반환한다.
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
    regi = MeasPlan.objects.filter(planYear = "2022")
    firstdate = MeasResult.objects.last()
    lastdate = MeasResult.objects.first()
    reportmsg = ReportMessage.objects.all()
    sregi = MeasResult.objects.all()
    sregi5G1 = MeasResult.objects.filter(networkId = "5G", area = "행정동").count()
    sregi5G2 = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라").count()
    sregi5G3 = MeasResult.objects.filter(networkId = "5G", area = "커버리지").count()
    sregi5G = MeasResult.objects.filter(networkId = "5G").count()
    tregi5G1 = MeasResult.objects.filter(networkId = "5G" , date = datetime.date.today(), area = "행정동").count()
    tregi5G2 = MeasResult.objects.filter(networkId = "5G" , date = datetime.date.today(), area = "다중이용시설/교통인프라").count()
    tregi5G3 = MeasResult.objects.filter(networkId = "5G" , date = datetime.date.today(), area = "커버리지").count()
    tregi5G = MeasResult.objects.filter(networkId = "5G" , date = datetime.date.today()).count()
    sregiLTE1 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시").count()
    sregLTE2 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시").count()
    sregiLTE3 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌").count()
    sregiLTE4 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩").count()
    sregiLTE5 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마").count()
    sregiLTE6 = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "커버리지").count()
    sregiLTE = MeasResult.objects.filter(networkId = "LTE").count()
    tregiLTE1 = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today(), molph_level0 = "대도시").count()
    tregiLTE2 = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today(), molph_level0 = "중소도시").count()
    tregiLTE3 = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today(), molph_level0 = "농어촌").count()
    tregiLTE4 = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today(), molph_level0 = "인빌딩").count()
    tregiLTE5 = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today(), molph_level0 = "테마").count()
    tregiLTE6 = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today(), molph_level0 = "커버리지").count()
    tregiLTE = MeasResult.objects.filter(networkId = "LTE",  date = datetime.date.today()).count()

    sregiWiFi1 = MeasResult.objects.filter(networkId = "WiFi", area = "상용").count()
    sregiWiFi2 = MeasResult.objects.filter(networkId = "WiFi", area = "개방").count()
    sregiWiFi = MeasResult.objects.filter(networkId = "WiFi").count()
    tregiWiFi1 = MeasResult.objects.filter(networkId = "WiFi",  date = datetime.date.today(), area = "상용").count()
    tregiWiFi2 = MeasResult.objects.filter(networkId = "WiFi",  date = datetime.date.today(), area = "개방").count()
    tregiWiFi = MeasResult.objects.filter(networkId = "WiFi",  date = datetime.date.today()).count()
    
    sregiweak1 = MeasResult.objects.filter(networkId = "품질취약지역", area = "등산로").count()
    sregiweak2 = MeasResult.objects.filter(networkId = "품질취약지역", area = "여객항로").count()
    sregiweak3 = MeasResult.objects.filter(networkId = "품질취약지역", area = "유인도서").count()
    sregiweak4 = MeasResult.objects.filter(networkId = "품질취약지역", area = "해안도로").count()
    sregiweak = MeasResult.objects.filter(networkId = "품질취약지역").count()
    tregiweak1 = MeasResult.objects.filter(networkId = "품질취약지역",  date = datetime.date.today(), area = "등산로").count()
    tregiweak2 = MeasResult.objects.filter(networkId = "품질취약지역",  date = datetime.date.today(), area = "여객항로").count()
    tregiweak3 = MeasResult.objects.filter(networkId = "품질취약지역",  date = datetime.date.today(), area = "유인도서").count()
    tregiweak4 = MeasResult.objects.filter(networkId = "품질취약지역",  date = datetime.date.today(), area = "해안도로").count()
    tregiweak = MeasResult.objects.filter(networkId = "품질취약지역",  date = datetime.date.today()).count()
    
    hjd5gseoul = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "서울").count()
    hjd5gincheon = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "인천").count()
    hjd5gulsan = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "울산").count()
    hjd5gdaegu = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "대구").count()
    hjd5ggwangju = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "광주").count()
    hjd5gdaejun = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "대전").count()
    hjd5ggyunggi = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "경기").count()
    hjd5ggyungbuk = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "경북").count()
    hjd5gjunnam = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "전남").count()
    hjd5gjunbuk = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "전북").count()
    hjd5gchungnam = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "충남").count()
    hjd5gchungbuk = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "충북").count()
    hjd5gsejong = MeasResult.objects.filter(networkId = "5G", area = "행정동", district = "세종").count()

    dagyo5gseoul = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "서울").count()
    dagyo5gincheon = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "인천").count()
    dagyo5gulsan = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "울산").count()
    dagyo5gdaegu = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "대구").count()
    dagyo5ggwangju = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "광주").count()
    dagyo5gdaejun = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "대전").count()
    dagyo5ggyunggi = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "경기").count()
    dagyo5ggyungbuk = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "경북").count()
    dagyo5gjunnam = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "전남").count()
    dagyo5gjunbuk = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "전북").count()
    dagyo5gchungnam = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "충남").count()
    dagyo5gchungbuk = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "충북").count()
    dagyo5gsejong = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "세종").count()
    dagyo5gsudo = MeasResult.objects.filter(networkId = "5G", area = "다중이용시설/교통인프라", district = "수도권").count()

    bigcityLTEseoul = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "서울").count()
    bigcityLTEincheon = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "인천").count()
    bigcityLTEulsan = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "울산").count()
    bigcityLTEdaegu = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "대구").count()
    bigcityLTEgwangju = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "광주").count()
    bigcityLTEdaejun = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "대전").count()
    bigcityLTEgyunggi = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "경기").count()
    bigcityLTEgyungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "경북").count()
    bigcityLTEjunnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "전남").count()
    bigcityLTEjunbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "전북").count()
    bigcityLTEchungnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "충남").count()
    bigcityLTEchungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "충북").count()
    bigcityLTEsejong = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "세종").count()
    bigcityLTEsudo = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "대도시", district = "수도권").count()

    smallcityLTEseoul = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "서울").count()
    smallcityLTEincheon = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "인천").count()
    smallcityLTEulsan = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "울산").count()
    smallcityLTEdaegu = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "대구").count()
    smallcityLTEgwangju = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "광주").count()
    smallcityLTEdaejun = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "대전").count()
    smallcityLTEgyunggi = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "경기").count()
    smallcityLTEgyungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "경북").count()
    smallcityLTEjunnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "전남").count()
    smallcityLTEjunbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "전북").count()
    smallcityLTEchungnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "충남").count()
    smallcityLTEchungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "충북").count()
    smallcityLTEsejong = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "세종").count()
    smallcityLTEsudo = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "중소도시", district = "수도권").count()

    
    nongLTEseoul = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "서울").count()
    nongLTEincheon = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "인천").count()
    nongLTEulsan = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "울산").count()
    nongLTEdaegu = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "대구").count()
    nongLTEgwangju = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "광주").count()
    nongLTEdaejun = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "대전").count()
    nongLTEgyunggi = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "경기").count()
    nongLTEgyungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "경북").count()
    nongLTEjunnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "전남").count()
    nongLTEjunbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "전북").count()
    nongLTEchungnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "충남").count()
    nongLTEchungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "충북").count()
    nongLTEsejong = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "세종").count()
    nongLTEsudo = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "농어촌", district = "수도권").count()

    inbuildingLTEcdys = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "철도역사").count()
    inbuildingLTEdhbw = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "대형병원").count()
    inbuildingLTEbhj = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "백화점").count()
    inbuildingLTEtmn = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "터미널").count()
    inbuildingLTEgh = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "공항").count()
    inbuildingLTEdhjp = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "대형점포").count()
    inbuildingLTEjsj = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "전시장").count()
    inbuildingLTEjhcys = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "인빌딩", molph_level1 = "지하철역사").count()

    themeLTEjunnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마", molph_level1 = "대학교").count()
    themeLTEjunbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마", molph_level1 = "놀이공원").count()
    themeLTEchungnam = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마", molph_level1 = "주요거리").count()
    themeLTEchungbuk = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마", molph_level1 = "전통시장").count()
    themeLTEsejong = MeasResult.objects.filter(networkId = "LTE", molph_level0 = "테마", molph_level1 = "지하철노선").count()
    
    sangWiFiseoul = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "서울", molph_level0 = "").count()
    sangWiFiincheon = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "인천", molph_level0 = "").count()
    sangWiFiulsan = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "울산", molph_level0 = "").count()
    sangWiFidaegu = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "대구", molph_level0 = "").count()
    sangWiFigwangju = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "광주", molph_level0 = "").count()
    sangWiFidaejun = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "대전", molph_level0 = "").count()
    sangWiFigyunggi = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "경기", molph_level0 = "").count()
    sangWiFigyungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "경북", molph_level0 = "").count()
    sangWiFijunnam = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "전남", molph_level0 = "").count()
    sangWiFijunbuk = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "전북", molph_level0 = "").count()
    sangWiFichungnam = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "충남", molph_level0 = "").count()
    sangWiFichungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "충북", molph_level0 = "").count()
    sangWiFisejong = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "세종", molph_level0 = "").count()
    sangWiFisudo = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "수도권", molph_level0 = "").count()

    trainsangWiFiseoul = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "서울", molph_level0 = "지하철").count()
    trainsangWiFiincheon = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "인천", molph_level0 = "지하철").count()
    trainsangWiFiulsan = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "울산", molph_level0 = "지하철").count()
    trainsangWiFidaegu = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "대구", molph_level0 = "지하철").count()
    trainsangWiFigwangju = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "광주", molph_level0 = "지하철").count()
    trainsangWiFidaejun = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "대전", molph_level0 = "지하철").count()
    trainsangWiFigyunggi = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "경기", molph_level0 = "지하철").count()
    trainsangWiFigyungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "경북", molph_level0 = "지하철").count()
    trainsangWiFijunnam = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "전남", molph_level0 = "지하철").count()
    trainsangWiFijunbuk = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "전북", molph_level0 = "지하철").count()
    trainsangWiFichungnam = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "충남", molph_level0 = "지하철").count()
    trainsangWiFichungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "충북", molph_level0 = "지하철").count()
    trainsangWiFisejong = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "세종", molph_level0 = "지하철").count()
    trainsangWiFisudo = MeasResult.objects.filter(networkId = "WiFi", area = "상용", district = "수도권", molph_level0 = "지하철").count()

    gaeWiFiseoul = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "서울", molph_level0 = "").count()
    gaeWiFiincheon = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "인천", molph_level0 = "").count()
    gaeWiFiulsan = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "울산", molph_level0 = "").count()
    gaeWiFidaegu = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "대구", molph_level0 = "").count()
    gaeWiFigwangju = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "광주", molph_level0 = "").count()
    gaeWiFidaejun = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "대전", molph_level0 = "").count()
    gaeWiFigyunggi = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "경기", molph_level0 = "").count()
    gaeWiFigyungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "경북", molph_level0 = "").count()
    gaeWiFijunnam = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "전남", molph_level0 = "").count()
    gaeWiFijunbuk = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "전북", molph_level0 = "").count()
    gaeWiFichungnam = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "충남", molph_level0 = "").count()
    gaeWiFichungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "충북", molph_level0 = "").count()
    gaeWiFisejong = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "세종", molph_level0 = "").count()
    gaeWiFisudo = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "수도권", molph_level0 = "").count()

    traingaeWiFiseoul = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "서울", molph_level0 = "지하철").count()
    traingaeWiFiincheon = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "인천", molph_level0 = "지하철").count()
    traingaeWiFiulsan = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "울산", molph_level0 = "지하철").count()
    traingaeWiFidaegu = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "대구", molph_level0 = "지하철").count()
    traingaeWiFigwangju = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "광주", molph_level0 = "지하철").count()
    traingaeWiFidaejun = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "대전", molph_level0 = "지하철").count()
    traingaeWiFigyunggi = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "경기", molph_level0 = "지하철").count()
    traingaeWiFigyungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "경북", molph_level0 = "지하철").count()
    traingaeWiFijunnam = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "전남", molph_level0 = "지하철").count()
    traingaeWiFijunbuk = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "전북", molph_level0 = "지하철").count()
    traingaeWiFichungnam = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "충남", molph_level0 = "지하철").count()
    traingaeWiFichungbuk = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "충북", molph_level0 = "지하철").count()
    traingaeWiFisejong = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "세종", molph_level0 = "지하철").count()
    traingaeWiFisudo = MeasResult.objects.filter(networkId = "WiFi", area = "개방", district = "수도권", molph_level0 = "지하철").count()

    weakseoul = MeasResult.objects.filter(networkId = "품질취약지역", district = "서울").count()
    weakincheon = MeasResult.objects.filter(networkId = "품질취약지역", district = "인천").count()
    weakulsan = MeasResult.objects.filter(networkId = "품질취약지역", district = "울산").count()
    weakdaegu = MeasResult.objects.filter(networkId = "품질취약지역", district = "대구").count()
    weakgwangju = MeasResult.objects.filter(networkId = "품질취약지역", district = "광주").count()
    weakdaejun = MeasResult.objects.filter(networkId = "품질취약지역", district = "대전").count()
    weakgyunggi = MeasResult.objects.filter(networkId = "품질취약지역", district = "경기").count()
    weakgyungbuk = MeasResult.objects.filter(networkId = "품질취약지역", district = "경북").count()
    weakjunnam = MeasResult.objects.filter(networkId = "품질취약지역", district = "전남").count()
    weakjunbuk = MeasResult.objects.filter(networkId = "품질취약지역", district = "전북").count()
    weakchungnam = MeasResult.objects.filter(networkId = "품질취약지역", district = "충남").count()
    weakchungbuk = MeasResult.objects.filter(networkId = "품질취약지역", district = "충북").count()
    weaksejong = MeasResult.objects.filter(networkId = "품질취약지역", district = "세종").count()
    weaksudo = MeasResult.objects.filter(networkId = "품질취약지역", district = "수도권").count()

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
    }

    return context
   
    # return render(request, "analysis/daily_report_form.html", context)

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
  




