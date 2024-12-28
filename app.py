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
    role = form['role']
    dat = db.GetLoginInfo(acc,pwd)
    if dat and acc == dat['email'] and pwd == dat['password'] and role == dat['role']:
        session['loginID'] = dat['user_id']
        session['name'] = dat['name']
        session['role'] = dat['role']
        if session['role'] == 'customer':
            return redirect('/')
        elif session['role'] == 'store':
            return redirect('/S_Dashboard')
        elif session['role'] == 'delivery':
            return redirect('/')
        elif session['role'] == 'platform':
            return redirect('/admin_store')
        else:
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
@app.route('/search', methods=['GET'])
def Search():
    form = request.form
    search_input = form['SEARCH']
    product = db.SearchFromDB(search_input)
    print(product)
    return render_template('searchpage.html', data=product, list_title="Search")
# -------------------------------------------------首頁---------------------------------------------------------------------











# -------------------------------------------------平台---------------------------------------------------------------------

@app.route('/admin_store')
def PAdminStore():
    data = db.PGetStoreTransaction()
    pdata = []
    for i in data:
        store_income = float(i['total_sum'])
        tmpdic = {"store_name": i["store_name"],
                  "store_income": store_income,
                  "platform_income": store_income*0.35,
                  "store_profit": store_income*0.75
                  }
        pdata.append(tmpdic)
    return render_template('admin.html', data = pdata )

@app.route('/admin_customer')
def PAdminCustomer():
    data = db.PGetCustomerTransaction()
    pdata = []
    for i in data:
        store_income = float(i['total_sum'])
        tmpdic = {"store_name": i["store_name"],
                  "store_income": store_income,
                  "platform_income": store_income*0.35,
                  "store_profit": store_income*0.75
                  }
        pdata.append(tmpdic)
    return render_template('admin.html', data = pdata )

@app.route('/admin_delivery')
def PAdminDelivery():
    data = db.PGetdeliveryTransaction()
    pdata = []
    for i in data:
        store_income = float(i['total_sum'])
        tmpdic = {"store_name": i["store_name"],
                  "store_income": store_income,
                  "platform_income": store_income*0.35,
                  "store_profit": store_income*0.75
                  }
        pdata.append(tmpdic)
    return render_template('admin.html', data = pdata )

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
    
    
    
    
    
    
    
    
    
    
    
    

# -------------------------------------------------外送員功能---------------------------------------------------------------------
# 外送員首頁：待接訂單與已接訂單
@app.route('/deliveryhome')
@LoginRequired
def DeliveryHome():
    pending_orders = db.GetPendingOrders()  # 待接訂單
    delivery_id = session['loginID']  # 取得外送員 ID
    accepted_orders = db.GetAcceptedOrders(delivery_id)
    completed_orders = db.GetCompletedOrders(delivery_id)  # 完成訂單，根據外送員 ID
    return render_template('deliveryhome.html', pending_orders=pending_orders, accepted_orders=accepted_orders,completed_orders=completed_orders)

@app.route('/pending_order/<int:order_id>', methods=['GET'])
@LoginRequired
def PendingDetail(order_id):
    # 獲取訂單資料，包括商品列表、商家資訊和顧客資訊
    order_items, store_info, customer_info = db.GetOrderDetails(order_id)
    order_status = db.GetOrderStatus(order_id)
    
    order_delivery_id = db.GetDeliveryID(order_id) 

    total_quantity = sum(item['quantity'] for item in order_items)
    total_price = sum(item['total_item_price'] for item in order_items)
    
    return render_template(
        'order_detail.html',
        order_items=order_items,
        order_id=order_id,
        store_name=store_info.get('store_name', ''),
        store_address=store_info.get('store_address', ''),
        customer_name=customer_info.get('customer_name', ''),
        customer_address=customer_info.get('customer_address', ''),
        total_quantity=total_quantity,
        total_price=total_price,
        order_status=order_status,
        delivery_id=order_delivery_id,
        is_pending=True
    )

@app.route('/order_detail/<int:order_id>', methods=['GET'])
@LoginRequired
def AcceptedDetail(order_id):

    order_items, store_info, customer_info = db.GetOrderDetails(order_id)
    order_status = db.GetOrderStatus(order_id)
    delivery_id = session.get('delivery_id')

    total_quantity = sum(item['quantity'] for item in order_items)
    total_price = sum(item['total_item_price'] for item in order_items)
    
    return render_template(
        'order_detail.html',
        order_items=order_items,
        order_id=order_id,
        store_name=store_info.get('store_name', ''),
        store_address=store_info.get('store_address', ''),
        customer_name=customer_info.get('customer_name', ''),
        customer_address=customer_info.get('customer_address', ''),
        total_quantity=total_quantity,
        total_price=total_price,
        order_status=order_status,
        delivery_id=delivery_id,  # 将数据库中的 delivery_id 传递给模板
        is_pending=False
    )

@app.route('/Completed_order/<int:order_id>', methods=['GET'])
@LoginRequired
def CompletedDetail(order_id):
    # 獲取訂單資料，包括商品列表、商家資訊和顧客資訊
    order_items, store_info, customer_info = db.GetOrderDetails(order_id)
    order_status = db.GetOrderStatus(order_id)
    feedback = db.GetFeedbackByOrder(order_id)
    order_delivery_id = db.GetDeliveryID(order_id) 

    total_quantity = sum(item['quantity'] for item in order_items)
    total_price = sum(item['total_item_price'] for item in order_items)
    
    return render_template(
        'order_detail.html',
        order_items=order_items,
        order_id=order_id,
        store_name=store_info.get('store_name', ''),
        store_address=store_info.get('store_address', ''),
        customer_name=customer_info.get('customer_name', ''),
        customer_address=customer_info.get('customer_address', ''),
        total_quantity=total_quantity,
        total_price=total_price,
        order_status=order_status,
        delivery_id=order_delivery_id,
        feedback=feedback
    )

@app.route('/order/accept/<int:order_id>', methods=['POST'])
@LoginRequired
def accept_order(order_id):
    # 確認當前登入的外送員ID是否存在於 session 中
    delivery_id = session.get('delivery_id')  # 使用 session 中儲存的外送員ID
    if not delivery_id:  # 如果沒有登入，跳轉到登入頁面
        return redirect("/login")
    
    # 設置訂單的 delivery_id，標示該外送員接單
    db.UpdateOrderStatus(order_id, status='waiting', delivery_id=delivery_id)  # 保持 status 為 'waiting'

    return redirect('/deliveryHome')

@app.route('/order/complete/<int:order_id>', methods=['POST'])
@LoginRequired
def complete_order(order_id):
    # 確認當前登入的外送員ID是否存在於 session 中
    delivery_id = session.get('delivery_id')
    if not delivery_id: 
        return redirect("/login")  # 未登入則跳轉到登入頁面 

    # 更新訂單狀態為已完成
    db.UpdateOrderStatus(order_id, status='completed', delivery_id=delivery_id)
    
    # 完成訂單後返回訂單首頁
    return redirect('/deliveryhome')