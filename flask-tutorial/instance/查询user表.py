import sqlite3
 
# 连接到SQLite数据库

conn = sqlite3.connect('flaskr.sqlite')
 
# 创建一个Cursor对象并使用它来执行SQL查询
cursor = conn.cursor()
 
# 执行查询
cursor.execute("SELECT * FROM user;")
 
# 获取所有记录列表
rows = cursor.fetchall()
 
for row in rows:
    print(row)
 
# 关闭连接
conn.close()