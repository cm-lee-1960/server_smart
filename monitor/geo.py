import json
import requests
import folium
from folium import plugins
import pandas as pd
import os
from haversine import haversine # 이동거리
from django.conf import settings
from management.models import AddressRegion
import logging


db_logger = logging.getLogger('db')

########################################################################################################################
# 좌표(위도,경도) 및 주소 변환 모듈
# - 카카오 개발문서 : https://developers.kakao.com/docs/latest/ko/local/dev-guide
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.22 - 코딩 및 주석 작성 룰에 벗어나는 내용 수정
# 2022.05.02 - 지도맵 작성시 모폴로지가 행정동일 때만 경계구역을 그린다.
# 2022.05.30 - 위도와 경도에 값이 없는 경우 지도상에 표기하지 않는다(SKIP).
#
########################################################################################################################
class KakaoLocalAPI:
    """Kakao Local API 컨트롤러"""
    def __init__(self, rest_api_key):
        """Rest API키 초기화 및 기능 별 URL 설정"""
        # REST API 키 설정
        self.rest_api_key = rest_api_key
        self.headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}

        # 서비스 별 URL 설정
        self.URL_01 = "https://dapi.kakao.com/v2/local/search/address.json" # 01 주소 검색
        self.URL_02 = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json" # 02 좌표-행정구역정보 변환
        self.URL_03 = "https://dapi.kakao.com/v2/local/geo/coord2address.json" # 03 좌표-주소 변환
        self.URL_04 = "https://dapi.kakao.com/v2/local/geo/transcoord.json" # 04 좌표계 변환
        self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json" # 05 키워드 검색
        self.URL_06 = "https://dapi.kakao.com/v2/local/search/category.json" # 06 카테고리 검색

    # ------------------------------------------------------------------------------------------------------------------
    # 01 주소 검색
    # ------------------------------------------------------------------------------------------------------------------
    def search_address(self, query, analyze_type=None, page=None, size=None):
        """01 주소 검색"""
        params = {"query": f"{query}"}

        if analyze_type is not None:
            params["analyze_type"] = f"{analyze_type}"

        if page is not None:
            params['page'] = f"{page}"

        if size is not None:
            params['size'] = f"{size}"

        res = requests.get(self.URL_01, headers=self.headers, params=params)
        document = json.loads(res.text)

    # ------------------------------------------------------------------------------------------------------------------
    # 02 좌표-행정구역정보 변환
    # ------------------------------------------------------------------------------------------------------------------
    def geo_coord2regioncode(self, x, y, input_coord=None, output_coord=None):
        """02 좌표-행정구역정보 변환"""
        params = {"x": f"{x}",
                  "y": f"{y}"}
        
        if input_coord is not None:
            params['input_coord'] = f"{input_coord}"
        
        if output_coord is not None:
            params['output_coord'] = f"{output_coord}"
            
        res = requests.get(self.URL_02, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document
 
    # ------------------------------------------------------------------------------------------------------------------
    # 03 좌표-주소 변환
    # ------------------------------------------------------------------------------------------------------------------
    def geo_coord2address(self, x, y, input_coord=None):
        """03 좌표-주소 변환"""
        params = {"x": f"{x}",
                  "y": f"{y}"}
        
        if input_coord is not None:
            params['input_coord'] = f"{input_coord}"
            
        res = requests.get(self.URL_03, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document

    # ------------------------------------------------------------------------------------------------------------------
    # 04 좌표계 변환
    # ------------------------------------------------------------------------------------------------------------------
    def geo_transcoord(self, x, y, output_coord, input_coord=None):
        """04 좌표계 변환"""
        params = {"x": f"{x}",
                  "y": f"{y}",
                  "output_coord": f"{output_coord}"}
        
        if input_coord is not None:
            params['input_coord'] = f"{input_coord}"
        
        res = requests.get(self.URL_04, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document

    # -------------------------------------------------------------------------------------------------
    # 05 키워드 검색
    #--------------------------------------------------------------------------------------------------     
    def search_keyword(self,query,category_group_code=None,x=None,y=None,radius=None,rect=None,page=None,size=None,sort=None):
        """05 키워드 검색"""
        params = {"query": f"{query}"}
        
        if category_group_code is not None:
            params['category_group_code'] = f"{category_group_code}"
        if x is not None:
            params['x'] = f"{x}"
        if y is not None:
            params['y'] = f"{y}"
        if radius is not None:
            params['radius'] = f"{radius}"
        if rect is not None:
            params['rect'] = f"{rect}"
        if page is not None:
            params['page'] = f"{page}"
        if size is not None:
            params['size'] = f"{params}"
        if sort is not None:
            params['sort'] = f"{sort}"
        
        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document

    # ------------------------------------------------------------------------------------------------------------------
    # 06 카테고리 검색
    # ------------------------------------------------------------------------------------------------------------------
    def search_category(self, category_group_code, x, y, radius=None, rect=None, page=None, size=None, sort=None):
        """06 카테고리 검색"""
        params = {'category_group_code': f"{category_group_code}",
                  'x': f"{x}",
                  'y': f"{y}"}
        
        if radius is not None:
            params['radius'] = f"{radius}"
        if rect is not None:
            params['rect'] = f"{rect}"
        if page is not None:
            params['page'] = f"{page}"
        if size is not None:
            params['size'] = f"{size}"
        if sort is not None:
            params['sort'] = f"{sort}"
            
        res = requests.get(self.URL_06, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document


########################################################################################################################
# 좌표(위도,경도) 및 주소 변환 모듈2 - olleh API
# - Test Page : https://gis.kt.com/doc/search/testUI_kr.html
# - API KEY 절대 외부 유출 금지!
########################################################################################################################
def ollehAPI_reverseGEO(latitude, longitude):
    '''olleh API를 통한 좌표->주소 전환
        .파라미터(input): 위도/경도
        .반환값 : dict '''
    try:
        api_key = settings.OLLEH_API_KEY
        headers = {'Content-Type': 'application/json; charset=utf-8',
                    "Authorization": api_key,
                    "Accept-Language": "ko-KR",
                    }
        url = f"https://gis.kt.com/search/v1.0/utilities/geocode?point.lat={latitude}&point.lng={longitude}&includeGeometry=false&expectedParcelLevel=LEAFPARCEL&expectedRoadLevel=LEAFSTREET&exactParcelMatch=false&exactRoadMatch=false"

        response = requests.get(url, headers=headers)
        data = response.json()

        if 'residentialAddress' in data.keys() and len(data['residentialAddress']) != 0 and \
            'parcelAddress' in data['residentialAddress'][0].keys() and len(data['residentialAddress'][0]['parcelAddress']) != 0:
            dt = data['residentialAddress'][0]['parcelAddress'][0]
            if 'siDo' in dt.keys(): siDo = dt['siDo']
            else: siDo = None
            if 'siGunGu' in dt.keys(): siGunGu = dt['siGunGu']
            else: siGunGu = None
            if 'eupMyeonDong' in dt.keys(): eupMyeonDong = dt['eupMyeonDong']
            else: eupMyeonDong = None
            # fullAddress = data['residentialAddress'][0]['parcelAddress'][0]['fullAddress']
            # ri = data['residentialAddress'][0]['parcelAddress'][0]['ri']
        
            result = {'result':'ok', 'siDo':siDo, 'siGunGu':siGunGu, 'eupMyeonDong':eupMyeonDong, 'data':data}
            return result
        else:
            db_logger.error("ollehAPI_reverseGEO: 주소변환실패" , data)
            return {'result':'fail', 'data':data}
    except Exception as e:
        db_logger.error("ollehAPI_reverseGEO:", str(e))
        return {'result':'fail'}


########################################################################################################################
# 측정 위치에 대한 지도맵 그리기
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.02 - 파일명에 통신사업자 코드를 넣음(파일명으로 어느 통신사 측정단말인지 알기 위해)
# 2022.03.07 - 측정위치 팝업 항목 표시 순서 변경(PCI, Cell ID, DL, UL, RSRP, SINR)
#            - 팝업 항목 및 값 가운데 정렬, 측정 데이터가 10개 이상일 때만 지도 자동확대 적용함
#              측정 데이터가 너무 적을 때 자동확대 하면 지도가 너무 크게 확대되는 현상이 있음
# 2022.03.12 - 생성된 지도맵 저장 파일명을 기존 측정일자(measdate)에서 측정일시(meastime)로 변경함
#              좁은 지역을 측정하는 경우 측정위치를 나태내는 원(Circle)이 너무 크게 확대되는 현상이 있어 조치함
#            - 지도상에 행정동 경계구역을 표시함 (경계구역을 모든 지도맵에 표시했는데, 차후 행정동만 표기할 것인지 검토 필요)
#
########################################################################################################################
# RSRP 값에 따라 색상코드를 결정한다. 
def rsrp2color(x):
    """ RSRP 값으로 색상코드를 반환한다.
        - 파라미터: RSRP(숫자)
        - 반환값: 색상값(문자열)
    """
    if x > -65:
        color = 'red'
    elif -75 <= x < -65:
        color = 'orange'
    elif -85 <= x < -75:
        color = 'yellow'
    elif -95 <= x < -85:
        color = 'green'
    elif -105 <= x < -95:
        color = 'blue'
    else:
        color = 'black'
    return color

# def make_map_locations(mdata):
#     """ 측정위치로 지도를 작성하는 함수
#         - 파라미터
#           . mdata: 측정 데이터(콜단위) (MeasureCallData)
#         - 반환값: 없음
#     """
#     # if locations and len(locations) < 1: return None
#     map = folium.Map(location=[mdata.phone.latitude, mdata.phone.longitude], zoom_start=15)
#
#     # 첫번째 측정위치를 지도맵에 표시한다.
#     folium.Marker(
#         location=[mdata.phone.latitude, mdata.phone.longitude],
#         icon=folium.Icon(color="red", icon="star"),
#         icon_size=(10,10),
#     ).add_to(map)
#
#     # 측정 위치를 지도맵에 표시한다.
#     locations = []
#     points = folium.FeatureGroup(name="All Points")
#     qs = mdata.phone.measurecalldata_set.filter(testNetworkType='speed').order_by("meastime")
#     if qs.exists():
#         for m in qs:
#             # 네트워크 유형(5G, LTE, 3G)에 따라서 무선품질 정보를 가져온다.
#             if m.networkId == '5G':
#                 pci, RSRP, SINR = m.NR_PCI, m.NR_RSRP, m.NR_SINR
#             else:
#                 pci, RSRP, SINR= m.p_pci, m.p_rsrp, m.p_SINR
#             # RSRP 값에 따라서 색상을 계산한다.
#             if m.latitude == mdata.latitude and m.longitude == mdata.longitude:
#                 radius = 40
#             else:
#                 radius = 25
#             df = pd.DataFrame([{'PCI': pci, 'Cell ID': m.cellId, 'DL': m.downloadBandwidth, 'UL': m.uploadBandwidth, \
#                                 'RSRP': RSRP, 'SINR': SINR },])
#             html = df.to_html(index=False,
#                             classes='table table-striped table-hover table-condensed table-responsive text-center')
#             html = html.replace('<th>', '<td align="center">') # 항목명 가운데 정렬
#             html = html.replace('<td>', '<td align="center">') # 항목값 가운데 정렬
#             popup = folium.Popup(html, min_width=100, max_width=300)
#             folium.Circle(
#                 location=[m.latitude, m.longitude],
#                 popup=popup,
#                 radius=radius, # 크기 지정
#                 color='black', # 테두리 색상
#                 fill_color=rsrp2color(RSRP) if RSRP else 'black', # 내부 색상 '#000000'
#                 fill_opacity=1.,
#                 weight=1
#             ).add_to(points)
#             locations.append([m.latitude, m.longitude])
#
#         # 지도맵에 이동경로를 표시한다.
#         folium.PolyLine(locations=locations).add_to(map)
#
#         # 지도맵에 측정지점들을 표시한다.
#         # 이동경로와 겹쳐서 먼저 이동경로를 그리고 난 후 측점지점들을 표시한다.
#         points.add_to(map)
#
#         # 지도 자동줌 기능(모든 POT과 시설이 지도상에 보여질 수 있도록 자동확대)
#         # 2022.03.07 - 측정 데이터가 10개 이상일 때만 지도를 자동확대 하도록 한다.
#         #              측정 데이터가 몇개 안될때 지도를 자동확대 하면 측정위치가 너무 크게 확대되는 현상이 있음
#         if len(locations) > 1:
#             start_loc = tuple(locations[0])
#             current_loc = (mdata.latitude, mdata.longitude)
#             distance = haversine(start_loc, current_loc)  # 킬로(km)
#             # if len(locations) >= 10:
#             if distance > 3:
#                 sw = pd.DataFrame(locations).min().values.tolist()
#                 ne = pd.DataFrame(locations).max().values.tolist()
#                 map.fit_bounds([sw, ne])
#
#     # # 지도상에 행정동 경계구역을 표시한다.
#     # # 동일한 필드명으로 조건을 두번 쓸수 없고, 필터를 두번 걸어야 함
#     # qs = AddressRegion.objects.filter( addressDetail__contains=mdata.phone.addressDetail) \
#     #                         .filter(addressDetail__contains=mdata.phone.guGun)
#     # if qs.exists():
#     #     json_data = qs[0].json_data
#     #     geo = {
#     #         "type": "FeatureCollection",
#     #         "name": "HangJeongDong_ver20220309",
#     #         "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
#     #         "bbox": [ 124.609681415304, 33.1118678527544, 131.871294250487, 38.616952080675 ],
#     #         "features": [ json_data
#     #     ]}
#     #     folium.GeoJson(geo, name='seoul_municipalities').add_to(map)
#
#     # 작성된 지도맵을 저장하고, 파일명을 반환한다.
#     filename = f'{mdata.meastime}-{mdata.ispId}-{mdata.phone_no}.html'
#     map.save("monitor/templates/maps/" + filename)
#
#     return filename

def make_map_locations(phoneGroup):
    """ 측정위치로 지도를 작성하는 함수
        - 파라미터
          . mdata: 측정 데이터(콜단위) (MeasureCallData)
        - 반환값: 없음
    """

    map = folium.Map(location=[phoneGroup.phone_set.first().latitude, phoneGroup.phone_set.first().longitude],
                     zoom_start=15)

    dl_points = folium.FeatureGroup(name="DL Points")
    ul_points = folium.FeatureGroup(name="UL Points")
    polyline = folium.FeatureGroup(name="PolyLine", show=False)

    locations = []
    max_distance = 0
    for phone in phoneGroup.phone_set.all():

        # 첫번째 측정위치를 지도맵에 표시한다.
        folium.Marker(
            location=[phone.latitude, phone.longitude],
            icon=folium.Icon(color="red", icon="star"),
            icon_size=(10, 10),
        ).add_to(map)

        start_loc = (phone.latitude, phone.longitude)
        for mdata in phone.measurecalldata_set.all():
            # 위도와 경도에 값이 없는 경우 지도상에 표기하지 않는다(SKIP).
            if mdata.latitude is None or mdata.longitude is None:
                continue
            # 네트워크 유형(5G, LTE, 3G)에 따라서 무선품질 정보를 가져온다.
            if mdata.networkId == '5G':
                pci, RSRP, SINR = mdata.NR_PCI, mdata.NR_RSRP, mdata.NR_SINR
            else:
                pci, RSRP, SINR = mdata.p_pci, mdata.p_rsrp, mdata.p_SINR

            df = pd.DataFrame(
                [{'PCI': pci, 'Cell ID': mdata.cellId, 'DL': mdata.downloadBandwidth, 'UL': mdata.uploadBandwidth, \
                  'RSRP': RSRP, 'SINR': SINR}, ])
            html = df.to_html(index=False,
                              classes='table table-striped table-hover table-condensed table-responsive text-center')
            html = html.replace('<th>', '<td align="center">')  # 항목명 가운데 정렬
            html = html.replace('<td>', '<td align="center">')  # 항목값 가운데 정렬
            popup = folium.Popup(html, min_width=100, max_width=300)
            radius = 25
            if mdata.downloadBandwidth is not None and mdata.downloadBandwidth > 0:
                folium.Circle(
                    location=[mdata.latitude, mdata.longitude],
                    popup=popup,
                    radius=radius,  # 크기 지정
                    color='black',  # 테두리 색상
                    fill_color=rsrp2color(RSRP) if RSRP else 'black',  # 내부 색상 '#000000'
                    fill_opacity=1.,
                    weight=1
                ).add_to(dl_points)
            elif mdata.uploadBandwidth is not None and mdata.uploadBandwidth > 0:
                folium.Circle(
                    location=[mdata.latitude, mdata.longitude],
                    popup=popup,
                    radius=radius,  # 크기 지정
                    color='black',  # 테두리 색상
                    fill_color=rsrp2color(RSRP) if RSRP else 'black',  # 내부 색상 '#000000'
                    fill_opacity=1.,
                    weight=1
                ).add_to(ul_points)

            # 측정 시작위치와 현재위치의 거리를 계산한다.
            current_loc = (mdata.latitude, mdata.longitude)
            distance = haversine(start_loc, current_loc)  # 킬로(km)
            if distance > max_distance :
                max_distance = distance

            locations.append([mdata.latitude, mdata.longitude])

    # 지도상에 행정동 경계구역을 표시한다.
    # 동일한 필드명으로 조건을 두번 쓸수 없고, 필터를 두번 걸어야 함
    # 2022.05.02 모폴로지가 행정동일때만 경계구역을 표시한다.
    if phoneGroup.morphology.morphology == "행정동":
        qs = AddressRegion.objects.filter(addressDetail__contains=mdata.phone.addressDetail) \
            .filter(addressDetail__contains=mdata.phone.guGun)
        if qs.exists():
            json_data = qs[0].json_data
            #         print(json_data)
            #         geo = {
            #             "type": "FeatureCollection",
            #             "name": "HangJeongDong_ver20220309",
            #             "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
            #             "bbox": [ 124.609681415304, 33.1118678527544, 131.871294250487, 38.616952080675 ],
            #             "features": [ json_data
            #         ]}
            #         folium.GeoJson(geo, name='seoul_municipalities').add_to(map)
            folium.GeoJson(data=json_data, name='AddressRegion').add_to(map)

    # 지도맵에 이동경로를 표시한다.
    folium.PolyLine(locations=locations).add_to(polyline)

    # 지도맵에 측정지점들을 표시한다.
    dl_points.add_to(map)
    ul_points.add_to(map)

    polyline.add_to(map)

    # 지도 자동줌 기능(모든 POT과 시설이 지도상에 보여질 수 있도록 자동확대)
    if max_distance > 3:
        sw = pd.DataFrame(locations).min().values.tolist()
        ne = pd.DataFrame(locations).max().values.tolist()
        map.fit_bounds([sw, ne])

    # 화면 왼쪽 상단에 컨트롤들을 표시하기
    plugins.Fullscreen(
        position='topright',
        title='전체화면 보기',
        title_cancel='전체화면 종료',
        force_separate_button=True
    ).add_to(map)
    #     plugins.ScrollZoomToggler().add_to(map)
    plugins.MeasureControl().add_to(map)
    folium.LayerControl(collapsed=False).add_to(map)

    # 작성된 지도맵을 저장하고, 파일명을 반환한다.
    dirName = "monitor/templates/maps/"
    filename = dirName + f'{phoneGroup.measdate}_{phoneGroup.phone_list}.html'
    # 해당 디렉토리가 있는지 확인해서 없으면 생성한다.
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    map.save(filename)

    return filename