from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from django.contrib import messages

from message.msg import make_message
from management.models import Morphology
from .events import event_occur_check
from .models import PhoneGroup, Phone, MeasureCallData, MeasureSecondData, get_morphology, Message
from .close import measuring_end, measuring_end_cancel, measuring_day_close, measuring_day_reclose, phonegroup_union


# 로그를 기록하기 위한 로거를 생성한다.
# import logging
# logger = logging.getLogger(__name__)

####################################################################################################################################
# 측정 데이터 처리모듈
#
# 1) 수신 받은 측정 데이터(JSON) 파싱
# 2) 해당일자/해당지역 측정중 단말기 그룹이 있는지 확인 ┌ -----------┐
# 3) 측정중인 단말기가 있는지 확인              ┌------>|  msg.py    |------------------┐
# 4) 측정 데이터를 저장하고, 통계정보 업데이트  |       └----------- ┘                  |
# 5) 메시지 및 이벤트 처리                      |       - make_message()                |
#                                               |                                       |
# ┌ -----------┐            ┌ -----------┐      |       ┌ -----------┐                  |
# |   url.py   |----------->|  views.py  |------┴------>| events.py  |------------------┤
# └----------- ┘            └----------- ┘              └----------- ┘                  |
#  - /monitor/json/         - receive_json()            - event_occur_check()           |
#                                 |                                                     |                       ┌ --------------┐
#                                 |                                                     |                       |      SMS      |
#       ┌-------------------------┼------------------------┐                            |               ┌------>|     (크로샷)  |
#       |                         |                        |                            |               |       |               |
#  (M)단말그룹              (M)측정단말            (M)측정 데이터                (M)메시지              |       └-------------- ┘
#  ┌ -----------┐           ┌ -----------┐          ┌ --------------┐           ┌ --------------┐       |       ┌ --------------┐               
#  | PhoneGroup |┼---------<|   Phone    |┼--------<|MeasureCallData|           |   Message     |       |       | TelegramBot   |
#  |            |           |            |          |               |           |               | ------┴------>| (tele_msg.py) |
#  |            |           |            |          |               |           |               |               |               |
#  └----------- ┘           └----------- ┘          └-------------- ┘           └-------------- ┘               └-------------- ┘
#                           - save()                                            - post_save.connect(send_message,..)
#                           - update_phone()                                      SIGNAL
#                           - update_initial_data()
#
# ----------------------------------------------------------------------------------------------------------------------------------
# 2022.03.03 - 측정 단말기 생성 후 초기에 한번 업데이트 해야 하는 모듈 추가
#            - 업데이트 항목: 단말기 행정동 위치, 모풀로지 맵핑 재지정
# 2022.03.06 - 간략한 시스템 다이어그램 작성
# 2022.03.07 - 관리대상(행정동, 테마, 인빌딩) 데이터에 대해서만 메시지 및 이벤트 발생여부를 확인한다.
#              (기존 이벤트 발생여부는 모든 데이터에 대해서 체크함)
# 2022.03.10 - 단말그룹이 자동으로 생성된 후 측정조를 지정하면 이후 해당 단말기에 대한 새로운 단말그룹이 생겼을 때 
#              기존 측정조를 갖와서 업데이트 한다.
#            - 하나의 단말그룹은 하루에 약 3개 정도 지역을 측정하게 된다.
# 2022.03.11 - 측정시작 메시지 분리
#              1) 전체대상 측정시작 메시지(START_F): 통산사, 측정유형 등에 상관없이 하루에 측정 시작시 맨처음 한번 메시지를 보냄
#              2) 해당지역 측정시작 메시지(START_M): 해당 지역에 측정을 시작하면 한번 메시지를 보냄
# 2022.03.12 - 메시지와 이벤트 처리 순서 변경 (이벤트발생 현황을 포함하여 메시지가 작성될 수 있도록 하기 위함)
#              기존: 메시지 작성 -> 이벤트발생 여부 체크
#              변경: 이벤트발생 여부 체크 -> 메시지 작성
# 2022.03.14 - 단말그룹에 대한 측정조 자동조회 설정
#              단말그룹에 속한 단말기들에 대한 기존 측정 데이터가 있고, 측정조가 편성되어 있다면 가져와서 자동 업데이트
#            - 당일 동일지억에 대해 모폴러지가 달라도 하나의 그룹으로 묶이는 현상 조치
#              예)행정동+커버리지, 테마+커버리지
#              * 현재 그룹생성 기준: 측정일자(YYYYMMDD) + 측정자 입력값1(userInfo1) + 통신사(ispId)
#              * 변경 그룹생성 기준: 측정일자(YYYYMMDD) + 측정자 입력값1(userInfo1) + 측정자 입력값2(userInfo2) + 통신사(ispId)
# 2022.03.22 - 단말그룹 관리대상 여부 항목 추가
#
####################################################################################################################################
@csrf_exempt
def receive_json(request):
    """ JSON 데이터를 받아서 처리하는 뷰 함수
        - 측정 데이터를 JSON 형태로 받아서 처리한다.
    """
    # ------------------------------------------------------------------------------------------------------------------
    # 1) 수신 받은 측정 데이터(JSON) 파싱
    # ------------------------------------------------------------------------------------------------------------------
    if request.method != 'POST':
        return HttpResponse("Error")

    data = JSONParser().parse(request)

    # ------------------------------------------------------------------------------------------------------------------
    # 2) 해당일자/해당지역 측정중인 단말기 그룹이 있는지 확인
    # 전화번호에 대한 특정 단말이 있는지 확인한다.
    # * 측정중인 단말이 있으면 가져오고,
    # * 측정중인 단말이 없으면 새로운 측정단말을 등록한다(테이블에 등록)
    # [ 처 리 내 역 ]
    # 2022.01.18 - 측정시 UL/DL 두개의 단말기로 측정하기 때문에 두개를 묶어서 처리하는 모듈 반영 필요
    #            - userInfo1, groupId(앞8자리), ispId(45008)
    #            - Goupp - Phone - MeasureData
    # 2022.02.22 - groupId(앞8자리) -> groupId(앞6자리)로 변경
    # 2022.02.23 - userInfo1 + meastime(8자리)
    # ------------------------------------------------------------------------------------------------------------------
    # 해당일자/해당지역 측정 단말기 그룹이 등록되어 있는지 확인한다.
    # meastime '20211101063756701'
    try: 
        measdate = str(data['meastime'])[:8] # 측정일자
        morphology = get_morphology(data['userInfo2']) # 모폴로지
        qs = PhoneGroup.objects.filter(measdate=measdate, userInfo1=data['userInfo1'], morphology=morphology, \
            ispId=data['ispId'], active=True)
        if qs.exists():
            phoneGroup = qs[0]    
        else:
            # 측정 단말기 그룹을 생성한다. 
            phoneGroup = PhoneGroup.objects.create(
                            measdate=measdate, # 측정일자
                            userInfo1=data['userInfo1'], # 측정자 입력값1
                            userInfo2=data['userInfo2'], # 측정자 입력갑2
                            morphology=morphology, # 모폴로지
                            ispId=data['ispId'], # 통신사(45008: KT, 45005: SKT, 45005: LGU+)
                            manage=morphology.manage, # 관리대상 여부
                            active=True) # 상태코드
            
    except Exception as e:
        # 오류 코드 및 내용을 반환한다.
        print("그룹조회:", str(e))
        return HttpResponse("그룹조회:" + str(e), status=500)

    # ------------------------------------------------------------------------------------------------------------------
    # 3) 측정중인 단말기가 있는지 확인  
    # 측정 단말기를 조회한다.
    # 기등록된 측정 단말기 그룹을 조회한다. -- 현재 콜카운트가 1 보다 크면 반드시 측정중인 단말기가 있어야 한다.
    # (측정 단말기 -> 측정 단말기 그룹 조회)
    # [ 해당일자 + 해당지역 + 해당전화번호 ] => 키값
    # 측, 해당일자, 해당지역에 측정하고 있는 단말(해당 전화번호)은 하나뿐이다.
    # ------------------------------------------------------------------------------------------------------------------
    try:
        qs = phoneGroup.phone_set.all().filter(phone_no=data['phone_no'], active=True)
        if qs.exists():
            phone = qs[0]
            phone.active = True
            phone.save()
        else:
            # 측정 단말기의 관래대상 여부를 판단한다.
            # 2022.02.24 - 네트워크유형(networkId)이 'NR'인 경우 5G 측정 단말로 판단한다.
            #            - 발견사례) 서울특별시-신분당선(강남-광교) 010-2921-3951 2021-11-08
            if data['networkId'] == 'NR':
                networkId = '5G'
            else:
                networkId = data['networkId']

            # 측정 단말기를 생성한다.
            # 2022.03.11 - 측정시작 메시지 분리 반영 (전체대상 측정시작: START_F, 해당지역 측정시작: START_M)
            meastime_s = str(data['meastime']) # 측정시간 (측정일자와 최초 측정시간으로 분리하여 저장)
            phone = Phone.objects.create(
                        phoneGroup = phoneGroup, # 단말그룹
                        measdate=meastime_s[0:8], # 측정일자
                        starttime=meastime_s[8:10]+ ':' + meastime_s[10:12], # 측정 시작시간
                        phone_no=data['phone_no'], # 측정단말 전화번호
                        userInfo1=data['userInfo1'], # 측정자 입력값1
                        userInfo2=data['userInfo2'], # 측정자 입력값2
                        networkId=networkId, # 측정유형(5G, LTE, 3G, WiFi)
                        ispId=data['ispId'], # 통신사(45008: KT, 45005: SKT, 45005: LGU+)
                        downloadBandwidth=0.0, # DL 평균속도
                        uploadBandwidth=0.0, # UL 평균속도
                        dl_count=0, # DL 콜카운트
                        ul_count=0, # UL 콜카운드
                        status='START_F', # 측정단말 상태코드(POWERON:파워온,START_F:측정첫시작,START_M:측정시작,MEASURING:측정중,END:측정종료)
                        currentCount=data['currentCount'], # 현재 콜카운트
                        total_count=data['currentCount'], # 총 콜카운트
                        addressDetail=data['addressDetail'], # 행정동
                        latitude=data['latitude'], # 위도
                        longitude=data['longitude'], # 경도
                        last_updated=data['meastime'], # 최종 위치보고시간
                        manage=False, # 관리대상 여부
                        active=True, # 상태
                    )
            # 측정 단말기 생성 후 초기에 한번 업데이트 해야 하는 내용을 담아 놓음
            # 1) 첫번째 측정 위치(위도,경도)에 대한 주소지를 행정동으로 변환하여 저장한다.
            # 2) 측정 데이터의 userInfo2를 확인하여 모풀로지를 매핑하여 지정한다.
            phone.update_initial_data()

            # 새롭게 생성된 단말그룹에 묶여 있는 단말기가 당일 이전 측정으로 측정조가 지정되어 있는지 확인
            # 측정조로 지정되어 있다면 그 정보를 가져와서 단말그룹에 업데이트 함
            phoneGroup.update_initial_data()

    except Exception as e:
        # 오류 코드와 내용을 반환한다.
        print("단말기조회:",str(e))
        return HttpResponse("단말기조회:" + str(e), status=500)

    # ------------------------------------------------------------------------------------------------------------------
    # 4) 측정 데이터를 저장하고, 통계정보 업데이트
    # 실시간 측정 데이터 유형에 따라서 데이터를 등록한다(콜단위, 초단위).
    # 데이터 유형에 따라서 처리내용이 달라질 수 있음 -- 판단하기 위해 JSON 데이터에 식별자를 가져가야 함
    # [ 콜단위 ] - 메시지 전송, 품질정보
    # [ 초단위 ] - 속도 업데이트, 이벤트처리
    # ------------------------------------------------------------------------------------------------------------------
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
            phone.update_phone(mdata)

    except Exception as e:
        # 오류 코드와 내용을 반환한다.
        print("데이터저장:",str(e))
        return HttpResponse("데이터저장:" + str(e), status=500)

    # ------------------------------------------------------------------------------------------------------------------
    # 5) 메시지 및 이벤트 처리
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
    # ------------------------------------------------------------------------------------------------------------------
    try:
        # 측정시작 메시지
        # 2022.02.27 - 측정시작 메시지 분리
        #            - 통신사 및 기타 조건에 상관없이 해당일자 측정이 시작하면 측정시작 메시지를 전송하도록 한다.
        # 2022.03.10 - 측정시작 메시지를 2개로 분리
        #              1) 측정시작 메시지(전체대상)
        #              2) 해당지역 측정시작 메시지
        if 'START' in mdata.phone.status:
            # 1) 측정시작 메시지(전체대상)
            #    - 전체대상 측정시작 메시지는 통신사, 측정유형에 상관없이 무조건 측정을 시작하면 한번 메시지를 보낸다.
            if mdata.phone.status == 'START_F': make_message(mdata)

            # 2) 해당지역 측정시작 메시지
            #    - 해당 지역에 대해서 측정을 시작하면 측정시작 메시지를 한번 보낸다.
            #    - 두개의 단말기로 측정을 진행하니 메시지가 한번만 갈 수 있도록 유의히야 한다.
            # (조건: KT 속도측정 데이터에 대해서만 적용)
            if mdata.phone.status == 'START_M' and mdata.ispId == '45008' and mdata.testNetworkType == 'speed': 
                make_message(mdata)

        # 2022.03.03 - 관리대상 모풀로지(행정동, 테마, 인빌딩)인 경우에만 메시지 처리를 수행한다.
        elif data['ispId'] == '45008' and data['testNetworkType'] == 'speed':
            mps= Morphology.objects.filter(manage=True).values_list('morphology', flat=True)
            if mdata.phone.morphology.morphology in mps:
                # 이벤트 발생여부를 체크한다. 
                event_occur_check(mdata)

                # 메시지를 작성한다.
                make_message(mdata)

    except Exception as e:
        # 오류 코드와 내용을 반환한다.
        print("메시지/이벤트처리:",str(e))
        return HttpResponse("메시지/이벤트처리:" + str(e), status=500)

    return HttpResponse("처리완료")


