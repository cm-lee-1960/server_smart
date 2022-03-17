from email import message
from django.conf import settings
from .models import Phone, PhoneGroup, Message
from django.conf import settings
from django.db.models import Max, Min, Avg, Count, Q

###################################################################################################
# 측정종료 및 측정마감 모듈
# 1) 측정종료 - 해당지역에 대한 측정을 종료처리
# 2) 측정마감 - 당일 모든 측정을 종료처리
# -------------------------------------------------------------------------------------------------
# 2022-03-11 - ???????
###################################################################################################

def measuring_end(phonegroup,measdate):

    channelId = settings.CHANNEL_ID
    ##tele 채널아이디
    
    '''해당지역 측정을 종효하는 함수'''
    # 1) 단말그룹: 상태변경
    # 2) 측정단말: 상태변경
    # 3) 해당지역 측정종료 메시지 생성 (유형: 텔레그램(TELE))
    # * 별도누적 테이블(모델) 필요 없음 - 검증을 위해 필요한 경우 메시지 모델에 항목 추가
    ## phonegroup == 폰그룹아이디, measdate == 측정날짜
    ## 메인페이지의 종료 에어리어의 폰그룹 버튼을 눌럿을때는 
    ## Phonegroup의 id값을 가지고 있어야된다.
    try:
        pg_check = PhoneGroup.objects.get(id=phonegroup,measdate=measdate)  
        if pg_check.active: ## phonegroup active가 1이면
            pg_check.active = 0
            ## measingTeam 으로 변경가능
            ## active 0은 stop 모드
            p_check = pg_check.phone_set.all()
            p_check.update(active=0)
            pg_check.save()
            ## phonegroup 하위 폰 active 일괄 업데이트
        else:
            pg_check.active = 1
            p_check = pg_check.phone_set.all()
            p_check.update(active=1)
            pg_check.save()
        
        ## 모델업데이트
    except Exception as e:     
        print("지역측정종료 폰그룹 존재안함:",str(e))
    
    
    ## 메세지 생성
    #1. monitor view에서 low행 하나씩 들어올때마다 make 메세지실행    
    #2. msg.py 에서 make_message함수로 메세지 생성후 message 모델 만들어지고
    #3. post_save 실행 monitor model의 send_message함수실행으로
    #4. bot.send_message_bot 실행
        
    #Q send_message는 왜 monitor model에잇는가        
    ##mdata == measurecalldata
    
    ## 모델 상관관계
    ## Phone Group -> Phone
    ##             -> Message
    ## phone그룹 단말기 정보
    phone = pg_check.phone_set.all()
    
    ## 데이터 초기화
    avg_downloadBandwidth = 0  
    avg_uploadBandwidth = 0
    t_dl_count = 0
    t_ul_count = 0
    
    f_phone_0 = phone[0] ##첫번째 단말기 정보는 기입
    avg_downloadBandwidth = f_phone_0.avg_downloadBandwidth * f_phone_0.dl_count
    t_dl_count = f_phone_0.dl_count
    avg_uploadBandwidth = f_phone_0.avg_uploadBandwidth * f_phone_0.ul_count
    t_ul_count = f_phone_0.ul_count

    
    if len(phone) > 1:
        for i in range(1, len(phone)):
            globals()['f_phone_{}'.format(i)]=phone[i] ## 폰 여러개일 경우대비 변수 생성 변수 초기화 수정필요
        
            avg_downloadBandwidth += globals()['f_phone_{}'.format(i)].avg_downloadBandwidth * globals()['f_phone_{}'.format(i)].dl_count
            t_dl_count += globals()['f_phone_{}'.format(i)].dl_count
            avg_uploadBandwidth += globals()['f_phone_{}'.format(i)].avg_uploadBandwidth * globals()['f_phone_{}'.format(i)].ul_count
            t_ul_count += globals()['f_phone_{}'.format(i)].ul_count
                         
    # else:
    #     f_phone_0 = phone[0] ## 폰그룹중 첫번째
        
    mdata = f_phone_0.measurecalldata_set.filter(phone_id=f_phone_0.id).order_by('-meastime')[0] 
    ##측정시간 기준으로 내림차순정렬의 첫번째 calldata를가져온다 즉 가장 최근측정 콜데이터
    
    ## 폰아이디로 measurecalldata 추출 
    
    avg_downloadBandwidth = avg_downloadBandwidth / t_dl_count
    avg_uploadBandwidth = avg_uploadBandwidth / t_ul_count
    
    messageContent = f"종료메세지== dl:" + str(avg_downloadBandwidth) +"ul:" +str(avg_uploadBandwidth)   ## 수정
                
    Message.objects.create(
        phone=phone[0],  ## 폰그룹에서 첫번째 단말기 정보 기입
        measdate=str(mdata.meastime)[0:8],
        sendType='TELE',
        userInfo1=mdata.userInfo1,
        currentCount=mdata.currentCount,
        phone_no=mdata.phone_no,
        downloadBandwidth=avg_downloadBandwidth,
        uploadBandwidth=avg_uploadBandwidth,
        messageType='SMS',
        message=messageContent,
        channelId=channelId,
        sended=True
    )
    
