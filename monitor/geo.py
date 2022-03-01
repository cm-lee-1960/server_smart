###################################################################################################
# 좌표(위도,경도) 및 주소 변환 모듈
# - 카카오 개발문서 : https://developers.kakao.com/docs/latest/ko/local/dev-guide
#################################################################################################### 

import json
import requests
import folium
class KakaoLocalAPI:
    '''Kakao Local API 컨트롤러'''
    def __init__(self, rest_api_key):
        '''Rest API키 초기화 및 기능 별 URL 설정'''
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

    # -------------------------------------------------------------------------------------------------
    # 01 주소 검색
    #--------------------------------------------------------------------------------------------------
    def search_address(self, query, analyze_type=None, page=None, size=None):
        '''01 주소 검색'''
        params = {"query": f"{query}"}

        if analyze_type != None:
            params["analyze_type"] = f"{analyze_type}"

        if page != None:
            params['page'] = f"{page}"

        if size != None:
            params['size'] = f"{size}"

        res = requests.get(self.URL_01, headers=self.headers, params=params)
        document = json.loads(res.text)

    # -------------------------------------------------------------------------------------------------
    # 02 좌표-행정구역정보 변환
    #--------------------------------------------------------------------------------------------------
    def geo_coord2regioncode(self, x, y, input_coord=None, output_coord=None):
        '''02 좌표-행정구역정보 변환'''
        params = {"x": f"{x}",
                  "y": f"{y}"}
        
        if input_coord != None:
            params['input_coord'] = f"{input_coord}"
        
        if output_coord != None:
            params['output_coord'] = f"{output_coord}"
            
        res = requests.get(self.URL_02, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document
 
    # -------------------------------------------------------------------------------------------------
    # 03 좌표-주소 변환
    #--------------------------------------------------------------------------------------------------    
    def geo_coord2address(self, x, y, input_coord=None):
        '''03 좌표-주소 변환'''
        params = {"x": f"{x}",
                  "y": f"{y}"}
        
        if input_coord != None:
            params['input_coord'] = f"{input_coord}"
            
        res = requests.get(self.URL_03, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document

    # -------------------------------------------------------------------------------------------------
    # 04 좌표계 변환
    #--------------------------------------------------------------------------------------------------  
    def geo_transcoord(self, x, y, output_coord, input_coord=None):
        '''04 좌표계 변환'''
        params = {"x": f"{x}",
                  "y": f"{y}",
                  "output_coord": f"{output_coord}"}
        
        if input_coord != None:
            params['input_coord'] = f"{input_coord}"
        
        res = requests.get(self.URL_04, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document

    # -------------------------------------------------------------------------------------------------
    # 05 키워드 검색
    #--------------------------------------------------------------------------------------------------     
    def search_keyword(self,query,category_group_code=None,x=None,y=None,radius=None,rect=None,page=None,size=None,sort=None):
        '''05 키워드 검색'''
        params = {"query": f"{query}"}
        
        if category_group_code != None:
            params['category_group_code'] = f"{category_group_code}"
        if x != None:
            params['x'] = f"{x}"
        if y != None:
            params['y'] = f"{y}"
        if radius != None:
            params['radius'] = f"{radius}"
        if rect != None:
            params['rect'] = f"{rect}"
        if page != None:
            params['page'] = f"{page}"
        if size != None:
            params['size'] = f"{params}"
        if sort != None:
            params['sort'] = f"{sort}"
        
        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document

    # -------------------------------------------------------------------------------------------------
    # 06 카테고리 검색
    #--------------------------------------------------------------------------------------------------       
    def search_category(self, category_group_code, x, y, radius=None, rect=None, page=None, size=None, sort=None):
        '''06 카테고리 검색'''
        params = {'category_group_code': f"{category_group_code}",
                  'x': f"{x}",
                  'y': f"{y}"}
        
        if radius != None:
            params['radius'] = f"{radius}"
        if rect != None:
            params['rect'] = f"{rect}"
        if page != None:
            params['page'] = f"{page}"
        if size != None:
            params['size'] = f"{size}"
        if sort != None:
            params['sort'] = f"{sort}"
            
        res = requests.get(self.URL_06, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document


#######################################################################################################
# 측정 위치에 대한 지도맵 그리기
#######################################################################################################
def make_map_locations(mdata):
    # if locations and len(locations) < 1: return None
    map = folium.Map(location=[mdata.phone.latitude, mdata.phone.longitude], zoom_start=15)

    # 첫번째 측정위치를 지도맵에 표시한다.
    folium.Marker(
        location=[mdata.phone.latitude, mdata.phone.longitude],
        icon=folium.Icon(color="red", icon="star"),
        icon_size=(10,10),
    ).add_to(map)

    # 측정 위치를 지도맵에 표시한다.
    for m in mdata.phone.measurecalldata_set.all():
        folium.Circle(
            location=[m.latitude, m.longitude],
            radius=14.5, # CircleMarker 크기 지정
            color='#3186cc', # CirclaMarker 테두리 색상
            fill_color='#3186cc', # CircleMarker 내부 색상 '#000000' 
            fill_opacity=1.,
            weight=1
        ).add_to(map)

    filename = f'0_{mdata.phone.measdate}_{mdata.phone_no}.html'
    map.save(filename)