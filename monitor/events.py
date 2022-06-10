import math
from datetime import datetime, timedelta
from django.conf import settings
from haversine import haversine  # 이동거리
from management.models import SendFailure, LowThroughput
from .geo import KakaoLocalAPI, make_map_locations
from .models import MeasureCallData, Phone, Message

########################################################################################################################
# 이벤트 발생여부를 체크하는 모듈
# [ 이벤트 처리내역 ]
#  1) 전송실패(Send Failure)
#  2) 속도저하(low throughput)
#  3) 음성 콜 드랍
#  4) 5G -> LTE 전환
#  5) 측정범위를 벗어나는 경우
#  6) 측정콜이 한곳에 머무는 경우
#  7) 측정단말이 중복 측정하는 경우(예: DL/DL, UL/UL)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.02.24 - 기존 속도저하(Low Throughput)을 통화불량(Call Failure)로 변경하고, 
#              새롭게 속도저하(Low Throughput) 모듈을 추가함
# 2022.02.27 - 메시지 작성 코드를 각각의 이벤트를 체크하는 함수 내부로 이동함 (이벤트 발생 관련정보를 메시지 내에 넣기 위해)
# 2022.02.27 - 오류 발생시 앞단으로 오류코드를 전달하기 위해 Exception을 발생하여 실행중인 함수명과 오류 메시지 전달
# 2022.03.01 - 전송실패 기준 관리 모듈 추가 및 이벤트 모듈에 반영(기존 소스코드 체크 -> DB 모델에서 불러와 체크)
# 2022.03.04 - 하드코딩 되어 있는 조건문 => DB 관리기준 조회 조건문으로 변환 (보통지역, 최약지역 구분)
# 2022.03.10 - 모델에서 다른 항목조건 및 연산을 해서 가져와야 하는 중복코드들을 모두 모델 함수로 이동(get함수)
# 2022.03.15 - 여러개의 이벤트 발생시 하나의 메시지로 통합해서 보내기
#            - 두 개의 단말이 중복측정하고 있는지 확인하는 이벤트 모듈 추가
# 2022.03.28 - 단말그룹의 이벤트발생 건수를 업데이트 하는 코드를 추가함
# 2022.03.30 - 전송실패 이벤트 발생시 시 속도저하 이벤트를 체크하지 않음
# 2022.04.08 - 메시지 모델에 단말그룹 추가에 따른 업데이트 코드 추가
# 2022.05.01 - 이벤트 건수에 전송실패 건수만 반영 및 DL/UL 전송실패 건수 항목 추가
# 2022.05.23 - 채널ID를 센터정보에서 가져온다.
#
########################################################################################################################
def event_occur_check(mdata: MeasureCallData):
    """이벤트 발생여부를 체크한다.
        - 1)전송실패(Send Failure)
        - 2)속도저하(low throughput)
        - 3)음성 콜 드랍
        - 4)5G->LTE 전환
        - 5)측정범위를 벗어나는 경우
        - 6)측정콜이 한곳에 머무는 경우
        - 7)측정단말이 중복측 정하는 경우
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '전송실패' or None
    """

    events_list = []
    # 1)전송실패(Send Failure)
    message = send_failure_check(mdata)
    if message and message is not None: events_list.append(message)

    # 2)속도저하(low throughput)
    if ('DL전송실패' not in events_list) and ('UL전송실패' not in events_list):
        message = low_throughput_check(mdata)
        if message and message is not None: events_list.append(message)

    # 3)음성 콜 드랍
    message = voice_call_drop_check(mdata)
    if message and message is not None: events_list.append(message)

    # 4)5G -> LTE 전환
    message = fivgtolte_trans_check(mdata)
    if message and message is not None: events_list.append(message)

    # 5)측정범위를 벗어나는 경우
    message = out_measuring_range(mdata)
    if message and message is not None: events_list.append(message)

    # 6)측정콜이 한곳에 머무는 경우
    message = call_staying_check(mdata)
    if message and message is not None: events_list.append(message)

    # 7)측정단말이 중복측 정하는 경우(예: DL/DL, UL/UL)
    message = duplicated_measuring(mdata)
    if message and message is not None: events_list.append(message)

    # 이벤트가 여러 건 발생한 경우 이벤트 메시지를 하나의 메시지로 통합한다.
    if len(events_list) > 0: make_event_message(mdata, events_list)


