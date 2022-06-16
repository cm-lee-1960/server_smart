import os, requests, json
from datetime import datetime
from management.models import Center

########################################################################################################################
# 크로샷 문자 메시지를 전송한다.
# ----------------------------------------------------------------------------------------------------------------------
# 2022.04.13 - Nodejs 파일 실행하여 Nodejs에서 Listening(Port:3000) -> Python에서 파라미터 POST 전달(수신번호, 메시지 내용)
# ----------------------------------------------------------------------------------------------------------------------
#   ┌ ---------------┐                                                           nodejs (xroshot_server.js)
#   |  xmcs_msg.py   |    1) nodejs실행 (os.popen)                        ┌───────────────────────────────────────────┐  
#   | send_sms()함수-|----->--------------------------------------------> │ 1) xroshot_server.js 실행    　      　　 │ 
#   ┗ ---------------┛ |  2) POST로 메시지 내용, 수신자 리스트 json 전달  │  -> http 3000포트 리스닝 시작       　 　 │
#     ↑                ┗ -->--------------------------------------------> │ 2) json Data Parsing                      │             
#     |                   3) Status Code 200, Body : {result: 'True'}     │  -> 메시지 내용/수신자 변수 저장  　      │
#     ┗--------------------<----------------------------------------------│-3) Reponse 전송 후 리스닝 종료            │
#                                                                         │  -> Status Code:200, Body:{크로샷 결과}   │
#                                                                         ┖───────────────────────────────────────────┛
# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################

# 로그를 기록하기 위한 로거를 생성한다.
import logging
db_logger = logging.getLogger('db')


def run_xmcs_server():   # 크로샷 서버 실행
  execute_send_sms_nodejs = os.popen('node ./message/xroshot_server.js')  # nodejs 파일 실행 -> 리스닝 시작 // node ./message/sms_broadcast.js

def send_sms(message, sender, receiver):
  '''크로샷 전송 함수
   .파라미터:
    - message: 보낼 메시지 내용 (Text)
    - receiver: 보낼 수신자(str) 리스트 (List) 
   .반환값:
    - Dict {status_code : 200, Body : 전송결과}'''
  url = "http://127.0.0.1:3000"   # nodejs에서 리스닝 중인 주소 - 포트 변경 가능
  
  # 수신자 리스트를 적절한 형태로 변환한다.
  receivers = []
  for i in range(len(receiver)):
    seq_num = {'Seq' : i+1, 'Number' : receiver[i]}
    receivers.append(seq_num)
  receiver.sort(key=len)
  try:
    if (message.isspace() == True) or not(len(receiver[0]) == len(receiver[-1]) == 11):  # 메시지가 공백이거나 or 수신자번호 11자리 아니면 오류
      db_logger.error('Error: 메시지 또는 수신자 번호를 확인해주세요.')
    else:  # 보낼 Data 생성 후 nodejs로 post 전송한다
      data = {'type': 'send', 'message': message, 'sender': sender, 'receiver': receivers}
      headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
      response = requests.post(url, data=json.dumps(data), headers=headers)
      result = {'status_code' : response.status_code, 'body': json.loads(response.text)}
      return result   # nodejs에서 받은 return값을 Dict로 변환한 값 : status code:200, Body:크로샷전송결과})
  except Exception as e:
    raise Exception("Xroshot message send error: %s" % e)


