from flask import Blueprint,render_template,request,session,redirect
import pymysql
from ..utils.md5 import md5
from settings import Config
from ..utils import helper

account = Blueprint('account',__name__)


@account.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    # 进行加密 密文和密文进行比较 不然密码要输入密文
    pwd_md5 = md5(pwd)

    data = helper.fetch_one('select id,nickname from userinfo WHERE user=%s and pwd=%s',(user,pwd_md5))

    if not data:
        return render_template('login.html',error='用户名密码错误')
    # session['user_id'] = data['id']
    # session['user_nickname'] = data['nickname']
    session['user_info'] = {'id':data['id'],'nickname':data['nickname']}
    # 也可以session['user_info'] = data {'id': 1, 'user': 'xiaoqiang', 'pwd': '1b9193d0260e00538b0216fc2b141bf5', 'nickname': '大帅比'}
    return redirect('/index')
    # 去数据库中进行校验

@account.route('/logout')
def logout():
    if 'user_info' in session:
        del session['user_info']
    return redirect('/login')