# ----------------------------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 발생여부 확인
# 2022.02.24 - WiFi 전송실패 기준 추가 (DL: 1M, UL: 0.5M)
# 2022.03.01 - 전송실패 기준 관리 모듈 추가 및 이벤트 모듈에 반영(기존 소스코드 체크 -> DB 모델에서 불러와 체크)
# ----------------------------------------------------------------------------------------------------------------------
def send_failure_check(mdata: MeasureCallData) -> str:
    """전송실패(Send Failure) 발생여부 확인
        - 전송실패 기준 정보(SendFailure)는 데이터베이스에 관리한다.
        - 품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
        - 품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '전송실패' or None
    """
    message = None
    try:
        if mdata.phone.morphology.morphology and mdata.phone.morphology.morphology == '취약지역':
            areaInd = 'WEEK'  # 취약지역
        else:
            areaInd = 'NORM'  # 보통지역
        networkId = mdata.phone.networkId
        dataType = ''
        if mdata.downloadBandwidth and mdata.downloadBandwidth > 0: dataType, bandwidth = 'DL', mdata.downloadBandwidth
        if mdata.uploadBandwidth and mdata.uploadBandwidth > 0: dataType, bandwidth = 'UL', mdata.uploadBandwidth
        if dataType in ('DL', 'UL'):

            qs = SendFailure.objects.filter(areaInd=areaInd, networkId=networkId, dataType=dataType)
            if qs.exists():
                if bandwidth < qs[0].bandwidth:
                    # # 메시지 내용을 작성한다.
                    # message = f"{mdata.address}에서 전송실패가 발생하였습니다.\n" + \
                    #         "(단말번호/시간/콜카운트/PCI/Cell ID/DL/UL/RSRP/SINR)\n" + \
                    #         f"{mdata.phone_no_sht} / {mdata.time} / {mdata.currentCount} / {mdata.get_pci} / {mdata.cellId} / " + \
                    #         f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
                    message = dataType + '전송실패'
            # print("####", qs.exists(), f"{areaInd}/{networkId}/{dataType}")

                    # 단말그룹의 이벤트 발생건수를 하나 증가시킨다.
                    if dataType == 'DL':
                        mdata.phone.phoneGroup.send_failure_dl_count += 1
                        mdata.phone.phoneGroup.event_count += 1  # 전체 이벤트 건수(전송실패)
                    elif dataType == 'UL':
                        mdata.phone.phoneGroup.send_failure_ul_count += 1
                        mdata.phone.phoneGroup.event_count += 1  # 전체 이벤트 건수(전송실패)
                    mdata.phone.phoneGroup.save()

    except Exception as e:
        print("send_failure_check():", str(e))
        raise Exception("send_failure_check(): %s" % e)

    return message


