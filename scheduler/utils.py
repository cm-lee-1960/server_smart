from functools import wraps
from django.db import connection

########################################################################################################################
# 데이터베이스 접속상태를 확인해서 비정상인 경우 재접속하는 데코레이션 장식자
########################################################################################################################
def db_auto_reconnect(func):
    """데이터베이스 접속상태를 확인해서 비정상인 경우 재접속하는 데코레이션 모듈"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            connection.connection.pind()
        except Exception as e:
            connection.close()
        return func(*args, **kwargs)

    return wrapper
