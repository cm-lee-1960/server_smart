from subprocess import check_output, call, Popen
import os

################## (3.4) 문자메시지 전송 ###########################################
######## node.js 파일 호출 / 변수 전달(메시지 내용, 수신번호) 가능하도록 수정해야함 ##
######## 현재 sms_broadcast.js 에 작성된 내용/수신번호로만 전달됨 ###################
######## (3.13) subporcess -> os 함수로 변경, 추후 수정 필요(예정}) #################
###################################################################################
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


def send_sms():
  execute_sms_nodejs = os.popen('node ./message/sms_broadcast.js')
  result = execute_sms_nodejs.read()
  return result