########################################################################################################################
# 해당지역 측정을 종료한다.
# ----------------------------------------------------------------------------------------------------------------------
# 2022.04.05 - 단말그룹ID를 전달 받아 측정을 종료하는 기능을 구현함
########################################################################################################################
def measuring_end_view(request, phonegroup_id):
    """ 해당일자에 대한 측정종료을 처리하는 뷰 함수
        - 파라미터
          . phonegroup_id: 단말그룹ID (int)
        - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
        """
    # 해당 단말그룹 ID로 오브젝트 데이터를 가져온다.
    qs = PhoneGroup.objects.filter(id=phonegroup_id)
    if qs.exists():
        phoneGroup = qs[0]
        # 해당 단말 그룹에 대한 측정을 종료한다.
        return_value = measuring_end(phoneGroup)
        print("dkdkdkd")
        print(return_value)
    else:
        return_value = {'result' : 'error'}

    return JsonResponse(return_value)


########################################################################################################################
# 해당지역 측정종료를 취소한다. (04.25)
def measuring_end_cancel_view(request, phonegroup_id):
    """ 해당일자에 대한 측정종료을 취소하는 뷰 함수
        - 파라미터
          . phonegroup_id: 단말그룹ID (int)
        - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
        """
    # 해당 단말그룹 ID로 오브젝트 데이터를 가져온다.
    qs = PhoneGroup.objects.filter(id=phonegroup_id)
    if qs.exists():
        phoneGroup = qs[0]
        # 해당 단말 그룹에 대한 측정종료를 취소한다.
        return_value = measuring_end_cancel(phoneGroup)
    else:
        return_value = {'result' : 'error'}

    return JsonResponse(return_value)


