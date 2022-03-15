from django.shortcuts import render,redirect
from monitor.models import Phone
from .models import MeasPlan, MeasResult, Register, TodayRegister
import pandas as pd
import datetime
from django.db.models import Sum
################################################################################################################################################
# 일일보고 이전버전
################################################################################################################################################
def make_report(request):
    regi5G = Register.objects.filter(category = "5G")
    regiLTE = Register.objects.filter(category = "LTE")
    regiWiFi = Register.objects.filter(category = "WiFi")
    regiweak = Register.objects.filter(category = "품질취약지역")
    firstdate = TodayRegister.objects.last()
    lastdate = TodayRegister.objects.first()
    
    sregi = TodayRegister.objects.all()
    sregi5G1 = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동").count()
    sregi5G2 = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라").count()
    sregi5G3 = TodayRegister.objects.filter(category = "5G", dongdaco = "커버리지").count()
    sregi5G = TodayRegister.objects.filter(category = "5G").count()
    tregi5G1 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "행정동").count()
    tregi5G2 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "다중이용시설/교통인프라").count()
    tregi5G3 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "커버리지").count()
    tregi5G = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today()).count()

    sregiLTE1 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시").count()
    sregLTE2 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시").count()
    sregiLTE3 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌").count()
    sregiLTE4 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩").count()
    sregiLTE5 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마").count()
    sregiLTE6 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "커버리지").count()
    sregiLTE = TodayRegister.objects.filter(category = "LTE").count()
    tregiLTE1 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "대도시").count()
    tregiLTE2 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "중소도시").count()
    tregiLTE3 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "농어촌").count()
    tregiLTE4 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "인빌딩").count()
    tregiLTE5 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "테마").count()
    tregiLTE6 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "커버리지").count()
    tregiLTE = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today()).count()

    sregiWiFi1 = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용").count()
    sregiWiFi2 = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방").count()
    sregiWiFi = TodayRegister.objects.filter(category = "WiFi").count()
    tregiWiFi1 = TodayRegister.objects.filter(category = "WiFi",  date = datetime.date.today(), sanggae = "상용").count()
    tregiWiFi2 = TodayRegister.objects.filter(category = "WiFi",  date = datetime.date.today(), sanggae = "개방").count()
    tregiWiFi = TodayRegister.objects.filter(category = "WiFi").count()
    
    sregiweak1 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "등산로").count()
    sregiweak2 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "여객항로").count()
    sregiweak3 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "유인도서").count()
    sregiweak4 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "해안도로").count()
    sregiweak = TodayRegister.objects.filter(category = "품질취약지역").count()
    tregiweak1 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "등산로").count()
    tregiweak2 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "여객항로").count()
    tregiweak3 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "유인도서").count()
    tregiweak4 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "해안도로").count()
    tregiweak = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today()).count()
    
    hjd5gseoul = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "서울").count()
    hjd5gincheon = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "인천").count()
    hjd5gulsan = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "울산").count()
    hjd5gdaegu = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "대구").count()
    hjd5ggwangju = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "광주").count()
    hjd5gdaejun = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "대전").count()
    hjd5ggyunggi = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "경기").count()
    hjd5ggyungbuk = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "경북").count()
    hjd5gjunnam = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "전남").count()
    hjd5gjunbuk = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "전북").count()
    hjd5gchungnam = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "충남").count()
    hjd5gchungbuk = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "충북").count()
    hjd5gsejong = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동", jiyok = "세종").count()

    dagyo5gseoul = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "서울").count()
    dagyo5gincheon = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "인천").count()
    dagyo5gulsan = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "울산").count()
    dagyo5gdaegu = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "대구").count()
    dagyo5ggwangju = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "광주").count()
    dagyo5gdaejun = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "대전").count()
    dagyo5ggyunggi = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "경기").count()
    dagyo5ggyungbuk = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "경북").count()
    dagyo5gjunnam = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "전남").count()
    dagyo5gjunbuk = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "전북").count()
    dagyo5gchungnam = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "충남").count()
    dagyo5gchungbuk = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "충북").count()
    dagyo5gsejong = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "세종").count()
    dagyo5gsudo = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라", jiyok = "수도권").count()

    bigcityLTEseoul = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "서울").count()
    bigcityLTEincheon = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "인천").count()
    bigcityLTEulsan = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "울산").count()
    bigcityLTEdaegu = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "대구").count()
    bigcityLTEgwangju = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "광주").count()
    bigcityLTEdaejun = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "대전").count()
    bigcityLTEgyunggi = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "경기").count()
    bigcityLTEgyungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "경북").count()
    bigcityLTEjunnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "전남").count()
    bigcityLTEjunbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "전북").count()
    bigcityLTEchungnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "충남").count()
    bigcityLTEchungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "충북").count()
    bigcityLTEsejong = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "세종").count()
    bigcityLTEsudo = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시", jiyok = "수도권").count()

    smallcityLTEseoul = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "서울").count()
    smallcityLTEincheon = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "인천").count()
    smallcityLTEulsan = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "울산").count()
    smallcityLTEdaegu = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "대구").count()
    smallcityLTEgwangju = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "광주").count()
    smallcityLTEdaejun = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "대전").count()
    smallcityLTEgyunggi = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "경기").count()
    smallcityLTEgyungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "경북").count()
    smallcityLTEjunnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "전남").count()
    smallcityLTEjunbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "전북").count()
    smallcityLTEchungnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "충남").count()
    smallcityLTEchungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "충북").count()
    smallcityLTEsejong = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "세종").count()
    smallcityLTEsudo = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시", jiyok = "수도권").count()

    
    nongLTEseoul = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "서울").count()
    nongLTEincheon = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "인천").count()
    nongLTEulsan = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "울산").count()
    nongLTEdaegu = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "대구").count()
    nongLTEgwangju = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "광주").count()
    nongLTEdaejun = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "대전").count()
    nongLTEgyunggi = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "경기").count()
    nongLTEgyungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "경북").count()
    nongLTEjunnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "전남").count()
    nongLTEjunbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "전북").count()
    nongLTEchungnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "충남").count()
    nongLTEchungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "충북").count()
    nongLTEsejong = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "세종").count()
    nongLTEsudo = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌", jiyok = "수도권").count()


    inbuildingLTEcdys = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "철도역사").count()
    inbuildingLTEdhbw = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "대형병원").count()
    inbuildingLTEbhj = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "백화점").count()
    inbuildingLTEtmn = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "터미널").count()
    inbuildingLTEgh = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "공항").count()
    inbuildingLTEdhjp = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "대형점포").count()
    inbuildingLTEjsj = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "전시장").count()
    inbuildingLTEjhcys = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩", jiyok = "지하철역사").count()


    themeLTEjunnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마", jiyok = "대학교").count()
    themeLTEjunbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마", jiyok = "놀이공원").count()
    themeLTEchungnam = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마", jiyok = "주요거리").count()
    themeLTEchungbuk = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마", jiyok = "전통시장").count()
    themeLTEsejong = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마", jiyok = "지하철노선").count()
    

    sangWiFiseoul = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "서울").count()
    sangWiFiincheon = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "인천").count()
    sangWiFiulsan = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "울산").count()
    sangWiFidaegu = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "대구").count()
    sangWiFigwangju = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "광주").count()
    sangWiFidaejun = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "대전").count()
    sangWiFigyunggi = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "경기").count()
    sangWiFigyungbuk = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "경북").count()
    sangWiFijunnam = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "전남").count()
    sangWiFijunbuk = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "전북").count()
    sangWiFichungnam = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "충남").count()
    sangWiFichungbuk = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "충북").count()
    sangWiFisejong = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "세종").count()
    sangWiFisudo = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용", jiyok = "수도권").count()

    gaeWiFiseoul = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "서울").count()
    gaeWiFiincheon = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "인천").count()
    gaeWiFiulsan = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "울산").count()
    gaeWiFidaegu = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "대구").count()
    gaeWiFigwangju = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "광주").count()
    gaeWiFidaejun = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "대전").count()
    gaeWiFigyunggi = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "경기").count()
    gaeWiFigyungbuk = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "경북").count()
    gaeWiFijunnam = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "전남").count()
    gaeWiFijunbuk = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "전북").count()
    gaeWiFichungnam = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "충남").count()
    gaeWiFichungbuk = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "충북").count()
    gaeWiFisejong = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "세종").count()
    gaeWiFisudo = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방", jiyok = "수도권").count()


    weakseoul = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "서울").count()
    weakincheon = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "인천").count()
    weakulsan = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "울산").count()
    weakdaegu = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "대구").count()
    weakgwangju = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "광주").count()
    weakdaejun = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "대전").count()
    weakgyunggi = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "경기").count()
    weakgyungbuk = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "경북").count()
    weakjunnam = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "전남").count()
    weakjunbuk = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "전북").count()
    weakchungnam = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "충남").count()
    weakchungbuk = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "충북").count()
    weaksejong = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "세종").count()
    weaksudo = TodayRegister.objects.filter(category = "품질취약지역", jiyok = "수도권").count()

    context = {'regi5G':regi5G,'regiLTE':regiLTE,'regiWiFi':regiWiFi,'regiweak':regiweak
    ,'sregi':sregi,'firstdate':firstdate,'lastdate':lastdate,
    'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G':tregi5G,'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G':sregi5G,
     'sregiLTE1':sregiLTE1, 'sregiLTE2':sregLTE2,'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,'sregiLTE':sregiLTE, 'tregiLTE1':tregiLTE1,
    'tregiLTE2':tregiLTE2, 'tregiLTE3':tregiLTE3,'tregiLTE4':tregiLTE4, 'tregiLTE5':tregiLTE5,'tregiLTE6':tregiLTE6, 'tregiLTE':tregiLTE,'sregiWiFi1':sregiWiFi1,
    'sregiWiFi2':sregiWiFi2,'sregiWiFi':sregiWiFi,'tregiWiFi1':tregiWiFi1,'tregiWiFi2':tregiWiFi2,'tregiWiFi':tregiWiFi,'sregiweak1':sregiweak1,'sregiweak2':sregiweak2,
    'sregiweak3':sregiweak3,'sregiweak4':sregiweak4,'sregiweak':sregiweak,'tregiweak1':tregiweak1,'tregiweak2':tregiweak2,'tregiweak3':tregiweak3,'tregiweak4':tregiweak4,
    'tregiweak':tregiweak,'hjd5gseoul':hjd5gseoul, 'hjd5gincheon':hjd5gincheon, 'hjd5gulsan':hjd5gulsan,
    "hjd5gseoul":hjd5gseoul,"hjd5gincheon":hjd5gincheon,"hjd5gulsan":hjd5gulsan,"hjd5gdaegu":hjd5gdaegu,"hjd5ggwangju":hjd5ggwangju,"hjd5gdaejun":hjd5gdaejun,"hjd5ggyunggi":hjd5ggyunggi,"hjd5ggyungbuk":hjd5ggyungbuk,"hjd5gjunnam":hjd5gjunnam,"hjd5gjunbuk":hjd5gjunbuk,"hjd5gchungnam":hjd5gchungnam,"hjd5gchungbuk":hjd5gchungbuk,"hjd5gsejong":hjd5gsejong,
    "dagyo5gseoul":dagyo5gseoul,"dagyo5gincheon":dagyo5gincheon,"dagyo5gulsan":dagyo5gulsan,"dagyo5gdaegu":dagyo5gdaegu,"dagyo5ggwangju":dagyo5ggwangju,"dagyo5gdaejun":dagyo5gdaejun,"dagyo5ggyunggi":dagyo5ggyunggi,"dagyo5ggyungbuk":dagyo5ggyungbuk,"dagyo5gjunnam":dagyo5gjunnam,"dagyo5gjunbuk":dagyo5gjunbuk,"dagyo5gchungnam":dagyo5gchungnam,"dagyo5gchungbuk":dagyo5gchungbuk,"dagyo5gsejong":dagyo5gsejong,"dagyo5gsudo":dagyo5gsudo,
    'bigcityLTEseoul':bigcityLTEseoul,'bigcityLTEincheon':bigcityLTEincheon,'bigcityLTEulsan':bigcityLTEulsan,'bigcityLTEdaegu':bigcityLTEdaegu,'bigcityLTEgwangju':bigcityLTEgwangju,'bigcityLTEdaejun':bigcityLTEdaejun,'bigcityLTEgyunggi':bigcityLTEgyunggi,'bigcityLTEgyungbuk':bigcityLTEgyungbuk,'bigcityLTEjunnam':bigcityLTEjunnam,'bigcityLTEjunbuk':bigcityLTEjunbuk,'bigcityLTEchungnam':bigcityLTEchungnam,'bigcityLTEchungbuk':bigcityLTEchungbuk,'bigcityLTEsejong':bigcityLTEsejong,'bigcityLTEsudo':bigcityLTEsudo,'smallcityLTEseoul':smallcityLTEseoul,'smallcityLTEincheon':smallcityLTEincheon,'smallcityLTEulsan':smallcityLTEulsan,'smallcityLTEdaegu':smallcityLTEdaegu,'smallcityLTEgwangju':smallcityLTEgwangju,'smallcityLTEdaejun':smallcityLTEdaejun,'smallcityLTEgyunggi':smallcityLTEgyunggi,'smallcityLTEgyungbuk':smallcityLTEgyungbuk,'smallcityLTEjunnam':smallcityLTEjunnam,'smallcityLTEjunbuk':smallcityLTEjunbuk,'smallcityLTEchungnam':smallcityLTEchungnam,'smallcityLTEchungbuk':smallcityLTEchungbuk,'smallcityLTEsejong':smallcityLTEsejong,'smallcityLTEsudo':smallcityLTEsudo,'nongLTEseoul':nongLTEseoul,'nongLTEincheon':nongLTEincheon,'nongLTEulsan':nongLTEulsan,'nongLTEdaegu':nongLTEdaegu,'nongLTEgwangju':nongLTEgwangju,'nongLTEdaejun':nongLTEdaejun,'nongLTEgyunggi':nongLTEgyunggi,'nongLTEgyungbuk':nongLTEgyungbuk,'nongLTEjunnam':nongLTEjunnam,'nongLTEjunbuk':nongLTEjunbuk,'nongLTEchungnam':nongLTEchungnam,'nongLTEchungbuk':nongLTEchungbuk,'nongLTEsejong':nongLTEsejong,'nongLTEsudo':nongLTEsudo,'inbuildingLTEcdys':inbuildingLTEcdys,'inbuildingLTEdhbw':inbuildingLTEdhbw,'inbuildingLTEbhj':inbuildingLTEbhj,'inbuildingLTEtmn':inbuildingLTEtmn,'inbuildingLTEgh':inbuildingLTEgh,'inbuildingLTEdhjp':inbuildingLTEdhjp,'inbuildingLTEjsj':inbuildingLTEjsj,'inbuildingLTEjhcys':inbuildingLTEjhcys,'themeLTEjunnam':themeLTEjunnam,'themeLTEjunbuk':themeLTEjunbuk,'themeLTEchungnam':themeLTEchungnam,'themeLTEchungbuk':themeLTEchungbuk,'themeLTEsejong':themeLTEsejong,'sangWiFiseoul':sangWiFiseoul,'sangWiFiincheon':sangWiFiincheon,'sangWiFiulsan':sangWiFiulsan,'sangWiFidaegu':sangWiFidaegu,'sangWiFigwangju':sangWiFigwangju,'sangWiFidaejun':sangWiFidaejun,'sangWiFigyunggi':sangWiFigyunggi,'sangWiFigyungbuk':sangWiFigyungbuk,'sangWiFijunnam':sangWiFijunnam,'sangWiFijunbuk':sangWiFijunbuk,'sangWiFichungnam':sangWiFichungnam,'sangWiFichungbuk':sangWiFichungbuk,'sangWiFisejong':sangWiFisejong,'sangWiFisudo':sangWiFisudo,'gaeWiFiseoul':gaeWiFiseoul,'gaeWiFiincheon':gaeWiFiincheon,'gaeWiFiulsan':gaeWiFiulsan,'gaeWiFidaegu':gaeWiFidaegu,'gaeWiFigwangju':gaeWiFigwangju,'gaeWiFidaejun':gaeWiFidaejun,'gaeWiFigyunggi':gaeWiFigyunggi,'gaeWiFigyungbuk':gaeWiFigyungbuk,'gaeWiFijunnam':gaeWiFijunnam,'gaeWiFijunbuk':gaeWiFijunbuk,'gaeWiFichungnam':gaeWiFichungnam,'gaeWiFichungbuk':gaeWiFichungbuk,'gaeWiFisejong':gaeWiFisejong,'gaeWiFisudo':gaeWiFisudo,'weakseoul':weakseoul,'weakincheon':weakincheon,'weakulsan':weakulsan,'weakdaegu':weakdaegu,'weakgwangju':weakgwangju,'weakdaejun':weakdaejun,'weakgyunggi':weakgyunggi,'weakgyungbuk':weakgyungbuk,'weakjunnam':weakjunnam,'weakjunbuk':weakjunbuk,'weakchungnam':weakchungnam,'weakchungbuk':weakchungbuk,'weaksejong':weaksejong,'weaksudo':weaksudo,

    }
   
    return render(request, "analysis/daily_report.html", context)
