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
    # -------------------------------------------------顧客---------------------------------------------------------------------   
    name = session.get('name')
    customer_id = session.get('customer_id')
    order_id =db.CGetLatestOrderId(customer_id)
    db.DeleteUnpaidOrders(customer_id)
# -------------------------------------------------顧客---------------------------------------------------------------------   
    return render_template('index.html', name=name,customer_id=customer_id)   

# 搜尋功能
@app.route('/search', methods=['POST'])
def Search():
    form = request.form
    search_input = form['SEARCH']
    product = db.SearchFromDB(search_input)
    print(product)
    return render_template('searchpage.html', data=product, list_title="Search")
# -------------------------------------------------首頁---------------------------------------------------------------------

# -------------------------------------------------平台---------------------------------------------------------------------

@app.route('/admin')
def PDashBoard():
    return render_template('admin.html')

# -------------------------------------------------平台---------------------------------------------------------------------

# -------------------------------------------------顧客---------------------------------------------------------------------    
@app.route('/C_商家菜單', methods=['GET'])
def Cg1():
    store_name = request.args.get('store_name')
    result = db.CGetStoreId(store_name)
    store_id = result['store_id']
    session['store_id'] = store_id
    main = db.CGetList()
    snacks =db.CGetList3()
    drinks =db.CGetList4()
    data =db.CGetList5()
    return render_template('/C_商家菜單.html', main=main, snacks=snacks, drinks=drinks, data=data,store_id=store_id)

@app.route('/C_訂單確認', methods=['POST'])
def COrderConfirmation():
    items = request.form
    customer_id = session.get('customer_id')
    store_id = session.get('store_id')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 訂單建立時間
   
    # 先新增訂單到 orders 表
    db.CAddToList2(customer_id, created_at, store_id)

    # 獲取顧客最新的訂單 ID
    order_id =db.CGetLatestOrderId(customer_id)
    
    # 處理訂單的每一項商品
    order_details = {item: int(quantity) for item, quantity in items.items() if item.startswith('item_')}
    for item_id, quantity in order_details.items():
        item_id = item_id.replace('item_', '')
        price = db.CGetItemPrice(item_id)  # 假設有函數取得商品價格
        db.CAddOrderItem(order_id, item_id, quantity, price)  # 將商品加入 order_items 表

    # 計算訂單總金額
    total_amount =db.CCalculateTotalAmount(order_id)

    # 傳遞訂單數據和總金額
    data =db.CGetList6(order_id)
    return render_template('C_訂單確認.html', order_details=order_details, data=data, total_amount=total_amount)

@app.route("/C_payaddress", methods=["GET", "POST"])
def Cg5():
    customer_id = session.get('customer_id')
    order_id = db.CGetLatestOrderId(customer_id)

    if request.method == "POST":
        # 獲取總金額並更新到 orders 表
        total_amount = db.CCalculateTotalAmount(order_id)
        db.CUpdateToList(total_amount, order_id)

        # 獲取地址（可以從 POST 資料中取得）
        address = request.form.get("address")

        # 這裡可以根據需求更新地址或進一步處理
        return redirect("/")  # 確認付款後跳轉回首頁

    else:
        # 獲取總金額及地址資料
        total_amount = db.CCalculateTotalAmount(order_id)
        address = db.CAddress(customer_id)
        return render_template('/C_確認付款方式.html', total_amount=total_amount, address=address)


@app.route("/C_delete")
def Cdelete():
    customer_id = session.get('customer_id')
    order_id =db.CGetLatestOrderId(customer_id)
    db.CDelete2(order_id)
    db.CDelete(order_id)
    return redirect('/')
# -------------------------------------------------顧客---------------------------------------------------------------------    