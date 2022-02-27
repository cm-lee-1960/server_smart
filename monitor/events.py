from django.conf import settings
from haversine import haversine # 이동거리
# from geopy.geocoders import Nominatim # 역지오코딩(위도,경도->주소)
import requests
from .geo import KakaoLocalAPI
from .models import Message

###################################################################################################
# 이벤트 발생여부를 체크하는 모듈
# [ 이벤트 처리내역 ]
#  1) 전송실패(Send Failure)
#  2) 속도저하(low throughput)
#  3) 음성 콜 드랍
#  4) 5G -> LTE 전환
#  5) 측정범위를 벗어나는 경우
#  6) 측정콜이 한곳에 머무는 경우
# -------------------------------------------------------------------------------------------------
# 2022.02.24 - 기존 속도저하(Low Throughput)을 통화불량(Call Failure)로 변경하고, 
#              새롭게 속도저하(Low Throughput) 모듈을 추가함
# 2022.02.27 - 메시지 작성 코드를 각각의 이벤트를 체크하는 함수 내부로 이동함 (이벤트 발생 관련정보를 메시지 내에 넣기 위해)
###################################################################################################  
def event_occur_check(mdata):
    '''이벤트 발생여부를 체크한다.'''
    # 1)전송실패(Send Failure)
    message = send_failure_check(mdata)
    if message : make_event_message(mdata, message)

    # 2)속도저하(low throughput)
    message = low_throughput_check(mdata)
    if message: make_event_message(mdata, message)
    
    # 3)음성 콜 드랍
    message = voice_call_drop_check(mdata)
    if message: make_event_message(mdata, message)

    # 4)5G -> LTE 전환
    message = fivgtolte_trans_check(mdata)
    if message: make_event_message(mdata, message)

    # 4)측정범위를 벗어나는 경우
    message = out_measuring_range(mdata)
    if message: make_event_message(mdata, message)

    # 6)측정콜이 한곳에 머무는 경우
    message = call_staying_check(mdata)
    if message: make_event_message(mdata, message)

# -------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 발생여부 확인
# 2022.02.24 - WiFi 전송실패 기준 추가 (DL: 1M, UL: 0.5M)
#--------------------------------------------------------------------------------------------------
def send_failure_check(mdata):
    '''전송실패(Send Failure) 발생여부 확인
        - 품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
        - 품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
        - 취약지구는 '~산로' 등 특정문구가 들어간 것으로 식별을 해야 하는데, 어려움이 있음(관리자 지정해야? -> 정보관리 대상)
        - return message
    '''
    # 측정종류가 속도(speed)일 때만 이벤트 발생여부를 학인한다. 
    message = None
    if mdata.testNetworkType == 'speed' :
        # 전송실패 판단기준
        LOW_THROUGHPUT_TABLE = {
            '5G' : {'DL': 12, 'UL': 2},
            'LTE': {'DL': 6, 'UL': 1},
            '3G' : {'DL': 256/1024, 'UL': 128/1024},
            'WiFi': {'DL': 1, 'UL': 0.5} }

        # 측정 단말기 및 데이터 유형(DL/UL)을 확인한다. 
        dataType = None
        phone = mdata.phone
        if mdata.downloadBandwidth and mdata.downloadBandwidth > 0 : dataType = 'DL'
        if mdata.uploadBandwidth and mdata.uploadBandwidth > 0 : dataType = 'UL'
        values = {'DL': mdata.downloadBandwidth, 'UL': mdata.uploadBandwidth}
        # 2022.0227 DL/UL 속도 값이 있는 데이터에 대해서만 처리한다.
        if dataType and dataType in ['DL', 'UL']:
            try:
                if phone.networkId in list(LOW_THROUGHPUT_TABLE.keys()):
                    if values[dataType] < LOW_THROUGHPUT_TABLE[phone.networkId][dataType]:
                        # 메시지 내용을 작성한다.
                        message = f"{mdata.userInfo1}전송실패가 발생하였습니다.\n" + \
                                f"{mdata.phone_no}/{mdata.networkId}/{mdata.downloadBandwidth}/{mdata.uploadBandwidth}"
            except Exception as e:  
                print("low_throughput_check():"+str(e))
    
    return message

# -------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 발생여부 확인
# 2022.02.24 속도저하 기준 별도 테이블 관리 필요 -- LowThroughput
#--------------------------------------------------------------------------------------------------
def low_throughput_check(mdata):
    '''속도저하(Low Throughput) 발생여부 확인
        - 속도저하 기준 별도 테이블 관리 예정
        - return 'CALLFAIL'
    '''
    message = None
    # *** 속도저하 판단 기준(DB)에서 가져와서 확인하는 코드 작성필요
    # # 메시지 내용을 작성한다. 
    # message = f"{mdata.userInfo1}에서 속도저하(Low Throughput)가 발생했습니다.\n" + \
    #             f"{mdata.phone_no}/{mdata.networkId}/{mdata.downloadBandwidth}/{mdata.uploadBandwidth}"

    return message

