from flask import Flask, render_template, request, session, redirect, flash
from functools import wraps
from datetime import datetime
import dbUtils as db
from werkzeug.utils import secure_filename
import os

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

# 限制輸入檔案
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def AllowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------------------------------登入功能---------------------------------------------------------------------
# 登入頁面
def LoginRequired(f):
    @wraps(f)
    def Wrapper(*args, **kwargs):
        loginID = session.get('loginID')
        if not loginID:
            return redirect('/login')
        return f(*args, **kwargs)
    return Wrapper

# 登入
@app.route("/login")
def Login():
    dat = db.GetList()
    return render_template('login.html', data=dat)

# 驗證帳密
@app.route('/check', methods=['POST'])
def Check():
    form = request.form
    acc = form['ACC']
    pwd = form['PWD']
    dat = db.GetLoginInfo(acc,pwd)
    if dat and acc == dat['user_account'] and pwd == dat['user_password']:
        session['loginID'] = dat['user_id']
        session['userName'] = dat['user_name']
        return redirect('/')
    else: 
        flash('Your account or password is wrong.')
        return redirect("/login")

# 登出
@app.route('/logout', methods=['POST'])
def Logout():
    session['loginID'] = None
    return redirect('/')

# 註冊頁面
@app.route('/register')
def Register():
    return render_template('register.html')   

# 註冊
@app.route('/registing', methods=['POST'])
def Registing():
    form = request.form
    user_name = form['username']
    account = form['email']
    password = form['password']
    confirm_password = form['confirm_password']
    if password != confirm_password:
        flash("The password doesn't match")
        return redirect("register")
    db.AddUser(user_name,account,password)
    return redirect("/login")
# -------------------------------------------------登入功能---------------------------------------------------------------------


# -------------------------------------------------首頁---------------------------------------------------------------------
# 首頁
@app.route('/')
def Home():
    # dat = db.GetAllItems()
    return render_template('index.html')   

# 搜尋功能
@app.route('/search', methods=['POST'])
def Search():
    form = request.form
    search_input = form['SEARCH']
    product = db.SearchFromDB(search_input)
    print(product)
    return render_template('searchpage.html', data=product, list_title="Search")
# -------------------------------------------------首頁---------------------------------------------------------------------
@app.route("/test")
def test():
    a = 10
    b = 20
    c = 30
    return a,b,c