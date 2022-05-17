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
networkid_list = ["5G NSA", "5G SA", "5G 공동망", "LTE", "WiFi", "품질취약지역"]
district_list = ['서울','인천','부산','울산','대구','광주','대전','경기','강원','경남','경북','전남','전북','충남','충북','세종','전국']
center_list = ['서울강북','강원','경기북부','서울강남','경기남부','경기서부','부산','경남','대구','경북','전남','전북','충남','충북']
city_list = ["대도시",'중소도시','농어촌']
facility5g_list = ['대형점포','대학교','아파트','병원','영화관','공항','거리','시장','지하상가','놀이공원','도서관','전시시설','터미널']
traffic5g_list = ['지하철노선','고속도로','지하철역사','KTX.SRT역사','KTX.SRT노선']
inbuildinglte_list = ['대형점포','KTX.SRT역사','대형병원','터미널','지하철역사','공항','전시시설','지하상가']
themelte_list = ['지하철','전통시장','대학교','놀이공원','주요거리','고속도로','KTX.SRT노선']
center_list1 = ['서울강북','강원','경기북부','서울강남','경기남부','경기서부','부산']
center_list2 = ['경남','대구','경북','전남','전북','충남','충북']
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
    
    sregi5G1 = LastMeasDayClose.objects.filter(nettype = "5G NSA", mopho = "행정동").count()
    sregi5G2 = LastMeasDayClose.objects.filter(Q(nettype = "5G NSA")&(Q(mopho = "다중이용시설")|Q(mopho = "교통인프라"))).count()
    sregi5G3 = LastMeasDayClose.objects.filter(nettype = "5G NSA").count()
    sregi5G4 = LastMeasDayClose.objects.filter(nettype = "5G SA ").count()
    sregi5G5 = LastMeasDayClose.objects.filter(nettype = "5G 공동망").count()
    sregi5G6 = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망")) & Q(mopho = "커버리지") & Q(detailadd = "다중이용시설/교통인프라")).count()
    sregi5G7 = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망")) & Q(mopho = "커버리지") & Q(detailadd = "중소시설")).count()
    sregi5G8 = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))).count()
    
    tregi5G1 = LastMeasDayClose.objects.filter(nettype = "5G NSA", mopho = "행정동", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G2 = LastMeasDayClose.objects.filter(Q(nettype = "5G NSA")&(Q(mopho = "다중이용시설")|Q(mopho = "교통인프라"))&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    tregi5G3 = LastMeasDayClose.objects.filter(nettype = "5G NSA", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G4 = LastMeasDayClose.objects.filter(nettype = "5G SA ", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G5 = LastMeasDayClose.objects.filter(nettype = "5G 공동망", measdate = datetime.date.today().strftime('%Y%m%d')).count()
    tregi5G6 = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망")) & Q(mopho = "커버리지") & Q(detailadd = "다중이용시설/교통인프라")&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    tregi5G7 = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망")) & Q(mopho = "커버리지") & Q(detailadd = "중소시설")&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    tregi5G8 = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(measdate = datetime.date.today().strftime('%Y%m%d'))).count()
    
    #5G 개수
    district5gcount = []
    for i in district_list:
        district5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(district = i)).count())
    city5gcount = []
    for i in city_list:
        city5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(detailadd = i)).count())
    facility5gcount = []
    for i in facility5g_list:
        facility5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(detailadd = i)).count())
    traffic5gcount = []
    for i in traffic5g_list:
        traffic5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(detailadd = i)).count())
    districtsa5gcount = []
    for i in district_list:
        districtsa5gcount.append(LastMeasDayClose.objects.filter(nettype = "5G SA", district = i).count())
    
    #LTE 개수
    
    sregiLTE1 = LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "대도시").count()
    sregiLTE2 = LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "중소도시").count()
    sregiLTE3 = LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "농어촌").count()
    sregiLTE4 = LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "인빌딩").count()
    sregiLTE5 = LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "테마").count()
    sregiLTE6 = LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "커버리지").count()
    sregiLTE = LastMeasDayClose.objects.filter(nettype = "LTE").count()
    
    tregiLTE1 = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), detailadd = "대도시").count()
    tregiLTE2 = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), detailadd = "중소도시").count()
    tregiLTE3 = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), detailadd = "농어촌").count()
    tregiLTE4 = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), mopho = "인빌딩").count()
    tregiLTE5 = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), mopho = "테마").count()
    tregiLTE6 = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d'), mopho = "커버리지").count()
    tregiLTE = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = datetime.date.today().strftime('%Y%m%d')).count()

    bctltecount = []
    for i in district_list:
        bctltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "대도시" ,district = i).count())
    mctltecount = []
    for i in district_list:
        mctltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "중소도시" ,district = i).count())
    sctltecount = []
    for i in district_list:
        sctltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "농어촌" ,district = i).count())
    ibltecount = []
    for i in inbuildinglte_list:
        ibltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "인빌딩" ,detailadd = i).count())
    tmltecount = []
    for i in themelte_list:
        tmltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "테마" ,detailadd = i).count()) 

   
    #WiFi 개수
    sregiWiFi1 = LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용").count()
    sregiWiFi2 = LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방").count()
    sregiWiFi3 = LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "공공").count()
    sregiWiFi = LastMeasDayClose.objects.filter(nettype = "WiFi").count()
    tregiWiFi1 = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d'), mopho = "상용").count()
    tregiWiFi2 = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d'), mopho = "개방").count()
    tregiWiFi3 = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d'), mopho = "공공").count()
    tregiWiFi = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = datetime.date.today().strftime('%Y%m%d')).count()
    
    sywificount = []
    for i in district_list:
        sywificount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용" ,district = i).count())
    gbwificount = []
    for i in district_list:
        gbwificount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방" ,district = i).count())
    publicwificount = []
    for i in district_list:
        publicwificount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "공공" ,district = i).count())
    
    
    

    #품질취약지역
    sregiweak1 = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "등산로").count()
    sregiweak2 = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "여객항로").count()
    sregiweak3 = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "유인도서").count()
    sregiweak4 = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "해안도로").count()
    sregiweak = LastMeasDayClose.objects.filter(mopho = "품질취약지역").count()
    tregiweak1 = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = datetime.date.today(), detailadd = "등산로").count()
    tregiweak2 = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = datetime.date.today(), detailadd = "여객항로").count()
    tregiweak3 = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = datetime.date.today(), detailadd = "유인도서").count()
    tregiweak4 = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = datetime.date.today(), detailadd = "해안도로").count()
    tregiweak = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = datetime.date.today()).count()
    
    dsrweakcount = []
    for i in district_list:
        dsrweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "등산로" ,district = i).count())
    yghrweakcount = []
    for i in district_list:
        yghrweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "여객항로" ,district = i).count())
    yidsweakcount = []
    for i in district_list:
        yidsweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "유인도서" ,district = i).count())
    hadrweakcount = []
    for i in district_list:
        hadrweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "해안도로" ,district = i).count())
    
