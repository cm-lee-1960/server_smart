#################################################################################################################
measdate = '20211101'  # <== ★★★★ 시뮬레이터를 실행하고자 하는 측정일자
#################################################################################################################

import mysql.connector
import requests, json
import time
import os
from django.db.models import Q

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# 데이터베이스 컨넥션을 생성한다.
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="smartnqi",
    passwd="nwai1234!",
    database="smart"
)

# 커서를 생성한다.
cur = mydb.cursor()

# ===============================================================================================================
# 해당 측정일자의 기존 자료를 초기화 한다.
# - 실시간 측정데이터(콜단위), 측정단말, 단말그룹 등
# measdate = '20211101' ### <== ★★★★ 시뮬레이터를 실행하고자 하는 측정일자
measdate_start = int(measdate + '000000000')
measdate_end = int(measdate + '235959999')

cur.execute("set foreign_key_checks = 0")
# 1) 실시간 측정데이터(콜단위)를 삭제한다.
cur.execute(f"DELETE FROM monitor_measurecalldata WHERE meastime between {measdate_start} and {measdate_end}")

# 2) 측정단말 데이터를 삭제한다.
cur.execute(f"DELETE FROM monitor_phonegroup WHERE measdate = {measdate}")

# 3) 단말그룹 데이터를 삭제한다.
cur.execute(f"DELETE FROM monitor_phone WHERE measdate = {measdate}")

cur.execute("COMMIT")
cur.execute("set foreign_key_checks = 1")
# ================================================================================================================

# 데이터를 조회할 쿼리문을 작성한다.
sql = f'''
    select 
        'call' as dataType,
        phone_no,
        meastime,
        networkId,
        groupId,
        currentTime,
        timeline,
        cellId,
        currentCount,
        ispId,
        testNetworkType,
        userInfo1,
        userInfo2,
        siDo,
        guGun,
        addressDetail,
        udpJitter,
        downloadBandwidth,
        uploadBandwidth,
        sinr,
        isWifi,
        latitude,
        longitude,
        bandType,
        p_dl_earfcn,
        p_pci,
        p_rsrp,
        p_SINR,
        NR_EARFCN,
        NR_PCI,
        NR_RSRP,
        NR_SINR
        from tb_ndm_data_measure  

        where meastime between {measdate_start} and {measdate_end}
             and ispId = '45008' 
                 and testNetworkType = 'speed'
                 -- and userInfo1 = '경상남도-진주시-진주교육대학교'
        order by savetime
    '''

# 쿼리문을 실행한다.
cur.execute(sql)
row_headers = [x[0] for x in cur.description]
res = cur.fetchall()

# 데이터를 가져와서 JSON 데이터를 생성한다.
for idx, row in enumerate(res):
    tmpData = dict(zip(row_headers, row))
    jsonData = json.dumps(tmpData)
    try:
        r = requests.post("http://localhost:8000/monitor/json/", data=jsonData)
        # 전송실패 시 오류값을 출력한다.
        if r.status_code == 200:
            print(f"###{idx + 1}번째 처리: 성공")
        else:
            print(f"###{idx + 1}번째 처리: 오류{r.status_code}{r.text}")
    except requests.exceptions.RequestException as e:
        print(str(e))

    # 초당 3개씩 전달하도록 한다.
    # 너무 다량의 데이터를 연속해서 보내면 서버단에서 부하로 오류가 발생한다.
#     if idx % 3 == 0:
#         time.sleep(1)