###############################################################################################################################################################################
#일일보고 수정버전 (admin.py를 이용)
###############################################################################################################################################################################
# def make_report(request):
#     measplan = MeasPlan.objects.all()
#     measplan_5G = MeasPlan.objects.filter(networkId="5G").order_by('area','molph_level0')
#     measplan_5G_total = MeasPlan.objects.filter(networkId="5G").aggregate(Sum('meas_count'))['meas_count__sum']
#     measplan_LTE = MeasPlan.objects.filter(networkId="LTE").order_by('area','molph_level0')
#     measplan_LTE_total = MeasPlan.objects.filter(networkId="LTE").aggregate(Sum('meas_count'))['meas_count__sum']
#     measplan_WiFi = MeasPlan.objects.filter(networkId="WiFi").order_by('area','molph_level0')
#     measplan_WiFi_total = MeasPlan.objects.filter(networkId="WiFi").aggregate(Sum('meas_count'))['meas_count__sum']
#     measplan_weakarea = MeasPlan.objects.filter(networkId="품질취약지역").order_by('area','molph_level0')
#     measplan_weakarea_total = MeasPlan.objects.filter(networkId="품질취약지역").aggregate(Sum('meas_count'))['meas_count__sum']
#     measplan_context = {'measplan':measplan, 'measplan_5G':measplan_5G, 'measplan_5G_total':measplan_5G_total, 'measplan_LTE':measplan_LTE, 'measplan_LTE_total':measplan_LTE_total, 'measplan_WiFi':measplan_WiFi, 'measplan_WiFi_total':measplan_WiFi_total, 'measplan_weakarea':measplan_weakarea, 'measplan_weakarea_total':measplan_weakarea_total}
    
