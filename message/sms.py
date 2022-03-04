from subprocess import check_output


################## (3.4) 문자메시지 전송 ###########################################
######## node.js 파일 호출 / 변수 전달(메시지 내용, 수신번호) 가능하도록 수정해야함 ##
######## 현재 sms_broadcast.js 에 작성된 내용/수신번호로만 전달됨 ###################
###################################################################################
def send_sms():
  result = check_output(['node', 'sms_broadcast.js'])
  return print(result)

# def send_sms2():
#   check_output(['node', 'sms_broadcast.js'])
