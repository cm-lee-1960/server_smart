from django.conf import settings
from .models import Phone, PhoneGroup, Message

###################################################################################################
# 측정종료 및 측정마감 모듈
# 1) 측정종료 - 해당지역에 대한 측정을 종료처리
# 2) 측정마감 - 당일 모든 측정을 종료처리
# -------------------------------------------------------------------------------------------------
# 2022-03-11 - ???????
###################################################################################################

def measuring_end(phonegroup,measdate):
    '''해당지역 측정을 종효하는 함수'''
    # 1) 단말그룹: 상태변경
    # 2) 측정단말: 상태변경
    # 3) 해당지역 측정종료 메시지 생성 (유형: 텔레그램(TELE))
    # * 별도누적 테이블(모델) 필요 없음 - 검증을 위해 필요한 경우 메시지 모델에 항목 추가
    ## phonegroup == 폰그룹아이디, measdate == 측정날짜
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
        
    pass

def measuing_day_close():
    '''당일측정을 마감하는 함수'''
    # 1) 단말그룹: 상태변경 - 혹시 남아 있는 상태(True)
    # 2) 측정단말: 상태변경 - 혹시 남아 있는 상태(Tre)
    # 3) 당일 측정마감 데이터 생성 --> 일일 상황보고 자료 활용 가능
    #    - 대상 데이터: 초단위 데이터
    # 4) 당일 측정종료 메시지 생성 (유형: 단문메시지(XMCS))
    pass