# ----------------------------------------------------------------------------------------------------------------------
# 속도저하(Low Throughput) 발생여부 확인
# 2022.02.24 - 속도저하 기준 별도 테이블 관리 필요 -- LowThroughput
# 2022.03.03 - 속도저하 기준 테이블(모델) 생성 및 체크 모듈 작성
# ----------------------------------------------------------------------------------------------------------------------
def low_throughput_check(mdata: MeasureCallData) -> str:
    """속도저하(Low Throughput) 발생여부 확인
        - 속도저하 기준 정보(LowThroughput)와 비교하여 이벤트 발생여부를 판단한다.
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '속도저하' or None
    """
    message = None
    try:
        if mdata.phone.morphology.morphology and mdata.phone.morphology.morphology == '취약지역':
            areaInd = 'WEEK'  # 취약지역
        else:
            areaInd = 'NORM'  # 보통지역
        networkId = mdata.phone.networkId
        # 해당 측정 데이터가 DL인지, UL인지 확인한다.
        dataType = ''
        if mdata.downloadBandwidth and mdata.downloadBandwidth > 0: dataType, bandwidth = 'DL', mdata.downloadBandwidth
        if mdata.uploadBandwidth and mdata.uploadBandwidth > 0: dataType, bandwidth = 'UL', mdata.uploadBandwidth
        if dataType in ('DL', 'UL'):

            # 데이터베이스에서 속도저하 판단 기준을 조회한다.
            qs = LowThroughput.objects.filter(areaInd=areaInd, networkId=networkId, dataType=dataType)
            if qs.exists():
                if bandwidth < qs[0].bandwidth:
                    # # 메시지 내용을 작성한다.
                    # message = f"{mdata.address}에서 속도저하가 발생했습니다.\n" + \
                    #         "(시간/단말번호/시간/콜카운트/PCI/Cell ID/DL/UL/RSRP/SINR)\n" + \
                    #         f"{mdata.phone_no_sht} / {mdata.time} / {mdata.currentCount} / {mdata.get_pci()} / {mdata.cellId} / " + \
                    #         f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
                    message = dataType + '속도저하'
                    # print("####", qs.exists(), f"{areaInd}/{networkId}/{dataType}")

    except Exception as e:
        print("low_throughput_check():", str(e))
        raise Exception("low_throughput_check(): %s" % e)

    return message


# ----------------------------------------------------------------------------------------------------------------------
# 음성 콜 드랍 발생여부 확인
# ----------------------------------------------------------------------------------------------------------------------
def voice_call_drop_check(mdata: MeasureCallData) -> str:
    """ 음성 콜 드랍 발생여부 확인
        - 품질 취약 VoLTE call drop/setup fail, 3G call drop/setup fail
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '음성콜 드랍' or None
    """
    message = None
    # 2022.01.17 DB가 다르기 때문에 나중에 알려 주겠음
    # message = "음성 콜 드랍이 발생했습니다."

    return message


# ----------------------------------------------------------------------------------------------------------------------
# 5G에서 LTE료 전환여부 확인
# ----------------------------------------------------------------------------------------------------------------------
def fivgtolte_trans_check(mdata: MeasureCallData) -> str:
    """ 5G에서 LTE료 전환여부 확인
        - 5G 측정시 LTE로 데이터가 전환되는 경우
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: 'LTE전환' or None
    """
    message = None
    # 2022.02.21 - 측정 데이터 안에는 NR인 경우가 5G -> LTE로 전환된 것임
    # 2022.02.27 - 메시지 내용을 작성한다.
    if mdata.phone.networkId == '5G' and mdata.networkId == 'NR':
        # message = f"{mdata.address}에서 5G->LTE로 전환되었습니다.\n" + \
        #             "(단말번호/시간/콜카운트/DL/UL/RSRP/SINR)\n" + \
        #             f"{mdata.phone_no_sht} / {mdata.time} / {mdata.currentCount} / " + \
        #             f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
        message = 'LTE전환'

    return message