# -------------------------------------------------------------------------------------------------
# 음성 콜 드랍 발생여부 확인
#--------------------------------------------------------------------------------------------------
def voice_call_drop_check(mdata):
    ''' 음성 콜 드랍 발생여부 확인
        - 품질 취약 VoLTE call drop/setup fail, 3G call drop/setup fail
    '''
    message = None
    # 2022.01.17 DB가 다르기 때문에 나중에 알려 주겠음
    # message = "음성 콜 드랍이 발생했습니다."

    return message

# -------------------------------------------------------------------------------------------------
# 5G에서 LTE료 전환여부 확인
#--------------------------------------------------------------------------------------------------
def fivgtolte_trans_check(mdata):
    ''' 5G에서 LTE료 전환여부 확인
        - 5G 측정시 LTE로 데이터가 전환되는 경우
        - return 'FIVETOLTE'
    '''
    message = None
    # 2022.02.21 - 측정 데이터 안에는 NR인 경우가 5G -> LTE로 전환된 것임
    # 2022.02.27 - 메시지 내용을 작성한다.
    if mdata.phone.networkId == '5G' and mdata.networkId == 'NR':
        message = f"{mdata.userInfo1}에서 5G->LTE로 전환되었습니다.\n" + \
                    f"{mdata.phone_no}/{mdata.networkId}/{mdata.downloadBandwidth}/{mdata.uploadBandwidth}"

    return message

# -------------------------------------------------------------------------------------------------
# 단말이 측정범위를 벗어났는지 확인
# 2022.02.21 - 측정유형(userinfo2)이 행정동("행-")인 경우만 처리하는 것이 맞지 않나? 
#            - 행정동: 도로주행 측정, 테마: 놀이공원 등 걸어서 측정, 인빌딩: 건물내 걸어서 측정
# 2022.02.27 - 측정 단말기 상세주소(addressDetail) 항목에서 행정동을 비교한다. 
#            - 측정 데이터의 경우 위도,경도에 따른 상세주소가 잘못되어 있는 데이터가 있음 (측정 단말기에 처음 상세주소 가져감)
#            - 측정 단말기에 있는 상세주소와 해당 측정 데이터의 위도,경도로 행정동을 찾아서 비고하도록 소스코드 수정함
#
#--------------------------------------------------------------------------------------------------
def out_measuring_range(mdata):
    ''' 단말이 측정범위를 벗어났는지 확인
        - 측정하는 행정동을 벗어나서 측정이 되는 경우
        - (아이디어) 행정동을 벗어남이 의심된다는 메시지 + 위치 지도 이미지도 함께 전송
        - return 'OUTRANGE'
    '''
    message = None
    # 측정유형이 행정동인 경우에만 단말이 측정범위를 벗어났는지 확인한다.
    if not mdata.userInfo2.startswith("행-") : return None

    # 2.20 역지오코딩 - 도로명 주소로 반환되어 카카오지도 API로 대체
    # geolocator = Nominatim(user_agent="myGeolocator")
    # location = geolocator.reverse(str(mdata.latitude) + ',' + str(mdata.longitude))
    # Location(영서로, 학곡리, 춘천시, 강원도, 24408, 대한민국, (37.81069349300918, 127.7657987426381, 0.0))
    # print("out_measuring_range():", location)

    rest_api_key = settings.KAKAO_REST_API_KEY
    kakao = KakaoLocalAPI(rest_api_key)
    input_coord = "WGS84" # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

    result = kakao.geo_coord2address(mdata.longitude, mdata.latitude, input_coord)
    # print("out_measuring_range():", result)
    # {'meta': {'total_count': 1}, 
    #   'documents': [
    #       {'road_address': None, 
    #       'address': 
    #       {'address_name': '강원 춘천시 동내면 사암리 산 121-1', 'region_1depth_name': '강원', 
    #       'region_2depth_name': '춘천시', 'region_3depth_name': '동내면 사암리', 'mountain_yn': 'Y', 
    #       'main_address_no': '121', 'sub_address_no': '1', 'zip_code': ''}}]}
    # meta,
    # document -> road_address
    #          -> address -> region_3depth_name
    # 좌표(위도,경도)로 찾은 주소와 어떤 것을 비교할지? 고민필요
    # userInfo1가 위도,경도 좌표로 변환한 행정동을 포함하고 있는지 확인
    try: 
        region_3depth_name = result['documents'][0]['address']['region_3depth_name'].split()[0]
        if mdata.phone.addressDetail and mdata.phone.addressDetail.find(region_3depth_name) == -1:
            message = f"{mdata.userInfo1}에서 측정단말이 측정범위를 벗어났습니다.\n" + \
                    "(전화번호/단말시작위치/위도/경도/측정위치)\n" + \
                    f"{mdata.phone_no}/{mdata.phone.addressDetail.split()[0]}/{mdata.latitude}/{mdata.longitude}/{region_3depth_name}"

    except Exception as e:
        print("out_measuring_range():", str(e))

    return message

