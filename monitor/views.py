from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from .models import Restapp
#from .serializers import RestappSerializer
from rest_framework.parsers import JSONParser
from .models import Phone, MeasureCallData, MeasureSecondData
# from telemsg.tele_msg_old import send_message_bot

# Create your views here.

@csrf_exempt
def receive_json(request):
    if request.method != 'POST':
        return HttpRespose("Error")
    data = JSONParser().parse(request)
    print(data)
  
    # -------------------------------------------------------------------------------------------------
    # 전화번호에 대한 특정 단말이 있는지 확인한다.
    # * 측정중인 단말이 있으면 가져오고,
    # * 측정중인 단말이 없으면 새로운 측정단말을 등록한다(테이블에 등록)
    # ★ ★ ★ ★ 새롭게 발견된 사항  ★ ★ ★ ★ ★ ★ ★ ★
    # 2022.01.18 - 측정시 UL/DL 두개의 단말기로 측정하기 때문에 두개를 묶어서 처리하는 모듈 반영 필요
    #            - userInfo2, groupId
    #            - Goupp - Phone - MeasureData
    #-------------------------------------------------------------------------------------------------
    phone_no = data['phone_no']
    # phone = Phone.objects.get() -- 없는 경우 오류발생
    qs= Phone.objects.filter(phone_no=phone_no)
    if qs.exists():
        phone = qs[0]
    else:
        # 측정 단말기를 생성한다. 
        phone = Phone.objects.create(
            phone_no=phone_no,
            avg_downloadBandwidth=data['downloadBandwidth'],
            avg_uploadBandwidth=data['uploadBandwidth'],
            status='START',
            total_count=data['currentCount']
            )

    # -------------------------------------------------------------------------------------------------
    # 실시간 측정 데이터 유형에 따라서 데이터를 등록한다(콜단위, 초단위).
    # 데이터 유형에 따라서 처리내용이 달라질 수 있음 -- 판단하기 위해 JSON 데이터에 식별자를 가져가야 함
    # [ 콜단위 ] - 메시지 전송, 품질정보
    # [ 초단위 ] - 속도 업데이트, 이벤트처리
    #------------------------------------------------------------------------------------------------- 
    # 초단위 측정 데이터를 등록한다.   
    msdata = MeasureSecondData.objects.create(
        phone = phone,
        **data
        )
    
    # 측정 단말기의 통계값들을 업데이트 한다. 
    # UL/DL 측정 단말기를 함께 묶어서 통계값을 산출해야 함
    phone.update_info(msdata)

    # -------------------------------------------------------------------------------------------------
    # 관리대상 식별기준
    # 1) 통신사
    # - KT 측정 데이터(ispId = 45008)인 경우만 메시지 및 이벤트 처리를 한다.  
    # - MCC : 450(대한민국), MNC: 08(KT), 05(SKT), 60(LGU+) 
    # 2) 커버리지 유형(테마, 인빌딩, 행정동) -- 그때 그때 바뀌기 때분에 확인해야 함(관리정보 대상)
    # - ★★★어떤 유형으로 사용하는지 확인 필요
    # - 예) 테-재효-2-d3, 행-용택-1, 인빌딩은 어떻게 표시되지?
    # - 예) 커-재효-2-d3, 커버리지 1조
    #-------------------------------------------------------------------------------------------------
    if data['ispId'] == '45008' and \
        (data['userInfo2'].startswith("테-") or data['userInfo2'].startswith("행-") or data['userInfo2'].startswith("인-")):
        # 전송 메시지를 생성한다.
        phone.make_message()

        # 이벤트 발생여부를 체크한다. 
        phone.event_occur_check()
    
    return HttpResponse("Success")



    
    
        
 