#     measresult = MeasResult.objects.all().count()
#     measresult_5G = MeasResult.objects
   
#     measresult_context = {'measresult':measresult,'measresult_5G':measresult_5G}
#     context = dict(measplan_context, **measresult_context)

#     return render(request, "analysis/daily_report.html", context)

###############################################################################################################################################################################
#키 값 만들기
###############################################################################################################################################################################













###############################################################################################################################################################################
#웹페이지(대상등록)
###############################################################################################################################################################################
# def new(request):
#     regi5G = Register.objects.filter(category = "5G")
#     regiLTE = Register.objects.filter(category = "LTE")
#     regiWiFi = Register.objects.filter(category = "WiFi")
#     regiweak = Register.objects.filter(category = "품질취약지역")
#     sregi = TodayRegister.objects.all()
#     tregi = TodayRegister.objects.filter(date = datetime.date.today())
#     sregi5G1 = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동").count()
#     sregi5G2 = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라").count()
#     sregi5G3 = TodayRegister.objects.filter(category = "5G", dongdaco = "커버리지").count()
#     sregi5G = TodayRegister.objects.filter(category = "5G").count()
#     tregi5G1 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "행정동").count()
#     tregi5G2 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "다중이용시설/교통인프라").count()
#     tregi5G3 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "커버리지").count()
#     tregi5G = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today()).count()

