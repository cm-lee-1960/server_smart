from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from .models import Restapp
#from .serializers import RestappSerializer
from rest_framework.parsers import JSONParser
from .models import Phone
from telemsg.tele_msg import send_message_bot

# Create your views here.

@csrf_exempt
def receive_json(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        return HttpResponse('성공')

    #1. 측정 단말기 전화번화 확인
        phone_no = data['phone_no'] ## 전화 번호
        
        phone = Phone.objects.get(phone_no=phone_no)
        
        if phone:
            pass
        else:
           phone = Phone.objects.create(Phone_no=phone_no)
        
        mdata = Measuredata.objects.create()
        phone.add_measure_data(mdata)
        send_message(phone) 
        
    # 측정 데이터 건에 대한 메시지를 전송한다.
    
    def send_message(phone):
        status = ['POWERON', 'START', 'MEASURING', 'END']
        messages = {
            'POWERON': "OO지역 단말이 켜졌습니다.",
            'START': f"측정을 시작합니다.\n{phone.phone_no} ",
            'MEASURING': f"{phone.total_count}번째 측정 데이터입니다.\n{phone.phone_no} ",
            "END": f"측정이 종료되었습니다(총{phone.total_count}건).\n{phone.phone_no} ",
        }
        if phone.status in status:
        # 측정 진행 메시지는 3, 10, 27, 37, 57 콜 단위로 보고함
            if status == 'MEASURING' and phone.total_count not in [3,10,27,37,57]:
                pass
            else:
                send_message_bot(messages[phone.status])  
 
    #2. 실시간 측정 데이터 처리
    #3. 이벤트를 체크한다.
    


########################
# 이벤트 발생을 체크한다.
# def event_occur_check():
# pass
# # 1)속도저하(low throughput)
# # 2)음성 콜 드랍
# # 3)5G -> LTE 전환
# # 4)측정범위를 벗어나는 경우
# # 5)측정콜이 한곳에 머무는 경우

# def low_throughput_check():
# # 속도저하(low throughput)
# # -품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
# # -품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
# pass
# def voice_call_drop_check():
# # 음성 콜 드랍
# # -품질 취약 VoLTE call drop/setup fail, 3G call drop/setup fail
# pass
# def fivgtolte_trans_check():
# # 5G->LTE 전환시
# # -5G 측정시 LTE로 데이터가 전환되는 경우
# pass
# def out_measuring_range():
# # 측정범위를 벗어하는 경우
# # - 측정하는 행정동을 벗어나서 측정이 되는 경우
# # - (아이디어) 행정동을 벗어남이 의심된다는 메시지 + 위치 지도 이미지도 함께 전송
# pass

# def call_staying_check():
# # 측정콜이 한곳에 머무는 경우
# # - 타사 측정단말에 문제가 발생하여 조치를 하거나 차량에 문제가 있거나 등 한곳에 오랫동안 멈는 경우가 있는데,
# # 이렇게 한곳에 멈춰 있는 경우 보고 대상임
# pass

# # 측정이 종료되었는지 확인한다.
## 주기적으로 체크 필요( ex)장고 스케쥴 )

# def measuring_end_check(self):
# # 마지막 이전 측정시점과 현재 측정시점의 시간간격을 계산한다(초).
# try:
# datetime_fmt = '%Y-%m-%d %H:%M:%S'
# diff = datetime.strptime(datetime.now().strftime(datetime_fmt), datetime_fmt) - \
# datetime.strptime(self.last_update_dt, datetime_fmt)
# if self.tot_count >= self.target_call_count and diff.total_seconds() > self.normal_call_interval:
# self.send_message('END')
# return True
# else:
# return False

# except Exception as e:
# raise CustomError("Phone->measuring_end_check(): " + str(e))
    
    
        
 