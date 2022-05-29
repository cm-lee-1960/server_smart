
import time
from django.db import connection

cursor = connection.cursor()
f = open('data_20211101.sql', 'r')
i = 0
while True:
    line = f.readline()
    if not line: break
    line += "; commit;"
    # res = cursor.execute(line)
    i += 1
    print(f"{i}번째처리: {line}")
    time.sleep(1)

f.close()