# Queryset 1개를(Message.objects.get) Input으로 받아 Xroshot 전송하는 함수
def send_sms_queryset(queryset, receiver, senderCenter):
  ''' queryset 하나를 input으로 받아 크로샷 전송 함수
  .파라미터:
   - queryset: 메시지 쿼리셋(Message.objects.get)
   - receiver: 수신자 번호(str) 리스트
   .반환값: Dict {status_code : 200, Body : 전송결과} '''
  try:
    msg = queryset.message  # 메시지내용
    if senderCenter in Center.objects.all().values_list('centerName', flat=True):
      sender = Center.objects.filter(centerName=senderCenter)[0].senderNum
    elif queryset.center_id:
      sender = queryset.center.senderNum  # 발신번호
    else:
      qs = Center.objects.filter(centerName='운용본부')
      if qs.exists():
        sender = qs[0].senderNum
      else:
        sender = '01032166418'
    result_sms = send_sms(msg, sender, receiver)  # 크로샷 전송 함수
    if result_sms['status_code'] == 200:
      queryset.sended = True if result_sms['body']['response']['Result'] == 10000 else False  # Result가 10000이면 전송성공
      queryset.sendTime = datetime.strptime(result_sms['body']['response']['Time'], '%Y%m%d%H%M%S')  # 전송시간 datetime 형태로 변환
      queryset.save()
      # 크로샷 전송 결과 개별 조회 수행 (정상 전송되었는지 확인)
      cnt = result_sms['body']['response']['Count']  # 전송 대상 수
      SendDay = result_sms['body']['response']['SubmitTime'][:8]  # 보낸날짜
      JobIDs = []  # 조회할 개별 JobID 리스트
      for i in range(cnt):
        JobIDs.append(result_sms['body']['response']['JobIDs'][i]['JobID'])
        #print(rst['body']['response']['JobIDs'][i]['Index'])
      result = report_sms(JobIDs, SendDay)  # 조회 결과 : Dict, {수신자번호 : 결과}
      return result  # 크로샷 전송 조회 결과를 반환
    else:
      result = {'오류': '전송실패'}
      return result
  except Exception as e:
    raise Exception("Xroshot queryset send error: %s" % e)


# 크로샷 전송 결과 개별 조회 함수는 필요 시 작성
def report_sms(JobIDs, SendDay):
  ''' 크로샷 전송 결과 개별 조회 함수
  .파라미터:
   - JobIDs: 조회할 JobID(int) 리스트(크로샷 전송 후 크로샷 서버에서 회신받은 JobID)
   - SendDay: 전송한 날짜(str, 8자리)
  .반환값: Dict {JobID : 전송결과} '''
  # nodejs에 전송할 data 생성 및 전송
  url = "http://127.0.0.1:3000"   # nodejs에서 리스닝 중인 주소 - 포트 변경 가능
  data = {'type':'report', 'JobIDs': JobIDs, 'SendDay': SendDay}
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  response = requests.post(url, data=json.dumps(data), headers=headers)
  cnt = len(JobIDs)
  # 반환할 Dict를 생성한다 : {수신자번호 : 결과}
  result_detail={}
  result={'TotalCount' : cnt, 'SuccessCount' : 0, 'FailCount' : 0, 'FailDetail' : {}, 'DetailAll' : {}}
  for i in range(cnt): 
    if json.loads(response.text)['response']['JobIDs'][i]['Result'] == 0:
      result['SuccessCount'] += 1
    else:  # 실패일 경우 수신자 번호 추가
      result['FailCount'] += 1
      result['FailDetail'][json.loads(response.text)['response']['JobIDs'][i]['ReceiveNumber']] = json.loads(response.text)['response']['JobIDs'][i]['Result']
    result_detail[json.loads(response.text)['response']['JobIDs'][i]['ReceiveNumber']] = json.loads(response.text)['response']['JobIDs'][i]['Result']
  result['DetailAll'] = result_detail
  return result


# test용
def send_sms_queryset_test(queryset, receiver):
  try:
    msg = queryset
    result_sms = send_sms(msg, receiver)  # 크로샷 전송 함수
    # 크로샷 전송 결과 개별 조회 수행 (정상 전송되었는지 확인)
    cnt = result_sms['body']['response']['Count']  # 전송 대상 수
    SendDay = result_sms['body']['response']['SubmitTime'][:8]  # 보낸날짜
    JobIDs = []  # 조회할 개별 JobID 리스트
    for i in range(cnt):
      JobIDs.append(result_sms['body']['response']['JobIDs'][i]['JobID'])
      #print(rst['body']['response']['JobIDs'][i]['Index'])
    result = report_sms(JobIDs, SendDay)  # 조회 결과 : Dict, {수신자번호 : 결과}
    print(result)
    return result  # 크로샷 전송 조회 결과를 반환
  except Exception as e:
    raise Exception("Xroshot queryset send error: %s" % e)
