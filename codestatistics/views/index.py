from flask import Blueprint,session,redirect,render_template,request
import uuid
from ..utils import helper
import os,json
import decimal
# 不能和函数重名
ind = Blueprint('index',__name__)

@ind.before_request
def process_request():
    if not session.get('user_info'):
        return redirect('/login')
    return None

@ind.route('/index')
def index():
    ret = session['user_info'].get('nickname')
    print(ret)
    return render_template('index.html',ret=ret)

@ind.route('/user_list',methods=['GET','POST'])
def user_list():
    import pymysql
    # conn = pymysql.Connect(host='127.0.0.1', user='root', password='468867748', database='day118', port=3306)
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute('select * from userinfo')
    # data_list = cursor.fetchall()
    # cursor.close()
    # conn.close()
    if request.method == 'POST':
        view_list = helper.fetch_all('select user_id,sum(line),nickname from record inner join userinfo on record.user_id = userinfo.id group by user_id',[])
        print(view_list)
        line_list = []
        nickname_list = []
        for item in view_list:
            line = int(item.get('sum(line)'))
            nickname = item.get('nickname')
            # print('****',line,nickname)
            line_list.append(line)
            nickname_list.append(nickname)
        ret = {'line_list':line_list,'nickname_list':nickname_list}
        print(line_list)
        return json.dumps(ret)
    data_list = helper.fetch_all('select * from userinfo',[])
    return render_template('user_list.html',data_list=data_list)

@ind.route('/detail/<int:nid>',methods=['GET','POST'])
def detail(nid):

    import pymysql
    # conn = pymysql.Connect(host='127.0.0.1', user='root', password='468867748', database='day118', port=3306)
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute('select id,line,ctime from record where user_id=%s',(nid,))
    # record_list = cursor.fetchall()
    # cursor.close()
    # conn.close()
    record_list = helper.fetch_all('select id,line,ctime from record where user_id=%s',(nid,))
    if request.method=="POST":
        line_list = []
        time_list=[]
        for item in record_list:
            line=item.get("line")
            time=item.get("ctime").strftime("%Y-%m-%d")
            date = item.get("ctime").strftime("%Y-%m")
            line_list.append(line)
            time_list.append(time)
            #print(line_list)
        ret={"line_list":line_list,"time_list":time_list,"date":date}
        return json.dumps(ret)
    #print(record_list)
    return render_template('detail.html', record_list=record_list)

@ind.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    file_obj = request.files.get('code')
    print(file_obj)

    # 1.检查上传文件的后缀名
    name_ext = file_obj.filename.rsplit('.',maxsplit=1)
    print(name_ext)
    if len(name_ext) != 2:
        return '请上传zip压缩文件'
    if name_ext[1] != 'zip':
        return '请上传zip压缩文件'

    """
    # 2.设置用户最大限制能传多少M文件 设置在settings

    # 2.5获取上传的文件 并写入到本地服务器
    file_path = os.path.join("files", file_obj.filename)
    # 从file_obj.stream中读取内容，写入到文件
    file_obj.save(file_path)

    # 3. 解压zip文件
    import shutil
    # 通过open打开压缩文件，读取内容再进行解压
    shutil._unpack_zipfile(file_path,'asdsada')
    """

    # 2+3,接受用户上传文件，并解压到指定目录
    import shutil
    target_path = os.path.join('files',str(uuid.uuid4()))
    # file_obj.stream 拿到里面的内容
    shutil._unpack_zipfile(file_obj.stream, target_path)

    # 4 遍历所有文件
    total_num = 0
    for base_path,folder,file_list in os.walk(target_path):
        for file_name in file_list:
            file_path = os.path.join(base_path,file_name)
            # print(file_path)
            file_ext = file_path.rsplit('.',maxsplit=1)
            # print(file_ext)
            if len(file_ext) != 2:
                continue
            if file_ext[1] != 'py':
                continue
            file_num = 0

            with open(file_path,'rb') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(b'#'):
                        continue
                    file_num += 1
            print(file_num,file_path)
            total_num += file_num
    print(total_num)

    # 获取当前时间
    import datetime
    ctime = datetime.date.today()

    # 查询数据库
    import pymysql
    # conn = pymysql.Connect(host='127.0.0.1',user='root',password='468867748',database='day118',charset='utf8')
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute('select id from record where ctime=%s and user_id=%s',(ctime,session['user_info']['id']))
    # data = cursor.fetchone()
    # cursor.close()
    # conn.close()
    data = helper.fetch_one('select id from record where ctime=%s and user_id=%s',(ctime,session['user_info']['id']))

    if data:
        return '今天已上传'

    # 写入数据库
    import pymysql
    # conn = pymysql.Connect(host='127.0.0.1', user='root', password='468867748', database='day118', charset='utf8')
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute('insert into record(line,ctime,user_id)value (%s,%s,%s)',(total_num,ctime,session['user_info']['id']))
    # conn.commit()
    # cursor.close()
    # conn.close()
    helper.insert('insert into record(line,ctime,user_id)value (%s,%s,%s)',(total_num,ctime,session['user_info']['id']))

    return '上传成功'