#작년 측정결과(과년도로 변경 예정)
    last5g = MeasLastyear5G.objects.all()
    lastlte = MeasLastyearLTE.objects.all()
    lastwifi = MeasLastyearWiFi.objects.all()
#5G 측정결과
    result5g_list = [["downloadBandwidth","downloadBandwidth__avg"],["uploadBandwidth","uploadBandwidth__avg"],["lte_percent","lte_percent__avg"],["success_rate","success_rate__avg"],["udpJitter","udpJitter__avg"]] 
    bctnsa5g=[]
    mctnsa5g=[]
    hjdnsa5g=[]
    djnsa5g=[]
    aptnsa5g=[]
    univnsa5g=[]
    trafficnsa5g=[]
    totalnsa5g=[]
    for i in result5g_list :
        try:
            bctnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "대도시").aggregate(Avg(i[0]))[i[1]],1))
        except:
            bctnsa5g.append("")
        try:
            mctnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "중소도시").aggregate(Avg(i[0]))[i[1]],1))
        except:
            mctnsa5g.append("")
        try:
            hjdnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",mopho = "행정동").aggregate(Avg(i[0]))[i[1]],1))
        except:
            hjdnsa5g.append("")
        try:
            djnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "다중이용시설").aggregate(Avg(i[0]))[i[1]],1))
        except:
            djnsa5g.append("")
        try:
            aptnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "아파트").aggregate(Avg(i[0]))[i[1]],1))
        except:
            aptnsa5g.append("")
        try:
            univnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "대학교").aggregate(Avg(i[0]))[i[1]],1))
        except:
            univnsa5g.append("")
        try:
            trafficnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",mopho = "교통인프라").aggregate(Avg(i[0]))[i[1]],1))
        except:
            trafficnsa5g.append("")
        try:
            totalnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA").aggregate(Avg(i[0]))[i[1]],1))
        except:
            totalnsa5g.append("")
    
    for i in result5g_list :
        try:
            sa5g = round(LastMeasDayClose.objects.filter(nettype = "5G SA").aggregate(Avg(i[0]))[i[1]],1)
        except:
            sa5g = ""
    