# ----------------------------------------------------------------------------------------------------------------------
# 단말이 측정범위를 벗어났는지 확인
# 2022.02.21 - 측정유형(userinfo2)이 행정동("행-")인 경우만 처리하는 것이 맞지 않나?
#            - 행정동: 도로주행 측정, 테마: 놀이공원 등 걸어서 측정, 인빌딩: 건물내 걸어서 측정
# 2022.02.27 - 측정 단말기 상세주소(addressDetail) 항목에서 행정동을 비교한다.
#            - 측정 데이터의 경우 위도,경도에 따른 상세주소가 잘못되어 있는 데이터가 있음 (측정 단말기에 처음 상세주소 가져감)
#            - 측정 단말기에 있는 상세주소와 해당 측정 데이터의 위도,경도로 행정동을 찾아서 비고하도록 소스코드 수정함
# 2022.02.27 - 행정동을 측정하는데, 여러 개의 동을 걸쳐서 측정하는 경우가 있음 <= 데이터 검증 필요
#            - 경상남도-사천시-남양동 2021.11.01 : 죽림동, 송포동, 노룡동 등
# 2022.03.01 - 측정범위를 벗어난 경우 측정 위치 및 경로를 지도맵(Folium)에 표시한다.
#            - 향후 작성된 지도맵을 이미지 형태로 텔레그램 메시지에 첨부하여 보내기 위함
# 2022.03.03 - 위,경도에 따른 행정동 검색 오류 수정 (2.27 이슈해결)
# 2022.06.08 - 행정구역 경계면 측정시 '측정범위 벗어남' 이벤트 다수 발생으로 측정지점으로부터 상하좌우 100m 오프셋 지역의
#              행정구역을 확인하는 모듈을 추가함
# ----------------------------------------------------------------------------------------------------------------------
# def out_measuring_range(mdata: MeasureCallData) -> str:
#     """ 단말이 측정범위를 벗어났는지 확인
#         - 측정하는 행정동을 벗어나서 측정이 되는 경우
#         - 파라미터
#           . mdata: 측정 데이터(콜단위)
#         - 반환값: '측정범위 벗어남' or None
#     """
#     message = None
#     # 측정유형이 행정동인 경우에만 단말이 측정범위를 벗어났는지 확인한다.
#     if mdata.phone.morphology.morphology != '행정동': return None
#     if not (mdata.longitude and mdata.latitude): return None
#
#     # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
#     rest_api_key = settings.KAKAO_REST_API_KEY
#     kakao = KakaoLocalAPI(rest_api_key)
#     input_coord = "WGS84"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
#     output_coord = "TM"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
#
#     result = kakao.geo_coord2regioncode(mdata.longitude, mdata.latitude, input_coord, output_coord)
#     # [ 리턴값 형식 ]
#     # print("out_measuring_range():", result)
#     # {'meta': {'total_count': 2},
#     # 'documents': [{'region_type': 'B',
#     # 'code': '4824012400',
#     # 'address_name': '경상남도 사천시 노룡동',
#     # 'region_1depth_name': '경상남도',
#     # 'region_2depth_name': '사천시',
#     # 'region_3depth_name': '노룡동', <-- 주소지 동
#     # 'region_4depth_name': '',
#     # 'x': 296184.5342265043,
#     # 'y': 165683.29710986698},
#     # {'region_type': 'H',
#     # 'code': '4824059500',
#     # 'address_name': '경상남도 사천시 남양동',
#     # 'region_1depth_name': '경상남도',
#     # 'region_2depth_name': '사천시',
#     # 'region_3depth_name': '남양동', <-- 행정구역
#     # 'region_4depth_name': '',
#     # 'x': 297008.1130364056,
#     # 'y': 164008.47612447804}]}
#     # 좌표(위도,경도)로 찾은 주소와 어떤 것을 비교할지? 고민필요
#     # userInfo1가 위도,경도 좌표로 변환한 행정동을 포함하고 있는지 확인
#     # 2022.02.28 - 단말기가 처음 측정을 시작할 때(현재 콜카운트가=1) 위치(위도,경도)가 정확하다고 가정하고 그때이 상세주소 값을
#     #              측정 단말기 정보에 가져간다.
#     #            - 측정 단말기의 상세주소와 해당 측정 데이터의 위도,경도를 통해 찾은 행정도 명칭과 비교한다.
#     try:
#         region_3depth_name = result['documents'][1]['region_3depth_name']
#         if mdata.phone.addressDetail and mdata.phone.addressDetail.find(region_3depth_name) == -1:
#             # # 메시지를 작성한다.
#             # message = f"{mdata.address}에서 측정단말이 측정범위를 벗어났습니다.\n" + \
#             #         "(단말번호/측정 행정동(현재 행정동)/시간/콜카운트/DL/UL/RSRP/SINR)\n" + \
#             #         f"{mdata.phone_no_sht} / {mdata.phone.addressDetail}({region_3depth_name}) / {mdata.time} / {mdata.currentCount} / " + \
#             #         f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
#             message = f'측정범위 벗어남({region_3depth_name})'
#
#     except Exception as e:
#         print("out_measuring_range():", str(e))
#         raise Exception("out_measuring_range(): %s" % e)
#
#     return message
def pos_offset_check(lat, lon, dn, de):
    # Earth’s radius, sphere
    R = 6378137

    #     # offsets in meters
    #     dn = 100
    #     de = 100

    # Coordinate offsets in radians
    dLat = dn / R
    dLon = de / (R * math.cos(math.pi * lat / 180))

    # OffsetPosition, decimal degrees
    new_lat = lat + dLat * 180 / math.pi
    new_lon = lon + dLon * 180 / math.pi

    rest_api_key = settings.KAKAO_REST_API_KEY
    kakao = KakaoLocalAPI(rest_api_key)
    input_coord = "WGS84"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
    output_coord = "TM"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

    result = kakao.geo_coord2regioncode(new_lon, new_lat, input_coord, output_coord)
    region_3depth_name = result['documents'][1]['region_3depth_name']
    #     print(result)
    #     print(new_lat, new_lon, region_3depth_name)

    return region_3depth_name

