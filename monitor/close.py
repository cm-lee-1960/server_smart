from email import message
from django.conf import settings
from .models import Phone, PhoneGroup, Message
from django.conf import settings
import mysql.connector
import requests, json
import time

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
    
    ## 폰이 networkid가 5G면 전환율 메세지 생성
    if f_phone_0.networkid == '5G':
        net_change = f"-LTE 전환율(DL/UL, %):"+ str(pg_check.dl_nr_count/t_dl_count) \
        + "/" + str(pg_check.dl_ul_count/t_ul_count)
    else:
        net_change =''
        
    avg_downloadBandwidth = avg_downloadBandwidth / t_dl_count
    avg_uploadBandwidth = avg_uploadBandwidth / t_ul_count

    messageContent = str(pg_check.measuringTeam) + str(f_phone_0.networkid) \
                     + f"종료메세지== dl:" + str(avg_downloadBandwidth) +"ul:" +str(avg_uploadBandwidth)   ## 수정
                
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
# def area_make_message(pg_check,f_phone_0,net_change):

#      messageContent = str(pg_check.measuringTeam) + str(f_phone_0.networkid) \
#                      + str(f_phone_0.siDo) + str(f_phone_0.guGun) + str(f_phone_0.addressDetail) \
#                      + f"측정ㅈ" 
                     
                     
#                      f"종료메세지== dl:" + str(avg_downloadBandwidth) +"ul:" +str(avg_uploadBandwidth)   ## 수정
    
def measuing_day_close(measdate):
    '''당일측정을 마감하는 함수'''
    # 1) 단말그룹: 상태변경 - 혹시 남아 있는 상태(True)
    # 2) 측정단말: 상태변경 - 혹시 남아 있는 상태(Tre)
    # 3) 당일 측정마감 데이터 생성 --> 일일 상황보고 자료 활용 가능
    #    - 대상 데이터: 초단위 데이터
    # 4) 당일 측정종료 메시지 생성 (유형: 단문메시지(XMCS))
    
    try:
        pg_check_day = PhoneGroup.objects.filter(measdate=measdate)
        #해당일자 폰그룹 쿼리셋 모두 검출
        pg_check_day.update(active=0)
        ## 모든 폰그룹 active 0으로 변경
        for pg_num in pg_check_day:
            p_check_day = pg_num.phone_set.all()
            p_check_day.update(active=0)
            
        ## 폰그룹의 하위 폰 active 0으로 변경
        
    except Exception as e:     
        print("해당일자 폰그룹 혹은 폰 존재안함:",str(e))
    
    ##센터별 DL,UL 처리 SQL USERINFO 데이터 신뢰 저하로 폰번호화 측정시간으로 처리하고 
    ##addressdetail로 센터 매핑
    
    #sql = 
    
    ## 초단위 데이터 가져오기 및 DB 생성
    #s_data_search(measdate, sql)
    
    ###############################################
    ## 1. 초단위 데이터로 일일 보고 데이터 생성
    ## 2. 센터별 분리 
    ## 3. 센터별 메세지 생성
    ## 4. 일괄 메세지 생성
    ## 5. 초단위 로우데이터 DB 삭제
    ###############################################
    pass

# def s_data_search(measdate, sql):

#     ## db  커넥터
#     mydb = mysql.connector.connect(
#         host="127.0.0.1",
#         user="smartnqi",
#         passwd="nwai1234!",
#         database="smart"
#     )
#     ##커서 생성
#     cur = mydb.cursor()
#     ##조회sql 생성    
#     sql = '''select * from tb_ndm_data_measure'''
    
#     cur.execute(sql)
#     row_headers=[x[0] for x in cur.description]
#     res = cur.fetchall()
    
#     ## 초단위 데이터 DB 생성
#     ## create 모델    
#     return 0