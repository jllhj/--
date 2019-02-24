# import hashlib
# hash = hashlib.md5(b'asdsadsa')
# # 加密
# hash.update(bytes('456',encoding='utf-8'))
# ret = hash.hexdigest()
# print(ret)


import pymysql
conn = pymysql.Connect(host='127.0.0.1',user='root',password='468867748',database='day118',port=3306)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute('select user_id,sum(line),nickname from record inner join userinfo on record.user_id = userinfo.id group by user_id')
data = cursor.fetchall()
cursor.close()
conn.close()
print(data)