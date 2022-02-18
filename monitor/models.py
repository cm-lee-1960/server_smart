from django.db import models
from django.db.models.signals import post_save
from telemsg.tele_msg_old import send_message_bot

###################################################################################################
# 측정 단말기 정보
# * 측정중인 단말을 관리한다. 
# * 측정이 종료되면 해당 측정 단말기 정보를 삭제한다. (Active or Inactive 관리도 가능)
###################################################################################################
class Phone(models.Model):
    phone_no = models.BigIntegerField()
    avg_downloadBandwidth = models.FloatField()
    avg_uploadBandwidth =models.FloatField()
    status = models.CharField(max_length=10)
    total_count = models.IntegerField()
    
    # 측정 단말기의 통계정보를 업데이트 한다.
    def update_info(self, mdata):

        # 단말기의 상태를 업데이트 한다. 
        # 상태 - 'POWERON', 'START', 'MEASURING', 'END'
        if mdata.currentCount == 1:
            self.status = 'START'
        else:
            self.status = 'MEASURING'

        # 단말기의 콜 수를 업데이트 한다. 
        self.total_count = mdata.currentCount

        # 초단위 측정 데이터로 부터 측정 단말기 정보를 업데이트 한다.
        # 업데이트 항목 - DL, UL
        for msdata in self.measureseconddata_set.all():
            print("초단위 데이터: " + str(msdata))

        # 초단위 측정 데이터로 부터 측정 단말기 정보를 업데이트 한다.
        # 업데이트 항목 - ????
        for mcdata in self.measurecalldata_set.all():
            print("콜단위 데이터" + str(mcdata))

    # 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
    def make_message(self):
        # settings.PHONE_STATUS 변수로 선언해도 될지 고민 예정임
        # 2022.01.17 Power On/Off는 데이터 추가해 달라고 하겠음
        status = ['POWERON', 'START', 'MEASURING', 'END']
        messages = { 
            'POWERON': "OO지역 단말이 켜졌습니다.",
            'START': f"측정을 시작합니다.\n{self.phone_no} / {self.avg_downloadBandwidth:.1f} / {self.avg_uploadBandwidth:.1f}",
            'MEASURING': f"{self.total_count}번째 측정 데이터입니다.\n{self.phone_no} / {self.avg_downloadBandwidth:.1f} / {self.avg_downloadBandwidth:.1f}",
            "END": f"측정이 종료되었습니다(총{self.total_count}건).\n{self.phone_no} / {self.avg_downloadBandwidth:.1f} / {self.avg_downloadBandwidth:.1f}",
        }
        if self.status in list(messages.keys()):
            # 측정 진행 메시지는 3, 10, 27, 37, 57 콜 단위로 보고함
            if self.status == 'MEASURING' and self.total_count not in [3, 10, 27, 37, 57]:
                pass
            else:
                # 전송 메시지를 생성한다. 
                Message.objects.create(
                    phone = self,
                    send_type = 'TELE',
                    currentCount = self.total_count,
                    message = messages[self.status]
                )

    # 이벤트 발생을 체크한다.
    def event_occur_check(self):
        # 1)속도저하(low throughput)
        # 2)음성 콜 드랍
        # 3)5G -> LTE 전환
        # 4)측정범위를 벗어나는 경우
        # 5)측정콜이 한곳에 머무는 경우
        pass

    def low_throughput_check(self):
        # 속도저하(low throughput)
        # -품질기준(5G DL: 12M, UL: 2M, LTE DL: 6M, UL: 1M, 3G DL: 256K, UL: 128K
        # -품질취약 LTE 1M, UL: 0.5, 3G DL: 256K, UL 128K
        # -취약지구는 '~산로' 등 특정문구가 들어간 것으로 식별을 해야 하는데, 어려움이 있음(관리자 지정해야? -> 정보관리 대상)
        pass

    def voice_call_drop_check(self):
        # 음성 콜 드랍
        # -품질 취약 VoLTE call drop/setup fail, 3G call drop/setup fail
        # 2022.01.17 DB가 다르기 때문에 나중에 알려 주겠음
        pass

    def fivgtolte_trans_check(self):
        # 5G->LTE 전환시
        # -5G 측정시 LTE로 데이터가 전환되는 경우
        pass

    def out_measuring_range(self):
        # 측정범위를 벗어하는 경우
        # - 측정하는 행정동을 벗어나서 측정이 되는 경우
        # - (아이디어) 행정동을 벗어남이 의심된다는 메시지 + 위치 지도 이미지도 함께 전송
        pass

    def call_staying_check():
        # 측정콜이 한곳에 머무는 경우
        # - 타사 측정단말에 문제가 발생하여 조치를 하거나 차량에 문제가 있거나 등 한곳에 오랫동안 멈는 경우가 있는데,
        # 이렇게 한곳에 멈춰 있는 경우 보고 대상임
        pass

###################################################################################################
# 실시간 측정 데이터(콜 단위)
###################################################################################################     
class MeasureCallData(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    phone_no = models.BigIntegerField()
    neworkid = models.CharField(max_length=10)
    meastime = models.BigIntegerField()
    ispId = models.CharField(max_length=10)
    currentCount = models.IntegerField()
    userInfo2 = models.CharField(max_length=100)
    downloadBandwidth = models.FloatField()
    uploadBandwidth = models.FloatField()

    def __str__(self):
         return f"{self.phone_no}/{self.neworkid}/{self.meastime}/{self.currentCount}/{self.downloadBandwidth}/{self.uploadBandwidth}/"


###################################################################################################
# 실시간 측정 데이터(초 단위)
###################################################################################################
class MeasureSecondData(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    phone_no = models.BigIntegerField()
    neworkid = models.CharField(max_length=10)
    meastime = models.BigIntegerField()
    ispId = models.CharField(max_length=10)
    currentCount = models.IntegerField()
    userInfo2 = models.CharField(max_length=100)
    downloadBandwidth = models.FloatField()
    uploadBandwidth = models.FloatField()

    def __str__(self):
        return f"{self.phone_no}/{self.neworkid}/{self.meastime}/{self.currentCount}"


###################################################################################################
# 실시간 측정 데이터(콜 단위)
###################################################################################################
class Message(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    send_type = models.CharField(max_length=10)
    currentCount = models.IntegerField()
    message = models.TextField()
    # 전송일시 항목추가

# -------------------------------------------------------------------------------------------------
# 전송 메시지가 저장된 후 텔래그램 전송 모듈을 호출한다. 
#--------------------------------------------------------------------------------------------------
post_save.connect(send_message_bot, sender=Message)