#     sregiLTE1 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시").count()
#     sregLTE2 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시").count()
#     sregiLTE3 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌").count()
#     sregiLTE4 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩").count()
#     sregiLTE5 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마").count()
#     sregiLTE6 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "커버리지").count()
#     sregiLTE = TodayRegister.objects.filter(category = "LTE").count()
#     tregiLTE1 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "대도시").count()
#     tregiLTE2 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "중소도시").count()
#     tregiLTE3 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "농어촌").count()
#     tregiLTE4 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "인빌딩").count()
#     tregiLTE5 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "테마").count()
#     tregiLTE6 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "커버리지").count()
#     tregiLTE = TodayRegister.objects.filter(category = "LTE").count()

#     sregiWiFi1 = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용").count()
#     sregiWiFi2 = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방").count()
#     sregiWiFi = TodayRegister.objects.filter(category = "WiFi").count()
#     tregiWiFi1 = TodayRegister.objects.filter(category = "WiFi",  date = datetime.date.today(), sanggae = "상용").count()
#     tregiWiFi2 = TodayRegister.objects.filter(category = "WiFi",  date = datetime.date.today(), sanggae = "개방").count()
#     tregiWiFi = TodayRegister.objects.filter(category = "WiFi").count()
    
#     sregiweak1 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "등산로").count()
#     sregiweak2 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "여객항로").count()
#     sregiweak3 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "유인도서").count()
#     sregiweak4 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "해안도로").count()
#     sregiweak = TodayRegister.objects.filter(category = "품질취약지역").count()
#     tregiweak1 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "등산로").count()
#     tregiweak2 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "여객항로").count()
#     tregiweak3 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "유인도서").count()
#     tregiweak4 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "해안도로").count()
#     tregiweak = TodayRegister.objects.filter(category = "품질취약지역").count()

