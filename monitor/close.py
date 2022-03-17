from email import message
from django.conf import settings
from .models import Phone, PhoneGroup, MeasureCallData, Message
from django.conf import settings
from django.db.models import Max, Min, Avg, Count, Q

###################################################################################################
# 측정종료 및 측정마감 모듈
# 1) 측정종료 - 해당지역에 대한 측정을 종료처리
# 2) 측정마감 - 당일 모든 측정을 종료처리
# -------------------------------------------------------------------------------------------------
# 2022-03-11 - ???????
###################################################################################################

def measuring_end2(phonegroup,measdate):

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


## 종료 메시지 만드는 함수
class monitor_close:
  def __init__(self, request):
    self.data_group = PhoneGroup.objects.get(id=request['id'])  # 전달 받은 ID로 PhoneGroup 데이터 할당
    self.data_phone = self.data_group.phone_set.all()   # 해당 그룹의 개별 Phone 데이터 할당
    self.data_calldata = self.data_phone[0].measurecalldata_set.all() | self.data_phone[1].measurecalldata_set.all()   # 해당하는 콜단위 데이터 할당
    self.total_count = min(self.data_group.dl_count, self.data_group.ul_count)  # 총 콜수 (DL 및 UL 카운트 중 최소값)
  
  # 5G -> LTE 전환율 계산 함수
  def make_fivgtolte_trans_percent(self):
    dl_nr_percent = self.data_group.dl_nr_count / self.data_group.dl_count
    ul_nr_percent = self.data_group.ul_nr_count / self.data_group.ul_count
    self.fivgtolte_trans_percent = [round(dl_nr_percent,2), round(ul_nr_percent,2)]
    return self.fivgtolte_trans_percent  # DL/UL 별 값을 List로 반환

  # 평균 속도 계산 함수
  def make_avg_bandwidth(self):
    self.dl_avg = self.data_calldata.exclude(Q(networkId='NR')|Q(downloadBandwidth__isnull=True)|Q(downloadBandwidth=0)).aggregate(Avg('downloadBandwidth'))
    self.ul_avg = self.data_calldata.exclude(Q(networkId='NR')|Q(uploadBandwidth__isnull=True)|Q(uploadBandwidth=0)).aggregate(Avg('uploadBandwidth'))
    self.bandwidth_avg = [round(self.dl_avg['downloadBandwidth__avg']), round(self.ul_avg['uploadBandwidth__avg'])]
    return self.bandwidth_avg  # DL/UL 별 값을 List로 반환

  # 측정 시간 계산 함수
  def make_meas_time(self):
    self.meas_time_all = self.data_calldata.aggregate(Max('meastime'), Min('meastime'))
    self.start_meas_time = str(self.meas_time_all['meastime__min'])[8:10] + ':' + str(self.meas_time_all['meastime__min'])[10:12]
    self.end_meas_time = str(self.meas_time_all['meastime__max'])[8:10] + ':' + str(self.meas_time_all['meastime__max'])[10:12]
    self.meas_time = [self.start_meas_time, self.end_meas_time]
    return self.meas_time  # 시작시간/종료시간 값을 List로 변환
  
  # 종료 메시지 생성 함수
  def make_message(self):
    meas_time = self.make_meas_time()
    avg_bandwidth = self.make_avg_bandwidth()
    if self.data_group.networkId == '5G':  # 측정 타입 5G일 경우 LTE 전환율 계산
      fivgtolte_trans_percent = self.make_fivgtolte_trans_percent()
      message_text = f"ㅇS-CXI {self.data_group.measuringTeam} {self.data_group.networkId} {self.data_group.userInfo1}" + \
              f"측정종료({meas_time[0]}~{meas_time[1]}, {self.total_count}콜)\n" + \
              f"- LTE 전환율(DL/UL, %): {fivgtolte_trans_percent[0]} / {fivgtolte_trans_percent[1]}\n" + \
              f"- 속도(DL/UL, Mbps): {avg_bandwidth[0]} / {avg_bandwidth[1]}"
    else:  # 5G가 아닌 경우 LTE 전환율 제외
      message_text = f"ㅇS-CXI {self.data_group.measuringTeam} {self.data_group.networkId} {self.data_group.userInfo1} \
              측정종료({meas_time[0]}~{meas_time[1]}, {self.total_count}콜)\n" + \
              f"- 속도(DL/UL, Mbps): {avg_bandwidth[0]} / {avg_bandwidth[1]}"
    save_message = Message.objects.create(
      phone=self.data_phone[0],
      status='END',
      currentCount=self.total_count,
      downloadBandwidth=avg_bandwidth[0],
      uploadBandwidth=avg_bandwidth[1],
      measdate=self.data_group.measdate,
      userInfo1=self.data_group.userInfo1,
      messageType='SMS',
      message=message_text,
    ) # EndMessage(analysis app) 모델에 DB 저장
    message_id = save_message.id  # 저장된 ID값 할당 (추후 메시지 전송을 위함)
    messages = {'id': message_id, 'text': message_text}  # id 및 내용을 Dictionary에 할당하여 반환
    
    return messages