def out_measuring_range(mdata: MeasureCallData) -> str:
    """ 단말이 측정범위를 벗어났는지 확인
        - 측정하는 행정동을 벗어나서 측정이 되는 경우
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '측정범위 벗어남' or None
    """
    message = None
    # 측정유형이 행정동인 경우에만 단말이 측정범위를 벗어났는지 확인한다.
    if mdata.phone.morphology.morphology != '행정동': return None
    if not (mdata.longitude and mdata.latitude): return None

    # 카카오 지도API를 통해 해당 위도,경도에 대한 행정동 명칭을 가져온다.
    rest_api_key = settings.KAKAO_REST_API_KEY
    kakao = KakaoLocalAPI(rest_api_key)
    input_coord = "WGS84"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM
    output_coord = "TM"  # WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM

    result = kakao.geo_coord2regioncode(mdata.longitude, mdata.latitude, input_coord, output_coord)
    # [ 리턴값 형식 ]
    # print("out_measuring_range():", result)
    # {'meta': {'total_count': 2},
    # 'documents': [{'region_type': 'B',
    # 'code': '4824012400',
    # 'address_name': '경상남도 사천시 노룡동',
    # 'region_1depth_name': '경상남도',
    # 'region_2depth_name': '사천시',
    # 'region_3depth_name': '노룡동', <-- 주소지 동
    # 'region_4depth_name': '',
    # 'x': 296184.5342265043,
    # 'y': 165683.29710986698},
    # {'region_type': 'H',
    # 'code': '4824059500',
    # 'address_name': '경상남도 사천시 남양동',
    # 'region_1depth_name': '경상남도',
    # 'region_2depth_name': '사천시',
    # 'region_3depth_name': '남양동', <-- 행정구역
    # 'region_4depth_name': '',
    # 'x': 297008.1130364056,
    # 'y': 164008.47612447804}]}
    # 좌표(위도,경도)로 찾은 주소와 어떤 것을 비교할지? 고민필요
    # userInfo1가 위도,경도 좌표로 변환한 행정동을 포함하고 있는지 확인
    # 2022.02.28 - 단말기가 처음 측정을 시작할 때(현재 콜카운트가=1) 위치(위도,경도)가 정확하다고 가정하고 그때이 상세주소 값을
    #              측정 단말기 정보에 가져간다.
    #            - 측정 단말기의 상세주소와 해당 측정 데이터의 위도,경도를 통해 찾은 행정도 명칭과 비교한다.
    try:
        region_3depth_name = result['documents'][1]['region_3depth_name']
        if mdata.phone.addressDetail and mdata.phone.addressDetail.find(region_3depth_name) == -1:
            offsets = [(100, 100), (-100, 100), (100, -100), (-100, -100)]
            regions = set()
            for dn, de in offsets:
                regions.add(pos_offset_check(mdata.latitude, mdata.longitude, dn, de))
            if mdata.phone.addressDetail not in regions:
                # # 메시지를 작성한다.
                # message = f"{mdata.address}에서 측정단말이 측정범위를 벗어났습니다.\n" + \
                #         "(단말번호/측정 행정동(현재 행정동)/시간/콜카운트/DL/UL/RSRP/SINR)\n" + \
                #         f"{mdata.phone_no_sht} / {mdata.phone.addressDetail}({region_3depth_name}) / {mdata.time} / {mdata.currentCount} / " + \
                #         f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
                message = f'측정범위 벗어남({regions.pop()})'

    except Exception as e:
        print("out_measuring_range():", str(e))
        raise Exception("out_measuring_range(): %s" % e)

    return message