#     context = {'regi5G':regi5G,'regiLTE':regiLTE,'regiWiFi':regiWiFi,'regiweak':regiweak, 'sregi':sregi,
#     'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G':tregi5G,'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G':sregi5G,
#     'sregiLTE1':sregiLTE1, 'sregiLTE2':sregLTE2,
#     'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,
#     'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,
#     'sregiLTE':sregiLTE, 'tregiLTE1':tregiLTE1,
#     'tregiLTE2':tregiLTE2, 'tregiLTE3':tregiLTE3,
#     'tregiLTE4':tregiLTE4, 'tregiLTE5':tregiLTE5,
#     'tregiLTE6':tregiLTE6, 'tregiLTE':tregiLTE,
#     'sregiWiFi1':sregiWiFi1,
#     'sregiWiFi2':sregiWiFi2,
#     'sregiWiFi':sregiWiFi,
#     'tregiWiFi1':tregiWiFi1,
#     'tregiWiFi2':tregiWiFi2,
#     'tregiWiFi':tregiWiFi,
#     'sregiweak1':sregiweak1,
#     'sregiweak2':sregiweak2,
#     'sregiweak3':sregiweak3,
#     'sregiweak4':sregiweak4,
#     'sregiweak':sregiweak,
#     'tregiweak1':tregiweak1,
#     'tregiweak2':tregiweak2,
#     'tregiweak3':tregiweak3,
#     'tregiweak4':tregiweak4,
#     'tregiweak':tregiweak,
#     }

