import pymysql
import time

conn = pymysql.connect(
    host="master", port=32306, user="canal", password="canal", database="canal", charset="utf8"
)

insert_sql = "insert into test(user_name, age) values ('canal', 12)"
# update_sql = "update blog_base set title = 'canal11' where title = 'canal'"
# delete_sql = "delete from blog_base"

cursor = conn.cursor()
num = 0
while True:
    num += 1
    print("---->", num)
    time.sleep(10)
    cursor.execute(insert_sql)
    conn.commit()
    # time.sleep(1)
    # cursor.execute(update_sql)
    # conn.commit()
    # time.sleep(1)
    # cursor.execute(delete_sql)
    # conn.commit()
    # time.sleep(1)