########################################################################################################################
# 당일 측정을 마감한다.
########################################################################################################################
def measuring_day_close_view(request, measdate):
    """ 해당일자에 대한 측정마감을 처리하는 뷰 함수
        - 파라미터
          . date: 기준일자(예: 20211101)
        - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """
    if request.method == 'GET':
        date = measdate.replace('-', '')  # 기준일자
    else:
        return_value = {'result' : '잘못된 요청입니다.'}

    # 1) 해당일자에 측정 이력이 없는 경우
    if PhoneGroup.objects.filter(measdate=date, ispId=45008).count() == 0:
        return_value = {'result': '해당일자에 측정 중인 지역이 없습니다.'}
    
    # 2) 해당일자에 측정마감이 기처리된 경우 -
    #    - 측정 진행중인 단말그룹이 없고(active=True)
    #    - 측정마감 메시지가 이미 생성되어 있는 경우(status='REPORT_ALL')
    elif PhoneGroup.objects.filter(measdate=date, ispId=45008, active=True).count() == 0 and \
        Message.objects.filter(status='REPORT_ALL', measdate=date).count() is not 0:
        return_value = {'result': '해당일자에 측정마감이 이미 처리되었습니다.'}

    # 3) 해당일자에 대한 측정마감을 처리한다.
    else:
        phoneGroup_list = PhoneGroup.objects.filter(measdate=date, ispId=45008, active=True, manage=True)  # 측정마감 대상 단말그룹
        # 해당일자의 대상 단말그룹 리스트에 대해서 측정마감을 처리한다.
        return_value = measuring_day_close(phoneGroup_list, date)

    return JsonResponse(return_value)

