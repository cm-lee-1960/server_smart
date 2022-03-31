#from subprocess import check_output, call, Popen  // subprocess 모듈로도 호출 가능
import os, requests, json

########################################################################################################################
# 크로샷 문자 메시지를 전송한다.
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.04 - Node.js 파일 호출 / 파라미터 전달(수신번호, 메시지 내용)
########################################################################################################################
# def send_sms():
#   result = check_output(['node', 'sms_broadcast.js'], universal_newlines=True)
#   print(result)
#   return result

# def send_sms2():
#   result = call(['node', './message/sms_broadcast.js'])
#   print(result)
#   return result

# def send_sms3():
#   result = Popen(['node', './message/sms_broadcast.js'], universal_newlines=True)
#   return result

# def send_sms_db():
#   execute_sms_nodejs = os.popen('node ./message/sms_broadcast.js')
#   result = execute_sms_nodejs.read()
#   return result
############################ 상기 함수들 삭제 예정 (DB형식 -> Json 형식 변경 예정)

########################################################################################################################
# 크로샷 문자 메시지를 전송한다.
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.31 - Nodejs 파일 호출 -> Nodejs에서 Listening(Port:3000) -> 파라미터 POST 전달(수신번호, 메시지 내용)
# ----------------------------------------------------------------------------------------------------------------------
#   ┌ ---------------┐                                                           nodejs (sms_broadcast.js)
#   |  xmcs_msg.py   |    1) nodejs실행 (os.popen)                        ┌───────────────────────────────────────────┐  
#   | send_sms()함수-|----->--------------------------------------------> │ 1) sms_broadcast.js 실행      　      　　 │ 
#   ┗ ---------------┛ |  2) POST로 메시지 내용, 수신자 리스트 json 전달    │  -> http 3000포트 리스닝 시작        　 　 │
#     ↑                ┗ -->--------------------------------------------> │ 2) json Data Parsing                      │             
#     |                   3) Status Code 200, Body : {result: 'True'}     │  -> 메시지 내용/수신자 변수 저장　  　      │
#     ┗--------------------<----------------------------------------------│-3) eponse 전송 후 리스닝 종료              │
#                                                                         │  -> Status Code:200, Body:{크로샷 결과}    │
#                                                                         ┖───────────────────────────────────────────┛
# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################

def send_sms(message, receiver):
  '''크로샷 전송 함수
   .파라미터
    - message: 보낼 메시지 내용 (Text)
    - receiver: 보낼 수신자 리스트 (List) '''
  url = "http://localhost:3000"   # nodejs에서 리스닝 중인 주소 - 포트 변경 가능
  execute_sms_nodejs = os.popen('node ./message/sms_broadcast2.js')  # nodejs 파일 실행 -> 리스닝 시작 // node ./message/sms_broadcast2.js

  # 수신자 리스트를 적절한 형태로 변환한다.
  receivers = []
  for i in range(len(receiver)):
    seq_num = {'Seq' : i+1, 'Number' : receiver[i]}
    receivers.append(seq_num)

  # 보낼 Data 생성 후 nodejs로 post 전송한다 : 응답받은 후 리스닝 종료됨
  data = {'message': message, 'receiver': receivers}
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  response = requests.post(url, data=json.dumps(data), headers=headers)
  result = {'status_code' : response.status_code, 'Body': json.loads(response.text)}

  print(result)
  return result   # nodejs에서 받은 return값을 Dict로 변환한 값 : status code:200, Body:크로샷전송결과})