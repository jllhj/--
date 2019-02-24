from settings import Config
import pymysql

# 开头
def connect():
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cursor

# 结尾
def connect_close(cursor,conn):
    cursor.close()
    conn.close()

def fetch_one(sql,args):
    conn,cursor = connect() # 封装 代码重复了 可查看下面没封装的时候
    cursor.execute(sql,args)
    result = cursor.fetchone()
    connect_close(cursor,conn)
    return result

def fetch_all(sql,args):
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    record_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return record_list


def insert(sql,args):
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row = cursor.execute(sql,args) # 受影响的行数
    conn.commit()
    cursor.close()
    conn.close()
    return row