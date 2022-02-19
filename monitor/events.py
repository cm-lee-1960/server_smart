from haversine import haversine
from .models import Message

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


def low_throughput_check(mdata):
    '''속도저하(Low Throughput) 발생여부 확인
        - 품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
        - 품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
        - 취약지구는 '~산로' 등 특정문구가 들어간 것으로 식별을 해야 하는데, 어려움이 있음(관리자 지정해야? -> 정보관리 대상)
    '''
    low_throughput_table = {
        '5G' : {'DL': 12, 'UL': 2},
        'LTE': {'DL': 6, 'UL': 1},
        '3G' : {'DL': 256/1024, 'UL': 128/1024} }
    phone = mdata.phone
    values = {'DL': mdata.downloadBandwidth, 'UL': mdata.uploadBandwidth}
    if phone.networkId in list(low_throughput_table.keys()):
        if values[phone.phone_type] < low_throughput_table[phone.networkId][phone.phone_type]:
            return 'LOWTHR'
    return None

def voice_call_drop_check(mdata):
    ''' 음성 콜 드랍 발생여부 확인
        - 품질 취약 VoLTE call drop/setup fail, 3G call drop/setup fail
    '''
    # 2022.01.17 DB가 다르기 때문에 나중에 알려 주겠음
    return None

def fivgtolte_trans_check(mdata):
    ''' 5G에서 LTE료 전환여부 확인
        - 5G 측정시 LTE로 데이터가 전환되는 경우
    '''
    if mdata.phone.networkId != mdata.networkId:
        return 'FIVETOLTE'
    return None

def out_measuring_range(mdata):
    ''' 단말이 측정범위를 벗어났는지 확인
        - 측정하는 행정동을 벗어나서 측정이 되는 경우
        - (아이디어) 행정동을 벗어남이 의심된다는 메시지 + 위치 지도 이미지도 함께 전송
    '''
    return None

def call_staying_check(mdata):
    ''' 측정단말이 한곳에 머무는지 확인
        - 타사 측정단말에 문제가 발생하여 조치를 하거나 차량에 문제가 있거나 등 한곳에 오랫동안 멈는 경우가 있는데,
          이렇게 한곳에 멈춰 있는 경우 보고 대상임
    '''
    for md in mdata.phone.measurecalldata_set.all():
        pass
    return None

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
        'OUTRANGE': "단말이 측정범위를 벗어났습니다.",
        'CALLSTAY': "단말이 한곳에 머물러 있습니다.",
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