# ----------------------------------------------------------------------------------------------------------------------
# 측정단말이 한곳에 머무는지 확인
# 2022.02.22 - 처리대상 데이터를 속도측정 데이터('speed')에 한정하여 처리한다.
#            - 행정동 측정일때만 체크한다. (예: 테마의 경우 위도,경도가 동일한 경우가 다수 발생함)
#            - 행정동: 도로주행 측정, 테마: 놀이공원 등 걸어서 측정, 인빌딩: 건물내 걸어서 측정
# 2022.02.27 - 기존 이동거리 5미터 이상, 연속해서 3회 초과 -> 이동거리 10미터 이상, 연속해서 5회 초과 발생으로 기준 변경
# 2022.03.01 - 이동거리를 강제로 500미터 이상으로 해서 한곳에 머무는지 판단하는 소스코드 검증
#            - 행정동 측정에서 기본 이동거리는 200~300미터 정도임
# 2022.06.08 - 행정동 여부를 측정단말에서 단말그룹의 모폴로지로 변경함
#
# ----------------------------------------------------------------------------------------------------------------------
def call_staying_check(mdata: MeasureCallData) -> str:
    """ 측정단말이 한곳에 머무는지 확인
        - 타사 측정단말에 문제가 발생하여 조치를 하거나 차량에 문제가 있거나 등 한곳에 오랫동안 멈는 경우가 있는데,
          이렇게 한곳에 멈춰 있는 경우 보고 대상임
        - 이동거리가 10미터 이내 연속해서 5회 이상 발생하면 한 곳에 머무는 것으로 판단
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '측정단말 한곳에 머뭄' or None
    """
    # if mdata.phone.morphology.morphology is not "행정동":
    if mdata.phone.phoneGroup.morphology.morphology is not "행정동":
        return None
    
    message = None
    # 측정유형이 행정동인 경우에만 측정단말이 한곳에 머무는지 확인한다.
    if mdata.phone.morphology.morphology == '행정동':
        # mdata_list = mdata.phone.measurecalldata_set.all()
        mdata_list = mdata.phone.measurecalldata_set.filter(testNetworkType='speed').order_by("-currentCount")
        count = len(mdata_list)
        callstay = True
        # 이동거리를 확인하기 위해서는 측정값이 6건 이상 있어야 한다.
        if count >= 6:
            # for idx, md in enumerate(mdata_list[count-1::-1]):
            result = ''
            before_loc = None
            for idx, md in enumerate(mdata_list):
                if idx == 0:
                    before_loc = (md.latitude, md.longitude)
                else:
                    # 두 측정저점간의 이동거리를 계산한다.
                    current_loc = (md.latitude, md.longitude)
                    distance = haversine(before_loc, current_loc) * 1000  # 미터(meters)
                    # print("call_staying_check():", idx, str(md), distance, before_loc, current_loc)
                    # 측정 단말기 이동거리가 10M 이상이 되면 한곳에 머무르지 않고, 이동하는 것으로 판단한다.
                    result += str(before_loc) + '/' + str(current_loc) + '/' + str(distance) + ',\n'
                    # if distance > 500 : <= 2022.03.01 테스트 시 사용
                    if distance > 10:
                        callstay = False
                        break
                    before_loc = current_loc
                if idx >= 6: break
        else:
            callstay = False

        if callstay:
            # # 메시지 내용을 작성한다.
            # message = f"{mdata.address}에서 측정단말이 한곳에 머물러 있습니다.\n" + \
            #            "(단말번호/시간/콜카운트/DL/UL/RSRP/SINR)\n" + \
            #             f"{mdata.phone_no_sht} / {mdata.time} / {mdata.currentCount} / " + \
            #             f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
            message = '측정단말 한곳에 머뭄'

    return message


