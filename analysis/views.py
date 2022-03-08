from django.shortcuts import render,redirect
from monitor.models import Phone
from .models import Register, TodayRegister
import pandas as pd
import datetime

# Create your views here.
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

    }
   
    return render(request, "analysis/daily_report.html", context)

def new(request):
    regi5G = Register.objects.filter(category = "5G")
    regiLTE = Register.objects.filter(category = "LTE")
    regiWiFi = Register.objects.filter(category = "WiFi")
    regiweak = Register.objects.filter(category = "품질취약지역")
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

    context = {'regi5G':regi5G,'regiLTE':regiLTE,'regiWiFi':regiWiFi,'regiweak':regiweak, 'sregi':sregi,
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
        register.category = request.POST['category']
        if(register.category == "5G"):
            register.dong = request.POST['dong']
            register.dagyo = request.POST['dagyo']
            register.coverage5g = request.POST['coverage5g']
            register.total = int(register.dong)+int(register.dagyo)+int(register.coverage5g)
        elif(register.category == "LTE"):
            register.bigct = request.POST['bigct']
            register.smallct = request.POST['smallct']
            register.inbuiling = request.POST['inbuiling']
            register.nong = request.POST['nong']
            register.theme = request.POST['theme']
            register.coveragelte = request.POST['coveragelte']
            register.total =  int(register.bigct)+ int(register.smallct)+ int(register.nong)+ int(register.inbuiling)+ int(register.theme)+ int(register.coveragelte)
        elif(register.category == "WiFi"):
            register.sangyong = request.POST['sangyong']
            register.gaebang = request.POST['gaebang']
            register.total =  int(register.sangyong)+ int(register.gaebang)
        else:
            register.mountain =request.POST['mountain']
            register.ship = request.POST['ship']
            register.yooin = request.POST['yooin']
            register.searoad = request.POST['searoad']
            register.total =  int(register.mountain)+ int(register.ship)+ int(register.yooin)+ int(register.searoad)
        
        # if(register.category == "5G"):
        #     register.total = int(register.dong)+int(register.dagyo)+int(register.coverage)
        # elif(register.category == "LTE"):
        #     register.total =  int(register.bigct)+ int(register.smallct)+ int(register.nong)+ int(register.inbuiling)+ int(register.theme)+ int(register.coverage)
        # elif(register.category == "WiFi"):
        #     register.total =  int(register.sangyong)+ int(register.gaebang)
        # else:
        #     register.total =  int(register.mountain)+ int(register.ship)+ int(register.yooin)+ int(register.searoad)
        
            
        Register.objects.filter(category = register.category).delete()
        register.save()

    return redirect("new")

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

def delete_todayregister(request):
    if(request.method== "POST") :
       
       TodayRegister.objects.all().delete()
       
       

    return redirect("new")
def test_layout(request):

    return render(request, "analysis/test_layout.html")