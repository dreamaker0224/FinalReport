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


# -------------------------------------------------店家登入功能---------------------------------------------------------------------
def LoginRequired(f):
    @wraps(f)
    def Wrapper(*args, **kwargs):
        S_id = session.get('S_id')
        if not S_id:
            return redirect('/S_login')
        return f(*args, **kwargs)
    return Wrapper
# Store login page
@app.route("/S_Login")
def SLogin():
    return render_template('store_login.html')
# Store account validation
@app.route('/S_Check', methods=['POST'])
def SCheck():
    form = request.form
    acc = form['ACC']
    pwd = form['PWD']
    S_info = db.SGetInfoByAccount(acc, pwd)
    if S_info:
        session['S_id'] = S_info['store_id']
        session['S_name'] = S_info['store_name']
        return redirect('/store_dashboard')
    else:
        flash('Your account or password is incorrect.')
        return redirect("/store_login")
# Store logout
@app.route('/S_Logout', methods=['POST'])
def SLogout():
    session['S_id'] = None
    return redirect('/')
# -------------------------------------------------店家首頁---------------------------------------------------------------------
# Store dashboard page
@app.route('/S_Dashboard')
@LoginRequired
def SDashboard():
    S_id = session.get('store_id')
    orders = db.GetOrdersByStore(S_id)
    return render_template('store_dashboard.html', orders=orders)
# -------------------------------------------------菜單管理---------------------------------------------------------------------
# Store menu page
@app.route('/S_Menu', methods=['GET'])
@LoginRequired
def SMenu():
    S_id = session.get('S_id')
    items = db.GetMenuItemsByStore(S_id)
    return render_template('store_menu.html', items=items)
# Add menu item
@app.route('/S_Add_Item', methods=['POST'])
@LoginRequired
def SAddItem():
    S_id = session.get('store_id')
    form = request.form
    item_name = form['item_name']
    price = form['price']
    description = form['description']
    db.AddMenuItem(S_id, item_name, price, description)
    flash('Item added successfully!')
    return redirect('/store_menu')
# Update menu item
@app.route('/S_Update_Item/<int:item_id>', methods=['GET', 'POST'])
@LoginRequired
def SUpdateItem(item_id):
    if request.method == 'POST':
        form = request.form
        item_name = form['item_name']
        price = form['price']
        description = form['description']
        db.UpdateMenuItem(item_id, item_name, price, description)
        flash('Item updated successfully!')
        return redirect('/store_menu')
    item = db.GetMenuItemById(item_id)
    return render_template('store_update_item.html', item=item)
# Delete menu item
@app.route('/S_Delete_Item/<int:item_id>', methods=['GET'])
@LoginRequired
def SDeleteItem(item_id):
    db.DeleteMenuItem(item_id)
    flash('Item deleted successfully!')
    return redirect('/store_menu')
# -------------------------------------------------訂單管理---------------------------------------------------------------------
# Order details
@app.route('/Store_Order_Details/<int:order_id>', methods=['GET'])
@LoginRequired
def SOrderDetails(order_id):
    items = db.GetOrderItems(order_id)
    total_amount = db.CalculateOrderTotal(order_id)
    return render_template('store_order_details.html', items=items, total_amount=total_amount, order_id=order_id)
# Update order status
@app.route('/S_Update_Order_status/<int:order_id>', methods=['POST'])
@LoginRequired
def SUpdateOrderStatus(order_id):
    status = request.form['status']
    db.UpdateOrderStatus(order_id, status)
    flash('Order status updated successfully!')
    return redirect('/store_dashboard')
# -------------------------------------------------店家報表---------------------------------------------------------------------
# Sales report for current month
@app.route('/S_Sales_Report', methods=['GET'])
@LoginRequired
def SSalesReport():
    store_id = session.get('store_id')
    year = datetime.now().year
    month = datetime.now().month
    total_sales = db.GetMonthlySalesReport(store_id, year, month)
    return render_template('store_sales_report.html', total_sales=total_sales, year=year, month=month)
# -------------------------------------------------店家管理---------------------------------------------------------------------
# Update store info
@app.route('/S_Update_Info', methods=['GET', 'POST'])
@LoginRequired
def SUpdateInfo():
    S_id = session.get('store_id')
    S_info = db.GetStoreInfo('store_id')
    
    if request.method == 'POST':
        S_name = request.form['store_name']
        S_address = request.form['store_address']
        S_phone = request.form['store_phone']
        db.UpdateStoreInfo('store_id', S_name, S_address, S_phone)
        flash('S information updated successfully!')
        return redirect('/S_dashboard')
    
    return render_template('S_update_info.html', S_info=S_info)
# -------------------------------------------------店家刪除訂單---------------------------------------------------------------------
# Delete order
@app.route('/S_Delete_Order/<int:order_id>', methods=['GET'])
@LoginRequired
def SDeleteOrder(order_id):
    db.DeleteOrder(order_id)
    flash('Order deleted successfully!')
    return redirect('/S_dashboard')
if __name__ == '__main__':
    app.run(debug=True)