#     return render(request, "analysis/new.html", context)

def new(request):
    measplan = Register.objects.filter(planYear = "2022")
  
    sregi = TodayRegister.objects.all()
    tregi = TodayRegister.objects.filter(date = datetime.date.today())
    sregi5G1 = TodayRegister.objects.filter(category = "5G", dongdaco = "행정동").count()
    sregi5G2 = TodayRegister.objects.filter(category = "5G", dongdaco = "다중이용시설/교통인프라").count()
    sregi5G3 = TodayRegister.objects.filter(category = "5G", dongdaco = "커버리지").count()
    sregi5G = TodayRegister.objects.filter(category = "5G").count()
    tregi5G1 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "행정동").count()
    tregi5G2 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "다중이용시설/교통인프라").count()
    tregi5G3 = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today(), dongdaco = "커버리지").count()
    tregi5G = TodayRegister.objects.filter(category = "5G" , date = datetime.date.today()).count()

    sregiLTE1 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "대도시").count()
    sregLTE2 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "중소도시").count()
    sregiLTE3 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "농어촌").count()
    sregiLTE4 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "인빌딩").count()
    sregiLTE5 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "테마").count()
    sregiLTE6 = TodayRegister.objects.filter(category = "LTE", bigsmallnongintheme = "커버리지").count()
    sregiLTE = TodayRegister.objects.filter(category = "LTE").count()
    tregiLTE1 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "대도시").count()
    tregiLTE2 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "중소도시").count()
    tregiLTE3 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "농어촌").count()
    tregiLTE4 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "인빌딩").count()
    tregiLTE5 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "테마").count()
    tregiLTE6 = TodayRegister.objects.filter(category = "LTE",  date = datetime.date.today(), bigsmallnongintheme = "커버리지").count()
    tregiLTE = TodayRegister.objects.filter(category = "LTE").count()

    sregiWiFi1 = TodayRegister.objects.filter(category = "WiFi", sanggae = "상용").count()
    sregiWiFi2 = TodayRegister.objects.filter(category = "WiFi", sanggae = "개방").count()
    sregiWiFi = TodayRegister.objects.filter(category = "WiFi").count()
    tregiWiFi1 = TodayRegister.objects.filter(category = "WiFi",  date = datetime.date.today(), sanggae = "상용").count()
    tregiWiFi2 = TodayRegister.objects.filter(category = "WiFi",  date = datetime.date.today(), sanggae = "개방").count()
    tregiWiFi = TodayRegister.objects.filter(category = "WiFi").count()
    
    sregiweak1 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "등산로").count()
    sregiweak2 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "여객항로").count()
    sregiweak3 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "유인도서").count()
    sregiweak4 = TodayRegister.objects.filter(category = "품질취약지역", weakjiyok = "해안도로").count()
    sregiweak = TodayRegister.objects.filter(category = "품질취약지역").count()
    tregiweak1 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "등산로").count()
    tregiweak2 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "여객항로").count()
    tregiweak3 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "유인도서").count()
    tregiweak4 = TodayRegister.objects.filter(category = "품질취약지역",  date = datetime.date.today(), weakjiyok = "해안도로").count()
    tregiweak = TodayRegister.objects.filter(category = "품질취약지역").count()

    context = {'measplan':measplan, 'sregi':sregi,
    'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G':tregi5G,'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G':sregi5G,
    'sregiLTE1':sregiLTE1, 'sregiLTE2':sregLTE2,
    'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,
    'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,
    'sregiLTE':sregiLTE, 'tregiLTE1':tregiLTE1,
    'tregiLTE2':tregiLTE2, 'tregiLTE3':tregiLTE3,
    'tregiLTE4':tregiLTE4, 'tregiLTE5':tregiLTE5,
    'tregiLTE6':tregiLTE6, 'tregiLTE':tregiLTE,
    'sregiWiFi1':sregiWiFi1,
    'sregiWiFi2':sregiWiFi2,
    'sregiWiFi':sregiWiFi,
    'tregiWiFi1':tregiWiFi1,
    'tregiWiFi2':tregiWiFi2,
    'tregiWiFi':tregiWiFi,
    'sregiweak1':sregiweak1,
    'sregiweak2':sregiweak2,
    'sregiweak3':sregiweak3,
    'sregiweak4':sregiweak4,
    'sregiweak':sregiweak,
    'tregiweak1':tregiweak1,
    'tregiweak2':tregiweak2,
    'tregiweak3':tregiweak3,
    'tregiweak4':tregiweak4,
    'tregiweak':tregiweak,
    }

    return render(request, "analysis/new.html", context)