# -------------------------------------------------------------------------------------------------
# 해당지역의 측정을 종료한다.
# -------------------------------------------------------------------------------------------------
def measuring_end(phoneGroup):
    ''' 해당지역의 측정을 종료하는 함수
      - 파라미터
        . phoneGroup: 단말그룹(PhoneGroup)
      - 반환값: dict
        . message_id: 메시지ID
        . message: 메시지 내용
    '''
    # 해당 단말그룹에 묶여 있는 단말기들을 가져온다.
    phone_list = phoneGroup.phone_set.all()
    qs = MeasureCallData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime")
    # DL 평균속도
    avg_downloadBandwidth = round(qs.exclude( Q(networkId='NR') | \
                                              Q(downloadBandwidth__isnull=True) | \
                                              Q(downloadBandwidth=0) \
                                              ).aggregate(Avg('downloadBandwidth'))['downloadBandwidth__avg'],1)
    # UL 평균속도
    avg_uploadBandwidth = round(qs.exclude( Q(networkId='NR') | \
                                            Q(uploadBandwidth__isnull=True) | \
                                            Q(uploadBandwidth=0)
                                            ).aggregate(Avg('uploadBandwidth'))['uploadBandwidth__avg'],1)

    # DL/UL 5G->LTE전환율   
    dl_nr_percent = round(phoneGroup.dl_nr_count / phoneGroup.dl_count * 100)
    ul_nr_percent = round(phoneGroup.ul_nr_count / phoneGroup.ul_count * 100)

    # 총 콜카운트를 가져온다.
    total_count = min(phoneGroup.dl_count, phoneGroup.ul_count) 
   
    # 측정시작 시간가 측정종료 시간을 확인한다.
    meastime_max_min = qs.aggregate(Max('meastime'), Min('meastime'))
    globals().update(meastime_max_min)
    start_meastime = str(meastime__min)[8:10] + ':' + str(meastime__min)[10:12]
    end_meastime = str(meastime__max)[8:10] + ':' + str(meastime__max)[10:12]

    # 메시지를 작성한다.
    message = f"ㅇS-CXI {phoneGroup.measuringTeam} {phoneGroup.networkId} {phoneGroup.userInfo1}" + \
            f"측정종료({start_meastime}~{end_meastime}, {total_count}콜)\n"
    # 5G의 경우 메시지 내용에 LTE전환율 포함한다.
    if phoneGroup.networkId == '5G':  
        message += f"- LTE 전환율(DL/UL, %): {dl_nr_percent} / {ul_nr_percent}\n" 
    message += f"- 속도(DL/UL, Mbps): {avg_downloadBandwidth} / {avg_uploadBandwidth}"

    # 메시지를 저장한다.
    result = Message.objects.create(
            phone=None,
            status='END',
            measdate=phoneGroup.measdate,
            sendType = 'XMCS',
            userInfo1=phoneGroup.userInfo1,
            phone_no=None,
            downloadBandwidth=avg_downloadBandwidth,
            uploadBandwidth=avg_uploadBandwidth,
            messageType='SMS',
            message = message,
            channelId = '',
            sended=True
        )

    # 반환값에 대해서는 향후 고민 필요
    return_value = {'message_id': result.id, 'message': message}

    return return_value