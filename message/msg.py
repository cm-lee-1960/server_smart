


# 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
def make_message(mdata):
    pass
    # '''측정단말의 상태에 따라서 메시지를 작성한다.'''
    # print("make_message()함수 시작")
    # # settings.PHONE_STATUS 변수로 선언해도 될지 고민 예정임
    # # 2022.01.17 Power On/Off는 데이터 추가해 달라고 하겠음
    # channelId = '-736183270' 
    # status = ['POWERON', 'START', 'MEASURING', 'END']
    # # 측정 진행 메시지는 DL/UP 측정 단말기의 현재 콜 카운트가 같고, 3, 10, 27, 37, 57 콜 단위로 보고함
    # # print("### make_message(): ", self.status, self.phoneGroup.current_count_check())
    # if self.status in status and self.phoneGroup.current_count_check(self):
    #     # 측정 단말기의 DL/UP 평균값들을 가져온다.
    #     dl_sum, ul_sum, dl_count, ul_count = 0, 0, 0, 0
    #     avg_downloadBandwidth = 0 # 다운로드 평균속도
    #     avg_uploadBandwidth = 0   # 업로드 평균속도
    #     for phone in self.phoneGroup.phone_set.all():
    #         dl_sum += phone.avg_downloadBandwidth * dl_count
    #         dl_count += phone.dl_count
    #         ul_sum += phone.avg_uploadBandwidth * ul_count
    #         ul_count += phone.ul_count
    #         print(phone)
    #         print("####", phone.phone_no, dl_sum, dl_count, ul_sum, ul_sum) 
    #     if dl_count > 0 : avg_downloadBandwidth = dl_sum / dl_count
    #     if ul_count > 0 : avg_uploadBandwidth = ul_sum / ul_count

    #     # 메시지를 작성한다. 
    #     messages = { 
    #         'POWERON': "OO지역 단말이 켜졌습니다.",
    #         'START': f"측정을 시작합니다.\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
    #         'MEASURING': f"{self.total_count}번째 측정 데이터입니다.\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
    #         'END': f"측정이 종료되었습니다(총{self.total_count}건).\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
    #         }

    #     # 전송 메시지를 생성한다. 
    #     Message.objects.create(
    #         phone = self,
    #         send_type = 'TELE',
    #         currentCount = self.total_count,
    #         message = messages[self.status],
    #         channelId = channelId
    #     )

def send_message(sender, **kwargs):
    #     bot.sendMessage(kwargs['instance'].channelId, text=kwargs['instance'].message)
    # 텔레그램 있때는 텔레그램 함수 호출하고, 정상이면 sended = True
    # 크로샷 때는 
    pass