def make_register(request):
    if(request.method== "POST") :
        register = Register() #빈 객체 생성
        
        register.planYear = request.POST['planYear']
        register.area1 = request.POST['area1']
        register.area2 = request.POST['area2']
        register.area3 = request.POST['area3']
        register.area4 = request.POST['area4']
        register.area5 = request.POST['area5']
        register.area6 = request.POST['area6']
        register.area7 = request.POST['area7']
        register.area8 = request.POST['area8']
        register.area9 = request.POST['area9']
        register.area10 = request.POST['area10']
        register.area11 = request.POST['area11']
        register.area12 = request.POST['area12']
        register.area13 = request.POST['area13']
        register.area14 = request.POST['area14']
        register.area15 = request.POST['area15']
        register.total5G =  int(register.area1)+ int(register.area2)+ int(register.area3)
        register.totalLTE =  int(register.area4)+ int(register.area5)+ int(register.area6)+ int(register.area7)+ int(register.area8)+ int(register.area9)
        register.totalWiFi =  int(register.area10)+ int(register.area11)
        register.totalWeakArea =  int(register.area12)+ int(register.area13)+ int(register.area14)+ int(register.area15)
        register.total =  register.total5G + register.totalLTE + register.totalWiFi + register.totalWeakArea
       
        Register.objects.filter(planYear = register.planYear).delete()
        register.save()

    return redirect("new")