########################################################################################################################
# 해당 날짜 재마감 함수
def measuring_day_reclose_view(request, measdate):
    """ 해당일자에 대한 측정마감을 다시 수행하는 뷰 함수
        - 파라미터
          . date: 기준일자(예: 20211101)
        - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """
    if request.method == 'GET':
        date = measdate.replace('-', '')  # 기준일자
    else:
        return_value = {'result' : '재마감 Request는 Get Method로 요청해주세요.'}

    # 1) 해당일자에 측정 이력이 없는 경우
    if PhoneGroup.objects.filter(measdate=date, ispId=45008).count() == 0:
        return_value = {'result' : '해당일자에 대한 측정 이력이 없습니다.'}
    
    # 2) 해당일자에 측정마감이 기처리된 경우에 재마감 실행
    elif PhoneGroup.objects.filter(measdate=date, ispId=45008, active=True).count() == 0 and \
        Message.objects.filter(status='REPORT_ALL', measdate=date).count() is not 0:
        return_value = measuring_day_reclose(date)

    # 3) 해당일자에 측정마감이 되지 않은 경우
    else:
        return_value = {'result' : '해당일자에 아직 마감이 완료되지 않았습니다. 먼저 측정마감 처리해주세요.'}

    return JsonResponse(return_value)


########################################################################################################################
# 폰그룹 데이터 합치는 함수 (04.26)
## 선택한 폰그룹과 measdate/unserInfo1/networkId/ispId 가 일치하는 폰그룹들이 있을 경우 데이터를 합친다.
########################################################################################################################
def phonegroup_union_view(request, phonegroup_id):
    base_pg = PhoneGroup.objects.get(id=phonegroup_id)
    added_pg = phoneGroup.objects.filter(measdate=base_pg.measdate, userInfo1=base_pg.userInfo1, networkId=base_pg.networkId, ispId='45008').order_by('-last_updated_dt')
    for pg in added_pg:
        return_value = phonegroup_union(base_pg, pg)
    return return_value


########################################################################################################################
# 측정위치로 작성된 지도맵 파일 전달
########################################################################################################################
def maps_files(request, filename):
    """ 단말이 측정하고 있는 위치를 지도맵으로 보여주는 뷰 함수
        - 현재 측정하고 있는 주소의 행정동 경계구역을 함께 지도맵에 보여준다.
    """
    return render(request, 'maps/' + filename)