#LTE 측정결과
    resultlte_list = [["downloadBandwidth","downloadBandwidth__avg"],["uploadBandwidth","uploadBandwidth__avg"],["success_rate","success_rate__avg"],["udpJitter","udpJitter__avg"]] 
    bctlte=[]
    mctlte=[]
    sctlte=[]
    hjdlte=[]
    iblte=[]
    tmlte=[]
    totallte=[]
    
    
    for i in resultlte_list :
        
            
        try:
            bctlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd="대도시").aggregate(Avg(i[0]))[i[1]],1))
        except:
            bctlte.append("")
        try:
            mctlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd="중소도시").aggregate(Avg(i[0]))[i[1]],1))
        except:
            mctlte.append("")
        try:
            sctlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd="농어촌").aggregate(Avg(i[0]))[i[1]],1))
        except:
            sctlte.append("")
        try:
            hjdlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", mopho="행정동").aggregate(Avg(i[0]))[i[1]],1))
        except:
            hjdlte.append("")
        try:
            iblte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", mopho="인빌딩").aggregate(Avg(i[0]))[i[1]],1))
        except:
            iblte.append("")
        try:
            tmlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", mopho="테마").aggregate(Avg(i[0]))[i[1]],1))
        except:
            tmlte.append("")
        try:
            totallte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE").aggregate(Avg(i[0]))[i[1]],1))
        except:
            totallte.append("")
        
        
            
#품질취약지역 측정결과
       