# ----------------------------------------------------------------------------------------------------------------------
# 중복측정이 발생했는지 확인
# 2022.03.16 - 단말그룹으로 묶여 있는 2개의 단말이 동일한 유형의 측정을 수행하고 있은 때 이벤트 발생(DL/DL, UL/UL)
# ----------------------------------------------------------------------------------------------------------------------
def duplicated_measuring(mdata: MeasureCallData) -> str:
    """ 두개의 단말이 중복측정하고 있는지 확인
        - 단말그룹으로 묶여 있는 2개의 단말이 동일한 유형의 측정을 수행하고 있은 때 이벤트 발생(DL/DL, UL/UL)
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: '중복측정' or None
    """
    message = None
    duplicated = False
    # 두개의 단말이 서로 측정유형을 바꾸는 동안 지연시간을 갖는다(2개 콜)
    # 즉, DL -> UL, UL -> DL
    if mdata.currentCount >= 3:

        # 측정단말 교체에 따른 중복 이벤트발생을 제외하기 위해서 현재시점 5분이전부터 발생한 데이터가 있는지 확인한다.
        now = datetime.now()
        from_dt = int((now - timedelta(minutes=5)).strftime("%Y%m%d%H%M%S") + '000')

        # 다운로드를 중복측정하고 있는지 확인한다.
        qs = Phone.objects.filter(phoneGroup=mdata.phone.phoneGroup, meastype='DL', last_updated__gte=from_dt)
        if qs.exists() and qs.count() > 1:
            duplicated = True

        # 업로드를 중복측정하고 있는지 확인한다.
        qs = Phone.objects.filter(phoneGroup=mdata.phone.phoneGroup, meastype='UL', last_updated__gte=from_dt)
        if qs.exists() and qs.count() > 1:
            duplicated = True

        if duplicated:
            # # 메시지 내용을 작성한다.
            # message = f"{mdata.address}에서 중복측정({mdata.phone.meastype})을 하고 있습니다.\n" + \
            #             "(단말번호/시간/콜카운트/DL/UL/RSRP/SINR)\n" + \
            #             f"{mdata.phone_no_sht} / {mdata.time} / {mdata.currentCount} / " + \
            #             f"{mdata.dl} / {mdata.ul} / {mdata.rsrp} / {mdata.p_sinr}"
            message = '중복측정'
    return message


