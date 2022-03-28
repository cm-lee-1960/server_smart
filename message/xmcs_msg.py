from subprocess import check_output, call, Popen
import os

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

def send_sms():
  execute_sms_nodejs = os.popen('node ./message/sms_broadcast.js')
  result = execute_sms_nodejs.read()
  return result