#wifi 측정결과(종합)
    try:
        totalwifidl = round(LastMeasDayClose.objects.filter(nettype = "WiFi").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalwifidl = ""
    try:
        totalsywifidl = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalsywifidl = ""
    try:
        totalgbwifidl = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방").aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalgbwifidl = ""
    try:
        totalwifiul = round(LastMeasDayClose.objects.filter(nettype = "WiFi").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalwifiul = ""
    try:
        totalsywifiul = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalsywifiul = ""
    try:
        totalgbwifiul = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방").aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalgbwifiul = ""
#wifi 측정결과(센터별)
    wificenterdl=[]
    
    wificenterul=[]
    
    wificenterdl2=[]
   
    wificenterul2=[]
    
    for i in center_list1:
        try:
            wificenterdl.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용", subadd='').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl.append("")
        try:
            wificenterdl.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방", subadd='').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl.append("")
        try:    
            wificenterul.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용", subadd='').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul.append("")
        try:    
            wificenterul.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방", subadd='').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul.append("")
    for i in center_list2:
        try:
            wificenterdl2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용", subadd='').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl2.append("")
        try:
            wificenterdl2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방", subadd='').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl2.append("")
        try:    
            wificenterul2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용", subadd='').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul2.append("")
        try:    
            wificenterul2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방", subadd='').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul2.append("")
#wifi 측정결과(지역별)
    train_list = [(Q('서울')|Q('인천')|Q('경기')|Q('부산')|Q('대구')|Q('광주')|Q('대전')),(Q('서울')|Q('인천')|Q('경기')),'부산','대구','광주','대전']
    wifitraindl=[]
    wifitrainul=[]
    for i in train_list:
        try:
            wifitraindl.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", district=i,subadd='지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wifitraindl.append("")
        try:
            wifitrainul.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", district=i, subadd='지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:
            wifitrainul.append("")
#금일 측정 결과 
    tresult5g = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(measdate = datetime.date.today().strftime('%Y%m%d')))
    tresultlte = LastMeasDayClose.objects.filter(nettype = "LTE", measdate = datetime.date.today())
    tresultwifi = LastMeasDayClose.objects.filter(nettype = "WiFi", measdate = datetime.date.today())
    tresultweak = LastMeasDayClose.objects.filter(nettype = "품질취약지역", measdate = datetime.date.today())
   
    context = { 
    'wificenterdl':wificenterdl,'wificenterul':wificenterul,'center_list1':center_list1,'center_list2':center_list2,
    'wificenterdl2':wificenterdl2,'wificenterul2':wificenterul2,
    'district5gcount':district5gcount,'city5gcount':city5gcount,'facility5gcount':facility5gcount,'traffic5gcount':traffic5gcount,'districtsa5gcount':districtsa5gcount,
    'bctltecount':bctltecount,'mctltecount':mctltecount,'sctltecount':sctltecount,'ibltecount':ibltecount,'tmltecount':tmltecount,
    'sywificount':sywificount,'gbwificount':gbwificount,'publicwificount':publicwificount,
    'dsrweakcount':dsrweakcount,'yghrweakcount':yghrweakcount,'yidsweakcount':yidsweakcount,'hadrweakcount':hadrweakcount,
    'tresult5g':tresult5g,'tresultlte':tresultlte,'tresultwifi':tresultwifi,'tresultweak':tresultweak,
    'regi':regi, 'reportmsg':reportmsg,'sregi':sregi,'firstdate':firstdate,'lastdate':lastdate,
    'tregi5G1':tregi5G1,'tregi5G2':tregi5G2,'tregi5G3':tregi5G3,'tregi5G4':tregi5G4, 'tregi5G5':tregi5G5,'tregi5G6':tregi5G6,'tregi5G7':tregi5G7,'tregi5G8':tregi5G8,
    'sregi5G1':sregi5G1,'sregi5G2':sregi5G2,'sregi5G3':sregi5G3,'sregi5G4':sregi5G4,'sregi5G5':sregi5G5,'sregi5G6':sregi5G6,'sregi5G7':sregi5G7,'sregi5G8':sregi5G8,
    'sregiLTE1':sregiLTE1, 'sregiLTE2':sregiLTE2,'sregiLTE3':sregiLTE3, 'sregiLTE4':sregiLTE4,'sregiLTE5':sregiLTE5, 'sregiLTE6':sregiLTE6,'sregiLTE':sregiLTE, 
    'tregiLTE1':tregiLTE1,'tregiLTE2':tregiLTE2, 'tregiLTE3':tregiLTE3,'tregiLTE4':tregiLTE4, 'tregiLTE5':tregiLTE5,'tregiLTE6':tregiLTE6, 'tregiLTE':tregiLTE,
    'sregiWiFi1':sregiWiFi1,'sregiWiFi2':sregiWiFi2,'sregiWiFi':sregiWiFi,'tregiWiFi1':tregiWiFi1,'tregiWiFi2':tregiWiFi2,'tregiWiFi':tregiWiFi,'sregiweak1':sregiweak1,
    'sregiweak2':sregiweak2,'sregiweak3':sregiweak3,'sregiweak4':sregiweak4,'sregiweak':sregiweak,'tregiweak1':tregiweak1,'tregiweak2':tregiweak2,'tregiweak3':tregiweak3,'tregiweak4':tregiweak4,
    'tregiweak':tregiweak,
    'bctnsa5g':bctnsa5g,
    'mctnsa5g':mctnsa5g,
    'hjdnsa5g':hjdnsa5g,
    'djnsa5g':djnsa5g,
    'aptnsa5g':aptnsa5g,
    'univnsa5g':univnsa5g,
    'trafficnsa5g':trafficnsa5g,
    'totalnsa5g':totalnsa5g,'sa5g':sa5g,
    'bctlte':bctlte,
    'mctlte':mctlte,
    'sctlte':sctlte,
    'hjdlte':hjdlte,
    'iblte':iblte,
    'tmlte':tmlte,
    'totallte':totallte,
    'last5g':last5g, 'lastlte':lastlte,'lastwifi':lastwifi,
    'wifitraindl':wifitraindl,
    'wifitrainul':wifitrainul,
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
    
    

    context = {'measclose':measclose,'networkid_list':networkid_list,
               'district_list':district_list,'center_list':center_list,'city_list':city_list ,'facility5g_list':facility5g_list,'traffic5g_list':traffic5g_list,
    'inbuildinglte_list':inbuildinglte_list,'themelte_list':themelte_list,
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
  

