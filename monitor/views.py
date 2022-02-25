from tracemalloc import start
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import PhoneGroup, Phone, MeasureCallData, MeasureSecondData
from message.msg import make_message
from .events import event_occur_check
# from django.conf import settings

# import logging
# logger = logging.getLogger(__name__)

###################################################################################################
# 측정 데이터 처리모듈
# 1) 수신 받은 측정 데이터(JSON) 파싱
# 2) 해당일자/해당지역 측정중인 단말기 그룹이 있는지 확인
# 3) 측정중인 단말기가 있는지 확인
# 4) 측정 데이터를 저장하고, 통계정보 업데이트
# 5) 메시지 및 이벤트 처리
###################################################################################################
@csrf_exempt
def receive_json(request):
    '''JSON 데이터를 받아서 처리한다.'''
    if request.method != 'POST':
        return HttpRespose("Error")
    data = JSONParser().parse(request)
    # print(data)

    # -------------------------------------------------------------------------------------------------
    # 전화번호에 대한 특정 단말이 있는지 확인한다.
    # * 측정중인 단말이 있으면 가져오고,
    # * 측정중인 단말이 없으면 새로운 측정단말을 등록한다(테이블에 등록)
    # [ 처 리 내 역 ]
    # 2022.01.18 - 측정시 UL/DL 두개의 단말기로 측정하기 때문에 두개를 묶어서 처리하는 모듈 반영 필요
    #            - userInfo1, groupId(앞8자리), ispId(45008)
    #            - Goupp - Phone - MeasureData
    # 2022.02.22 - groupId(앞8자리) -> groupId(앞6자리)로 변경
    # 2022.02.23 - userInfo1 + meastime(8자리)
    #------------------------------------------------------------------------------------------------- 
    # 해당일자/해당지역 측정 단말기 그룹이 등록되어 있는지 확인한다.
    #  meastime '20211101063756701'
    try: 
        measdate = str(data['meastime'])[:8]
        qs = PhoneGroup.objects.filter(measdate=measdate, userInfo1=data['userInfo1'], ispId=data['ispId'], \
            active=True)
        if qs.exists():
            phoneGroup = qs[0]    
        else:
            # 측정 단말기 그룹을 생성한다. 
            phoneGroup = PhoneGroup.objects.create(
                            measdate=measdate,
                            userInfo1=data['userInfo1'],
                            ispId=data['ispId'],
                            active=True)
    except Exception as e:
        # 오류코드 리턴 필요
        print("그룹조회:",str(e))
        return HttpResponse("그룹조회:" + str(e), status=500)

    # 측정 단말기를 조회한다.
    # 기등록된 측정 단말기 그룹을 조회한다. -- 현재 콜카운트가 1 보다 크면 반드시 측정중인 단말기가 있어야 한다.
    # (측정 단말기 -> 측정 단말기 그룹 조회)
    # [ 해당일자 + 해당지역 + 해당전화번호 ] => 키값
    # 측, 해당일자, 해당지역에 측정하고 있는 단말(해당 전화번호)은 하나뿐이다.
    try:
        qs = phoneGroup.phone_set.all().filter(phone_no=data['phone_no'], active=True)
        if qs.exists():
            phone = qs[0]
            phone.active = True
            phone.save()
        else:
            # 측정 단말기의 관래대상 여부를 판단한다.
            # *** 모폴로지 조건체크는 향후 DB 테이블에서 가져오서 확인하는 코드로 변경해야 함
            if data['ispId'] == '45008' and \
                (data['userInfo2'].startswith("테-") or data['userInfo2'].startswith("행-") or data['userInfo2'].startswith("인-")):
                manage = True
            else:
                manage = False

            # 5G 측정단말인데, 네트워크 유형이 'NR' 들어오는 경우 '5G'로 처리한다.
            # 2022.02.24 - 네트워크유형(networkId)이 'NR'인 경우 5G 측정 단말로 판단한다.
            #            - 발견사례) 서울특별시-신분당선(강남-광교) 010-2921-3951 2021-11-08
            if data['networkId'] == 'NR':
                networkId = '5G'
            else:
                networkId = data['networkId']

            # 측정 단말기를 생성한다.
            phone = Phone.objects.create(
                        phoneGroup = phoneGroup,
                        measdate=str(data['meastime'])[0:8],
                        phone_no=data['phone_no'],
                        userInfo1=data['userInfo1'],
                        networkId=networkId,
                        ispId=data['ispId'],
                        avg_downloadBandwidth=0.0,
                        avg_uploadBandwidth=0.0,
                        dl_count=0,
                        ul_count=0,
                        status='START',
                        total_count=data['currentCount'],
                        last_updated=data['meastime'],
                        manage=manage,
                        active=True,
                    )

            # 2022.02.25 측정 단말기가 생성되면 첫번째 측정 시작인지 확인한다.
            make_message(phone)

    except Exception as e:
        # 오류코드 리턴 필요
        print("단말기조회:",str(e))
        return HttpResponse("단말기조회:" + str(e), status=500)

    # -------------------------------------------------------------------------------------------------
    # 실시간 측정 데이터 유형에 따라서 데이터를 등록한다(콜단위, 초단위).
    # 데이터 유형에 따라서 처리내용이 달라질 수 있음 -- 판단하기 위해 JSON 데이터에 식별자를 가져가야 함
    # [ 콜단위 ] - 메시지 전송, 품질정보
    # [ 초단위 ] - 속도 업데이트, 이벤트처리
    #------------------------------------------------------------------------------------------------- 
    try: 
        if data['dataType'] == 'call':
            # 콜단위 측정 데이터를 등록한다. 
            mdata = MeasureCallData.objects.create(phone=phone, **data)
        else:
            # 초단위 측정 데이터를 등록한다. 
            mdata = MeasureSecondData.objects.create(phone=phone, **data)
        
        # 측정 단말기의 통계값들을 업데이트 한다. 
        # UL/DL 측정 단말기를 함께 묶어서 통계값을 산출해야 함
        # 2022.02.23 통계값 산출은 KT 데이터만 처리한다(통신사코드=45008).
        # 2022.02.24 통계값 산출은 KT 데이터/속도 조건을 만족하는 경우에만 처리한다. 
        if data['ispId'] == '45008' and data['testNetworkType'] == 'speed': 
            phone.update_info(mdata)

    except Exception as e:
        # 오류코드 리턴 필요
        print("데이터저장:",str(e))
        return HttpResponse("데이터저장:" + str(e), status=500)

    # -------------------------------------------------------------------------------------------------
    # 관리대상 식별기준
    # 1) 통신사
    # - KT 측정 데이터(ispId = 45008)인 경우만 메시지 및 이벤트 처리를 한다.  
    # - MCC : 450(대한민국), MNC: 08(KT), 05(SKT), 60(LGU+) 
    # 2) 측졍유형(테마, 인빌딩, 행정동, 커버리지) -- 그때 그때 바뀌기 때분에 확인해야 함(관리정보 대상)
    # - ★★★어떤 유형으로 사용하는지 확인 필요
    # - 관리대상(O): 테-재효-2-d3, 행-용택-1, 인빌딩은 어떻게 표시되지?
    # - 관리대상(X): 커-재효-2-d3, 커버리지 1조
    # 3) 측정종류
    # - 측정종류가 속도(speed)인 경우만 메시지 및 이벤트 처리를 한다.
    # - 예) speed / latency / web
    #-------------------------------------------------------------------------------------------------
    try:
        # *** 모폴로지 조건체크는 향후 DB 테이블에서 가져오서 확인하는 코드로 변경해야 함
        if data['ispId'] == '45008' and \
            (data['userInfo2'].startswith("테-") or data['userInfo2'].startswith("행-") or data['userInfo2'].startswith("인-")) and \
            data['testNetworkType'] == 'speed':
            # 전송 메시지를 생성한다.
            make_message(phone)

            # 이벤트 발생여부를 체크한다. 
            event_occur_check(mdata)

    except Exception as e:
        # 오류코드 리턴 필요
        print("메시지/이벤트처리:",str(e))
        return HttpResponse("메시지/이벤트처리:" + str(e), status=500)
    
    return HttpResponse("성공")

    