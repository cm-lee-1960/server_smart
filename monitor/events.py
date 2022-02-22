from haversine import haversine # 이동거리
# from geopy.geocoders import Nominatim # 역지오코딩(위도,경도->주소)
import requests
from .models import Message
from .geo import KakaoLocalAPI

###################################################################################################
# 이벤트 발생여부를 체크하는 모듈
###################################################################################################  
def event_occur_check(mdata):
    '''이벤트 발생여부를 체크한다.'''
    # 1)속도저하(low throughput)
    event_code = low_throughput_check(mdata)
    if event_code: make_event_message(mdata, event_code)
    
    # 2)음성 콜 드랍
    event_code = voice_call_drop_check(mdata)
    if event_code: make_event_message(mdata, event_code)

    # 3)5G -> LTE 전환
    event_code = fivgtolte_trans_check(mdata)
    if event_code: make_event_message(mdata, event_code)

    # 4)측정범위를 벗어나는 경우
    event_code = out_measuring_range(mdata)
    if event_code: make_event_message(mdata, event_code)

    # 5)측정콜이 한곳에 머무는 경우
    event_code = call_staying_check(mdata)
    if event_code: make_event_message(mdata, event_code)

# -------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 발생여부 확인
#--------------------------------------------------------------------------------------------------
def low_throughput_check(mdata):
    '''속도저하(Low Throughput) 발생여부 확인
        - 품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
        - 품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
        - 취약지구는 '~산로' 등 특정문구가 들어간 것으로 식별을 해야 하는데, 어려움이 있음(관리자 지정해야? -> 정보관리 대상)
        - return 'LOWTHR'
    '''
    low_throughput_table = {
        '5G' : {'DL': 12, 'UL': 2},
        'LTE': {'DL': 6, 'UL': 1},
        '3G' : {'DL': 256/1024, 'UL': 128/1024} }
    phone = mdata.phone
    values = {'DL': mdata.downloadBandwidth, 'UL': mdata.uploadBandwidth}
    try:
        if phone.networkId in list(low_throughput_table.keys()):
            if values[phone.phone_type] < low_throughput_table[phone.networkId][phone.phone_type]:
                return 'LOWTHR'
    except Exception as e:  
        print("low_throughput_check():"+str(e))
        return None

    return None

# -------------------------------------------------------------------------------------------------
# 음성 콜 드랍 발생여부 확인
#--------------------------------------------------------------------------------------------------
def voice_call_drop_check(mdata):
    ''' 음성 콜 드랍 발생여부 확인
        - 품질 취약 VoLTE call drop/setup fail, 3G call drop/setup fail
    '''
    # 2022.01.17 DB가 다르기 때문에 나중에 알려 주겠음
    return None

# -------------------------------------------------------------------------------------------------
# 5G에서 LTE료 전환여부 확인
#--------------------------------------------------------------------------------------------------
def fivgtolte_trans_check(mdata):
    ''' 5G에서 LTE료 전환여부 확인
        - 5G 측정시 LTE로 데이터가 전환되는 경우
        - return 'FIVETOLTE'
    '''
    # 2.21 측정 데이터 안에는 NR인 경우가 5G -> LTE로 전환된 것임
    if mdata.phone.networkId == '5G' and mdata.networkId == 'NR':
        return 'FIVETOLTE'
    return None

# -------------------------------------------------------------------------------------------------
# 단말이 측정범위를 벗어났는지 확인
# 2022.02.21 - 측정유형(userinfo2)이 행정동("행-")인 경우만 처리하는 것이 맞지 않나? 
#            - 행정동: 도로주행 측정, 테마: 놀이공원 등 걸어서 측정, 인빌딩: 건물내 걸어서 측정
#--------------------------------------------------------------------------------------------------
def out_measuring_range(mdata):
    ''' 단말이 측정범위를 벗어났는지 확인
        - 측정하는 행정동을 벗어나서 측정이 되는 경우
        - (아이디어) 행정동을 벗어남이 의심된다는 메시지 + 위치 지도 이미지도 함께 전송
        - return 'OUTRANGE'
    '''
    # 측정유형이 행정동인 경우에만 단말이 측정범위를 벗어났는지 확인한다.
    if not mdata.userInfo2.startswith("행-") : return None

    # 2.20 역지오코딩 - 도로명 주소로 반환되어 카카오지도 API로 대체
    # geolocator = Nominatim(user_agent="myGeolocator")
    # location = geolocator.reverse(str(mdata.latitude) + ',' + str(mdata.longitude))
    # Location(영서로, 학곡리, 춘천시, 강원도, 24408, 대한민국, (37.81069349300918, 127.7657987426381, 0.0))
    # print("out_measuring_range():", location)

    rest_api_key = "9daef46439c87ea1a53391feb26ebb8b"
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
        if mdata.userInfo1.find(region_3depth_name) == -1:
            return 'OUTRANGE'
        else:
            return None
    except Exception as e:
        print("out_measuring_range():", str(e))
        return None

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
        - return 'CALLSTAY'
    '''
    # 측정유형이 행정동인 경우에만 측정단말이 한곳에 머무는지 확인한다.
    if not mdata.userInfo2.startswith("행-") : return None

    # mdata_list = mdata.phone.measurecalldata_set.all()
    mdata_list = mdata.phone.measurecalldata_set.filter(testNetworkType='speed').order_by("-currentCount")
    count = len(mdata_list)
    callstay = True
    # 이동거리를 확인하기 위해서는 측정값이 4건 이상 있어야 한다.
    if count >= 4:
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
                result += str(before_loc)+ '/' + str(current_loc) + '/' + str(distance) + ','
                if distance > 5 :
                    callstay = False
                    break
                before_loc = current_loc
            if idx >= 3 : break
    else:
        callstay = False
    if callstay: 
        print("###CALLSTAY", result)
        return 'CALLSTAY' 
    else:
        return None

# -------------------------------------------------------------------------------------------------
# 이벤트 메시지 작성 함수
#--------------------------------------------------------------------------------------------------
def make_event_message(mdata, evnet_code):
    '''이벤트 메시지 작성 함수'''
    channelId = '-736183270' 
    if mdata.downloadBandwidth:
        phone_type, bandwidth = 'DL', mdata.downloadBandwidth
    elif mdata.uploadBandwidth: 
        phone_type, bandwidth = 'UL', mdata.uploadBandwidth
    messages = { 
        'LOWTHR': f"속도저하(Low Throughput)가 발생했습니다.\n{phone_type}/{bandwidth:.1f}",
        'CALLDROP': "음성 콜 드랍이 발생했습니다.",
        'FIVETOLTE':"5G에서 LTE 전환되었습니다.",
        'OUTRANGE': "측정단말이 측정범위를 벗어났습니다.",
        'CALLSTAY': "측정단말이 한곳에 머물러 있습니다.",
        }

    # 전송 메시지를 생성한다.
    if evnet_code in list(messages.keys()):
        # 전송 메시지를 생성한다. 
        Message.objects.create(
            phone = mdata.phone,
            send_type = 'TELE',
            currentCount = mdata.currentCount,
            message = messages[evnet_code],
            channelId = channelId
        )
