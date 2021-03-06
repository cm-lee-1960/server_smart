from apscheduler.schedulers.background import BackgroundScheduler
from .cron import measuring_end_check, delete_logs_before_week, start_monitoring, daily_jobs_after_meas

########################################################################################################################
# 스케쥴러 백그라운드 작업을 등록하고, 실행한다.
# __init__.py 역할
# * 패키지를 초기화 하는 역할
# * 폴더(디렉토리)가 패키지로 인식되도록 하는 역할
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.27 - 주기적으로 수행되어야 하는 작업 또는 텔레그램 커맨드 핸들러를 등록하시 위해 사용할 예정임
# 2022.06.13 - 매주 월요일 감시가 중지되어 있으면 자동으로 사작한다.
# 2022.06.29 - 측정종료 후 매일 처리해야 하는 작업들을 모아 스케쥴로 등록(매일저녁 10시)
#              * 측정단말 사전정보 내 파워온/오프 초기화(오프상태)
#
########################################################################################################################
def start():
    sched = BackgroundScheduler()
    # sched.add_job(XXXX, "cron", hour=1, minute=1) # 특정시간에 수행
    # sched.add_job(telegram_command_handler, 'interval', seconds=5) # 정해진 시간간격으로 수행
    # sched.add_job(measuring_end_check, 'interval', seconds=5)
    sched.add_job(delete_logs_before_week, "cron", hour=23, minute=0)  # 로그내역 삭제(7일 초과)
    sched.add_job(daily_jobs_after_meas, "cron", hour=22, minute=0)    # 측정종료 후 작업들
    # sched.add_job(delete_logs_before_week, 'interval', seconds=5)
    sched.add_job(start_monitoring, "cron", hour=0, minute=30)         # 매주 월요일 감시시작
    sched.start()