# -------------------------------------------------------------------------------------------------
# 측정단말이 한곳에 머무는지 확인
# 2022.02.22 - 처리대상 데이터를 속도측정 데이터('speed')에 한정하여 처리한다.  
#            - 행정동 측정일때만 체크한다. (예: 테마의 경우 위도,경도가 동일한 경우가 다수 발생함)
#            - 행정동: 도로주행 측정, 테마: 놀이공원 등 걸어서 측정, 인빌딩: 건물내 걸어서 측정
#--------------------------------------------------------------------------------------------------
def call_staying_check(mdata):
    ''' 측정단말이 한곳에 머무는지 확인
        - 타사 측정단말에 문제가 발생하여 조치를 하거나 차량에 문제가 있거나 등 한곳에 오랫동안 멈는 경우가 있는데,
          이렇게 한곳에 멈춰 있는 경우 보고 대상임
        - 이동거리가 5미터 이내 연속해서 3회 이상 발생하면 한 곳에 머무는 것으로 판단 <- 기준확인 필요
        - return message
    '''
    message = None
    # 측정유형이 행정동인 경우에만 측정단말이 한곳에 머무는지 확인한다.
    if mdata.userInfo2.startswith("행-"):
        # mdata_list = mdata.phone.measurecalldata_set.all()
        mdata_list = mdata.phone.measurecalldata_set.filter(testNetworkType='speed').order_by("-currentCount")
        count = len(mdata_list)
        callstay = True
        # 이동거리를 확인하기 위해서는 측정값이 6건 이상 있어야 한다.
        if count >= 6:
            # for idx, md in enumerate(mdata_list[count-1::-1]):
            result = ''
            for idx, md in enumerate(mdata_list):
                if idx == 0:
                    before_loc = (md.latitude, md.longitude)
                else:
                    # 두 측정저점간의 이동거리를 계산한다. 
                    current_loc = (md.latitude, md.longitude)
                    distance = haversine(before_loc, current_loc) * 1000 # 미터(meters)
                    # print("call_staying_check():", idx, str(md), distance, before_loc, current_loc)
                    # 측정 단말기 이동거리가 5M 이상이 되면 한곳에 머무르지 않고, 이동하는 것으로 판단한다.
                    result += str(before_loc)+ '/' + str(current_loc) + '/' + str(distance) + ',\n'
                    if distance > 10 :
                        callstay = False
                        break
                    before_loc = current_loc
                if idx >= 6 : break
        else:
            callstay = False

        if callstay: 
            # 메시지 내용을 작성한다.
            message = f"{mdata.userInfo1}에서 측정단말이 한곳에 머물러 있습니다.\n" + \
                        f"{mdata.phone_no}/{mdata.latitude}/{mdata.longitude}/{mdata.addressDetail}\n" + \
                        "[검증데이터]\n" + result
    return message

# -------------------------------------------------------------------------------------------------
# 이벤트 메시지 작성 함수
# 2022.02.27 - 메시지 포맷 정의 (이벤트 발생 관련 정보 표시)
#            - 메시지 작성 코드를 각각 이벤트 확인하는 함수로 이동함(메시지 내에 관련정보 포함하기 위해)
#--------------------------------------------------------------------------------------------------
def make_event_message(mdata, message):
    '''이벤트 메시지 작성 함수'''
    # 환경변수에서 채널ID를 가져온다.
    channelId = settings.CHANNEL_ID


    # 전송 메시지를 생성한다.
    if message:
        # 전송 메시지를 생성한다. 
        Message.objects.create(
            phone = mdata.phone,
            measdate=str(mdata.meastime)[0:8],
            sendType = 'TELE',
            userInfo1=mdata.userInfo1,
            currentCount=mdata.currentCount,
            phone_no=mdata.phone_no,
            ownloadBandwidth=mdata.downloadBandwidth,
            uploadBandwidth=mdata.uploadBandwidth,
            messageType='EVENT',
            message = message,
            channelId = channelId,
            sended=True
        )
