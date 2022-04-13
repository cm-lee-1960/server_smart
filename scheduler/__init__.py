from apscheduler.schedulers.background import BackgroundScheduler
from .cron import measuring_end_check, delete_logs_before_week

########################################################################################################################
# 스케쥴러 백그라운드 작업을 등록하고, 실행한다.
# __init__.py 역할
# * 패키지를 초기화 하는 역할
# * 폴더(디렉토리)가 패키지로 인식되도록 하는 역할
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.27 - 주기적으로 수행되어야 하는 작업 또는 텔레그램 커맨드 핸들러를 등록하시 위해 사용할 예정임
#
########################################################################################################################
def start():
    sched = BackgroundScheduler()
    # sched.add_job(XXXX, "cron", hour=1, minute=1) # 특정시간에 수행
    # sched.add_job(telegram_command_handler, 'interval', seconds=5) # 정해진 시간간격으로 수행
    # sched.add_job(measuring_end_check, 'interval', seconds=5)
    sched.add_job(delete_logs_before_week, "cron", hour=11, minute=0)
    # sched.add_job(delete_logs_before_week, 'interval', seconds=5)
    sched.start()
