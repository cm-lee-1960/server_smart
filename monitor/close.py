<<<<<<< HEAD
from django.conf import settings
from .models import Phone, PhoneGroup, Message
from django.conf import settings

=======
>>>>>>> 0f277551f46bb7d33cd5d5a5e6c3cfaf6273b726
###################################################################################################
# 측정종료 및 측정마감 모듈
# 1) 측정종료 - 해당지역에 대한 측정을 종료처리
# 2) 측정마감 - 당일 모든 측정을 종료처리
# -------------------------------------------------------------------------------------------------
# 2022-03-11 - ???????
###################################################################################################

<<<<<<< HEAD
def measuring_end(phonegroup,measdate):

    channelId = settings.CHANNEL_ID
    ##tele 채널아이디
    
=======
def measuring_end():
>>>>>>> 0f277551f46bb7d33cd5d5a5e6c3cfaf6273b726
    '''해당지역 측정을 종효하는 함수'''
    # 1) 단말그룹: 상태변경
    # 2) 측정단말: 상태변경
    # 3) 해당지역 측정종료 메시지 생성 (유형: 텔레그램(TELE))
    # * 별도누적 테이블(모델) 필요 없음 - 검증을 위해 필요한 경우 메시지 모델에 항목 추가
<<<<<<< HEAD
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
            ## phonegroup 하위 폰 active 일괄 업데이트
        else:
            pg_check.active = 1
            p_check = pg_check.phone_set.all()
            p_check.update(active=1)
        
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
    
    avg_downloadBandwidth = 0
    avg_uploadBandwidth = 0
    t_dl_count = 0
    t_ul_count = 0
    phone = pg_check.phone_set.all()
    if len(phone) > 1:
        for i in range(len(phone)):
            globals()['f_phone_{}'.format(i)]=phone[i]
            
            avg_downloadBandwidth += globals()['f_phone_{}'.format(i)].avg_downloadBandwidth * globals()['f_phone_{}'.format(i)].dl_count
            t_dl_count += globals()['f_phone_{}'.format(i)].dl_count
            avg_uploadBandwidth += globals()['f_phone_{}'.format(i)].avg_uploadBandwidth * globals()['f_phone_{}'.format(i)].ul_count
            t_ul_count += globals()['f_phone_{}'.format(i)].dl_count
                         
        # f_phone_1 = phone[0] ## 폰그룹중 첫번째
        # f_phone_2 = phone[1]
    else:
        f_phone_0 = phone[0] ## 폰그룹중 첫번째
        
    mdata = f_phone_0.measurecalldata_set.filter(phone_id=f_phone_0.id)
    
    ## 폰아이디로 measurecalldata 추출 
    
    avg_downloadBandwidth = avg_downloadBandwidth / t_dl_count
    avg_uploadBandwidth = avg_uploadBandwidth / t_ul_count
    
    messageContent = f"종료메세지" ## 수정
                            
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
    
=======
    pass

>>>>>>> 0f277551f46bb7d33cd5d5a5e6c3cfaf6273b726
def measuing_day_close():
    '''당일측정을 마감하는 함수'''
    # 1) 단말그룹: 상태변경 - 혹시 남아 있는 상태(True)
    # 2) 측정단말: 상태변경 - 혹시 남아 있는 상태(Tre)
    # 3) 당일 측정마감 데이터 생성 --> 일일 상황보고 자료 활용 가능
    #    - 대상 데이터: 초단위 데이터
    # 4) 당일 측정종료 메시지 생성 (유형: 단문메시지(XMCS))
    pass