
import time
from django.db import connection

cursor = connection.cursor()

line = f"""
use smart;
SET foreign_key_checks = 0;

delete FROM smart.tb_ndm_data_measure where meastime between 20211101000000000 and 20211101235959999;
delete from monitor_measurecalldata where meastime between 20211101000000000 and 20211101235959999;
delete from monitor_phone where measdate = '20211101';
delete from monitor_phonegroup where measdate = '20211101';

SET foreign_key_checks = 1;
COMMIT;
"""
res = cursor.execute(line)
print("데이터를 초기화 했습니다.")

f = open('data_20211101.sql', 'r')
i = 0
while True:
    line = f.readline()
    if not line: break
    line += " commit;"
    res = cursor.execute(line)
    i += 1
    print(f"{i}번째처리: {line}")
    time.sleep(1)

f.close()