def measuing_day_close():
    '''당일측정을 마감하는 함수'''
    # 1) 단말그룹: 상태변경 - 혹시 남아 있는 상태(True)
    # 2) 측정단말: 상태변경 - 혹시 남아 있는 상태(Tre)
    # 3) 당일 측정마감 데이터 생성 --> 일일 상황보고 자료 활용 가능
    #    - 대상 데이터: 초단위 데이터
    # 4) 당일 측정종료 메시지 생성 (유형: 단문메시지(XMCS))
    pass


class monitor_close:
  def __init__(self, request):
    self.data_group = PhoneGroup.objects.get(id=request['id'])
    self.data_phone = self.data_group.phone_set.all()
    self.data_calldata = self.data_phone[0].measurecalldata_set.all() | self.data_phone[1].measurecalldata_set.all()
    self.total_count = min(self.data_group.dl_count, self.data_group.ul_count)
  
  def make_fivgtolte_trans_percent(self):
    dl_nr_percent = self.data_group.dl_nr_count / self.data_group.dl_count
    ul_nr_percent = self.data_group.ul_nr_count / self.data_group.ul_count
    self.fivgtolte_trans_percent = [dl_nr_percent, ul_nr_percent]
    return self.fivgtolte_trans_percent

  def make_avg_bandwidth(self):
    self.dl_avg = self.data_calldata.exclude(Q(networkId='NR')|Q(downloadBandwidth__isnull=True)|Q(downloadBandwidth=0)).aggregate(Avg('downloadBandwidth'))
    self.ul_avg = self.data_calldata.exclude(Q(networkId='NR')|Q(uploadBandwidth__isnull=True)|Q(uploadBandwidth=0)).aggregate(Avg('uploadBandwidth'))
    self.bandwidth_avg = [round(self.dl_avg['downloadBandwidth__avg']), round(self.ul_avg['uploadBandwidth__avg'])]
    return self.bandwidth_avg

  def make_meas_time(self):
    self.meas_time_all = self.data_calldata.aggregate(Max('meastime'), Min('meastime'))
    self.start_meas_time = str(self.meas_time_all['meastime__min'])[8:10] + ':' + str(self.meas_time_all['meastime__min'])[10:12]
    self.end_meas_time = str(self.meas_time_all['meastime__max'])[8:10] + ':' + str(self.meas_time_all['meastime__max'])[10:12]
    self.meas_time = [self.start_meas_time, self.end_meas_time]
    return self.meas_time
  
  def make_message(self):
    meas_time = self.make_meas_time()
    avg_bandwidth = self.make_avg_bandwidth()
    if self.data_group.networkId == '5G':
      fivgtolte_trans_percent = self.make_fivgtolte_trans_percent()
      messages = f"<code>ㅇS-CXI {self.data_group.measuringTeam} {self.data_group.networkId} {self.data_group.userInfo1} \
              측정종료({meas_time[0]}~{meas_time[1]}, {self.total_count}콜)\n" + \
              f"- LTE 전환율(DL/UL, %): {fivgtolte_trans_percent[0]}/{fivgtolte_trans_percent[1]}\n" + \
              f"- 속도(DL/UL, Mbps): {avg_bandwidth[0]}/{avg_bandwidth[1]}</code>"
    else:
      messages = f"<code>ㅇS-CXI {self.data_group.measuringTeam} {self.data_group.networkId} {self.data_group.userInfo1} \
        측정종료({meas_time[0]}~{meas_time[1]}, {self.total_count}콜)\n" + \
        f"- 속도(DL/UL, Mbps): {avg_bandwidth[0]}/{avg_bandwidth[1]}</code>"

    return messages