# def make_measplan(request):
#     if(request.method== "POST") :
#         measplan = MeasPlan() #빈 객체 생성
#         measplan.networkId = request.POST['networkId']
        
#         measpaln.year = request.POST['year']
#         measplan.area = request.POST['area']
#         measplan.molph_level0 = request.POST['molph_level0']
#         measplan.meas_count = request.POST['meas_count']
        
     
            
#         measplan.objects.filter(year = measplan.year, networkId = measplan.networkId, area = measplan.area, molph_level0 = measplan.molph_level0).delete()
#         register.save()

#     return redirect("new")

# def make_register(request):
#     if(request.method== "POST") :
#         register = Register() #빈 객체 생성
#         register.category = request.POST['category']
#         if(register.category == "5G"):
#             register.dong = request.POST['dong']
#             register.dagyo = request.POST['dagyo']
#             register.coverage5g = request.POST['coverage5g']
#             register.total = int(register.dong)+int(register.dagyo)+int(register.coverage5g)
#         elif(register.category == "LTE"):
#             register.bigct = request.POST['bigct']
#             register.smallct = request.POST['smallct']
#             register.inbuiling = request.POST['inbuiling']
#             register.nong = request.POST['nong']
#             register.theme = request.POST['theme']
#             register.coveragelte = request.POST['coveragelte']
#             register.total =  int(register.bigct)+ int(register.smallct)+ int(register.nong)+ int(register.inbuiling)+ int(register.theme)+ int(register.coveragelte)
#         elif(register.category == "WiFi"):
#             register.sangyong = request.POST['sangyong']
#             register.gaebang = request.POST['gaebang']
#             register.total =  int(register.sangyong)+ int(register.gaebang)
#         else:
#             register.mountain =request.POST['mountain']
#             register.ship = request.POST['ship']
#             register.yooin = request.POST['yooin']
#             register.searoad = request.POST['searoad']
#             register.total =  int(register.mountain)+ int(register.ship)+ int(register.yooin)+ int(register.searoad)
        
#         # if(register.category == "5G"):
#         #     register.total = int(register.dong)+int(register.dagyo)+int(register.coverage)
#         # elif(register.category == "LTE"):
#         #     register.total =  int(register.bigct)+ int(register.smallct)+ int(register.nong)+ int(register.inbuiling)+ int(register.theme)+ int(register.coverage)
#         # elif(register.category == "WiFi"):
#         #     register.total =  int(register.sangyong)+ int(register.gaebang)
#         # else:
#         #     register.total =  int(register.mountain)+ int(register.ship)+ int(register.yooin)+ int(register.searoad)
        
            
#         Register.objects.filter(category = register.category).delete()
#         register.save()

#     return redirect("new")

def make_todayregister(request):
    if(request.method== "POST") :
        tregister = TodayRegister() #빈 객체 생성
        tregister.name = request.POST['name']
        tregister.category = request.POST['category']
        tregister.jiyok = request.POST['jiyok']
        tregister.date = request.POST['date']
        tregister.dongdaco = request.POST['dongdaco']
        tregister.bigsmallnongintheme = request.POST['bigsmallnongintheme']
        tregister.sanggae = request.POST['sanggae']
        tregister.weakjiyok = request.POST['weakjiyok']

        # TodayRegister.objects.filter(date = tregister.date).delete()

        tregister.save()
        
    return redirect("new")


def delete_register(request):
    if(request.method== "POST") :
       
       Register.objects.all().delete()

    return redirect("new")
def delete_todayregister(request):
    if(request.method== "POST") :
       
       TodayRegister.objects.all().delete()
       
       

    return redirect("new")
def test_layout(request):

    return render(request, "analysis/test_layout.html")