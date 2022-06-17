from monitor.models import Phone
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from logs.models import StatusLog
from management.models import MessageConfig

########################################################################################################################
# 백그라운드 스케쥴러 작업을 관리하는 모듈
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.27 - 백그라운드 스케쥴러 작업 모듈 작성 및 테스트
#            - 향후 측정마감이나 텔레그램 커맨드 핸들러 등록 등 백그라운드 작업 등록에 사용할 예정임
# 2022.06.13 - 매주 월요일 감시가 중지되어 있으면 자동으로 사작한다.
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 측정이 종료되었는지 확인한다.
# ----------------------------------------------------------------------------------------------------------------------
def measuring_end_check():
    """단말이 측정이 종료되었는지 확인한다.
        - (행정동) 콜 카운트가 54콜 이상이고, 최종 위치보고시간 이후 2~3분이 지났을 경우
        - (인빌딩) 요구사항 세부내역 확인
    """
    pass
    # qs = Phone.objects.all()
    # for phone in qs:
    #     print(phone)


# @db_auto_reconnect
# def telegram_command_handler():
#     command_handler()

# ----------------------------------------------------------------------------------------------------------------------
# 2주전 로그내역을 삭제한다.
# ----------------------------------------------------------------------------------------------------------------------
def delete_logs_before_week():
    """2주전 로그내역을 삭제하는 함수"""
    base_date = datetime.today() - timedelta(days=7)
    qs = StatusLog.objects.filter(create_datetime__lt=base_date)
    if qs.exists():
        qs.delete()

# ----------------------------------------------------------------------------------------------------------------------
# 매주 월요일 감시가 중지되어 있으면 자동으로 사작한다.
# - 공휴일이 아닌 경우에만 감시를 시작함
# ----------------------------------------------------------------------------------------------------------------------
def print_whichday(year, month, day):
    # 0	Monday
    # 1	Tuesday
    # 2	Wednesday
    # 3	Thursday
    # 4	Friday
    # 5	Saturday
    # 6	Sunday
    r = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    aday = datetime.date(year, month, day)
    bday = aday.weekday()
    return r[bday]


def get_request_query(url, operation, params, serviceKey):
    import urllib.parse as urlparse
    params = urlparse.urlencode(params)
    request_query = url + '/' + operation + '?' + params + '&' + 'serviceKey' + '=' + serviceKey
    return request_query


def holiday_check(year, month, tday):
    # 해당 월에 대해 문자열로 변환한다(예: 03)
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    #  해당 일자에 대해 문자열로 변환한다(예: 02)
    if tday < 10:
        tday = '0' + str(tday)
    else:
        tday = str(tday)

    # 일반 인증키(Encoding)
    mykey = "6uBBLx%2Bw7eAFCIh9t7jqX2uOFOyrZFXmVz4dMvExFt7qHhM5y3aWlzVlJBOk7VQ%2FZ2UYp%2Bw4yWDW4BDcw%2FChcA%3D%3D"
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService"
    # 공휴일 정보 조회
    operation = 'getRestDeInfo'
    params = {'solYear': year, 'solMonth': month}

    request_query = get_request_query(url, operation, params, mykey)
    get_data = requests.get(request_query)
    #     print(get_data.content)

    holidays = []
    if True is get_data.ok:
        soup = BeautifulSoup(get_data.content, 'html.parser')

        item = soup.findAll('item')
        for i in item:
            day = int(i.locdate.string[-2:])
            weekname = print_whichday(int(year), int(month), day)
            #             print(i.datename.string, i.isholiday.string, i.locdate.string, weekname)
            holidays.append(i.locdate.string)

    # 해당 일자에 대해서 공휴일인지 확인한다.
    date_s = str(year) + month + tday
    if date_s in holidays:
        result = True
    else:
        result = False
    return result

def start_monitoring():
    dt = datetime.today()
    # if  print_whichday(dt.year, dt.month, dt.day) == "월요일" and not holiday_check(dt.year, dt.month, dt.day):
    if not holiday_check(dt.year, dt.month, dt.day):
        msgcfg = MessageConfig.objects.all()[0]
        if msgcfg.ALL is False:
            msgcfg.ALL = True
            msgcfg.save()