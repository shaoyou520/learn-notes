import pymysql
import time

conn = pymysql.connect(
    host="node1", port=32306, user="syblog", password="Abcde.123", database="blog", charset="utf8"
)

insert_sql = "insert into blog_base(title) values ('canal')"
update_sql = "update blog_base set title = 'canal11' where title = 'canal'"
delete_sql = "delete from blog_base"

cursor = conn.cursor()
num = 0
while True:
    num += 1
    print("---->", num)
    time.sleep(1)
    cursor.execute(insert_sql)
    conn.commit()
    time.sleep(1)
    cursor.execute(update_sql)
    conn.commit()
    time.sleep(1)
    cursor.execute(delete_sql)
    conn.commit()
    time.sleep(1)