from django.shortcuts import render,redirect
from monitor.models import Phone
from .models import Register
import pandas as pd


# Create your views here.
def make_report(request):
    phones = Phone.objects.all()
    phones1 = Phone.objects.get(pk = 2)
    phones2 = Phone.objects.filter(phone_no = 1044700193)
    
    pho = Phone.objects.all().values()
    pho = pd.DataFrame(pho)
    regi5G = Register.objects.filter(category = "5G")
    regiLTE = Register.objects.filter(category = "LTE")
    regiWiFi = Register.objects.filter(category = "WiFi")
    regiweak = Register.objects.filter(category = "품질취약지역")
    context = {'phones':phones,'phones1':phones1,'phones2':phones2,'pho':pho, 'regi5G':regi5G,'regiLTE':regiLTE,'regiWiFi':regiWiFi,'regiweak':regiweak}
   
    return render(request, "analysis/daily_report.html", context)

def new(request):
    regi5G = Register.objects.filter(category = "5G")
    regiLTE = Register.objects.filter(category = "LTE")
    regiWiFi = Register.objects.filter(category = "WiFi")
    regiweak = Register.objects.filter(category = "품질취약지역")

    context = {'regi5G':regi5G,'regiLTE':regiLTE,'regiWiFi':regiWiFi,'regiweak':regiweak}

    return render(request, "analysis/new.html", context)

def make_register(request):
    if(request.method== "POST") :
        register = Register() #빈 객체 생성
        register.category = request.POST['category']
        register.dong = request.POST['dong']
        register.dagyo = request.POST['dagyo']
        register.coverage = request.POST['coverage']
        register.bigct = request.POST['bigct']
        register.smallct = request.POST['smallct']
        register.inbuiling = request.POST['inbuiling']
        register.nong = request.POST['nong']
        register.theme = request.POST['theme']
        register.sangyong = request.POST['sangyong']
        register.gaebang = request.POST['gaebang']
        register.mountain =request.POST['mountain']
        register.ship = request.POST['ship']
        register.yooin = request.POST['yooin']
        register.searoad = request.POST['searoad']
    
        if(register.category == "5G"):
            register.total = int(register.dong)+int(register.dagyo)+int(register.coverage)
        elif(register.category == "LTE"):
            register.total =  int(register.bigct)+ int(register.smallct)+ int(register.nong)+ int(register.inbuiling)+ int(register.theme)+ int(register.coverage)
        elif(register.category == "WiFi"):
            register.total =  int(register.sangyong)+ int(register.gaebang)
        else:
            register.total =  int(register.mountain)+ int(register.ship)+ int(register.yooin)+ int(register.searoad)
        
            
        Register.objects.filter(category = register.category).delete()
        register.save()

    return redirect("new")