# ----------------------------------------------------------------------------------------------------------------------
# 이벤트 메시지 작성 함수
# 2022.02.27 - 메시지 포맷 정의 (이벤트 발생 관련 정보 표시)
#            - 메시지 작성 코드를 각각 이벤트 확인하는 함수로 이동함(메시지 내에 관련정보 포함하기 위해)
# 2022.03.28 - 단말그룹의 이벤트발생 건수를 업데이트 하는 코드를 추가함
# ----------------------------------------------------------------------------------------------------------------------
def make_event_message(mdata: MeasureCallData, events_list: list):
    """이벤트 메시지 작성한다.
        - 파라미터
          . mdata: 측정 데이터(콜단위)
          . event_list: 발생된 이벤트 문자열 리스트(예: ['LTE전환', '측정범위 벗어남'])
        - 반환값: '중복측정' or None
    """
    # 환경변수에서 채널ID를 가져온다.
    # channelId = settings.CHANNEL_ID
    channelId = mdata.phone.center.channelId

    # 해당 측정위치에 대한 지도맵을 작성하고, 메시지 하단에 [지도보기] 링크를 붙인다.
    # (단말번호/측정 행정동(현재 행정동)/시간/콜카운트/DL/UL/RSRP/SINR)
    # 2022.03.17 - 보안이슈로 지도맵 제공기능 취소함
    # filename = make_map_locations(mdata)

    # 메시지를 작성한다.
    message = f"[{mdata.userInfo1} 측정 단말]\n" + \
            f"{mdata.address}에서 이벤트가 발생했습니다. ({mdata.phone.networkId})\n" + \
            f"* 발생 이벤트({len(events_list)}건): {', '.join(events_list)}\n" + \
            f"(단말/시간/{mdata.phone.meastype}속도/RSRP/SINR)\n" + \
            f"{mdata.phone_no_sht} / {mdata.time} / {mdata.bw} / {mdata.rsrp} / {mdata.p_sinr}"

    # 2022.03.17 - 보안이슈로 지도맵 제공기능 취소함
    # message += f"\n<a href='http://127.0.0.1:8000/monitor/maps/{filename}'>지도보기</a>"

    # 전송 메시지를 생성한다.
    if message:
        # 전송 메시지를 생성한다. 
        Message.objects.create(
            phoneGroup=mdata.phone.phoneGroup, # 단말그룹
            phone=mdata.phone,  # 측정단말
            center=mdata.phone.phoneGroup.center,
            status=mdata.phone.status,  # 측정단말 상태
            measdate=str(mdata.meastime)[0:8],  # 측정일자
            sendType='TELE',  # 메시지 전송유형(TELE: 텔레그램, XMCS: 크로샷)
            userInfo1=mdata.userInfo1,  # 측정자 입력값1
            currentCount=mdata.currentCount,  # 현재 콜카운트
            phone_no=mdata.phone_no,  # 측정단말 전화번호
            downloadBandwidth=mdata.downloadBandwidth,  # DL 속도
            uploadBandwidth=mdata.uploadBandwidth,  # UL 속도
            messageType='EVENT',  # 메시지 유형(SMS: 단문메시지, EVENT: 이벤트발생 메시지)
            message=message,  # 메시지 내용
            channelId=channelId,  # 채널ID
        )

        # 단말그룹의 이벤트 발생건수를 하나 증가시킨다.
        # 2022.05.01 - 이벤트 발생건수에 "전송실패"만 반영하기로 함  -->  2022.06.03 이벤트 발생건수는 send_failure_check 에서 처리하도록 이동
        # if 'DL전송실패' in events_list:
        #     mdata.phone.phoneGroup.send_failure_dl_count += 1
        #     mdata.phone.phoneGroup.event_count += 1  # 전체 이벤트 건수(전송실패)
        # elif 'UL전송실패' in events_list:
        #     mdata.phone.phoneGroup.send_failure_ul_count += 1
        #     mdata.phone.phoneGroup.event_count += 1  # 전체 이벤트 건수(전송실패)
        # mdata.phone.phoneGroup.save()

