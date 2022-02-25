from .models import Message
from django.conf import settings
from monitor.models import Phone


# 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
def make_message(phone):
    """측정단말의 상태에 따라서 메시지를 작성한다."""
    print("make_message()함수 시작")
    # settings.PHONE_STATUS 변수로 선언해도 될지 고민 예정임
    # 2022.01.17 Power On/Off는 데이터 추가해 달라고 하겠음
    # channelId = '-736183270'
    channelId = settings.CHANNEL_ID
    print("채널아이디는 :", channelId)

    # status = ["POWERON", "START", "MEASURING", "END"]  ## MEASUREING은 따로
    status = ["POWERON", "MEASURING", "END"]  ## MEASUREING은 따로
    # 측정 진행 메시지는 DL/UP 측정 단말기의 현재 콜 카운트가 같고, 3, 10, 27, 37, 57 콜 단위로 보고함
    # print("### make_message(): ", self.status, self.phoneGroup.current_count_check())
    if phone.status in status and phone.phoneGroup.current_count_check(phone):

        # 측정 단말기의 DL/UP 평균값들을 가져온다.
        dl_sum, ul_sum, dl_count, ul_count = 0, 0, 0, 0
        avg_downloadBandwidth = 0  # 다운로드 평균속도
        avg_uploadBandwidth = 0  # 업로드 평균속도
        count_check = 0  ## 쌍폰의 카운트 체크

        # for phone in phone.phoneGroup.phone_set.all():  ## 그룹폰 가져오기
        for phone_id in phone.phoneGroup.phone_set.all():  ##그룹폰의 목록 카운트
            # if 콜카운트가 낮은 phone이면 정보 저장하고 패스
            if phone_id.id == phone.id:
                print("이게궁금하다.", phone.id)
                dl_count = phone.dl_count  ##현재 dl카운트
                avg_downloadBandwidth += phone.avg_downloadBandwidth  ## 현재 dl 에버리지
                ul_count = phone.ul_count  ## 현재 ul카운트
                avg_uploadBandwidth += phone.avg_uploadBandwidth  ## 현재 ul 에버리지
                print(dl_count, avg_downloadBandwidth, ul_count, avg_uploadBandwidth)

            else:
                for count, measure in enumerate(
                    Phone.objects.get(id=phone_id.id).measurecalldata_set.all()
                ):
                    if count <= phone.total_count:
                        ## 인스턴스여야만한다. 카운트 체크
                        g_phone_dl = int(
                            0
                            if measure.downloadBandwidth == None
                            else measure.downloadBandwidth
                        )
                        g_phone_ul = int(
                            0
                            if measure.uploadBandwidth == None
                            else measure.uploadBandwidth
                        )
                        ## None값 0으로 초기화

                        # dl_count = phone.dl_count  ##현재 카운트
                        dl_sum += g_phone_dl
                        # ul_count = phone.ul_count  ## 현재 카운트
                        ul_sum += g_phone_ul

                        print(phone)
                        print(
                            "####", phone.phone_no, ul_count, dl_count, ul_sum, dl_sum
                        )

                if dl_sum != 0:
                    avg_downloadBandwidth += dl_sum / phone.total_count
                if ul_sum != 0:
                    avg_uploadBandwidth += ul_sum / phone.total_count

        # 메시지를 작성한다.
        messages = {
            "POWERON": "OO지역 단말이 켜졌습니다.",
            "START": f"측정을 시작합니다.\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
            "MEASURING": f"{phone.total_count}번째 측정 데이터입니다.\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
            ## 이게 우선
            "END": f"측정이 종료되었습니다(총{phone.total_count}건).\n{avg_downloadBandwidth:.1f} / {avg_uploadBandwidth:.1f}",
        }

        msg_test = messages[phone.status]
        print("요게궁금하다. :", msg_test)

        # 전송 메시지를 생성한다.
        Message.objects.create(
            phone=phone,
            send_type="TELE",
            currentCount=phone.total_count,
            message=messages[phone.status],
            channelId=channelId,
            sended=True,
        )
