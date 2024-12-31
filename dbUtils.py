#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="foodpangolin"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)

def GetList():
	sql="select * from users where 1"
	#param=('值',...)
	cursor.execute(sql)
	return cursor.fetchall()

def GetOrder(order_id):
    sql="select * from orders where order_id = %s"
    param = (order_id,)
    cursor.execute(sql,param)
    return cursor.fetchone()

# -------------------------------------------------首頁---------------------------------------------------------------------
def GetAllStores():
    sql='''
    SELECT stores.*, 
       ROUND(AVG(feedback.rating), 1) AS avg_rating, 
       COUNT(feedback.review_id) AS review_count
    FROM stores
    LEFT JOIN orders ON stores.store_id = orders.store_id
    LEFT JOIN feedback ON orders.order_id = feedback.order_id
    GROUP BY stores.store_id;
    '''
    cursor.execute(sql)
    return cursor.fetchall()
# -------------------------------------------------首頁---------------------------------------------------------------------



# -------------------------------------------------登入---------------------------------------------------------------------
def GetLoginInfo(id, pwd):
    sql="select * from users where email=%s and password=%s"
    param=(id,pwd,)
    cursor.execute(sql,param)
    user = cursor.fetchone()
    if user:
        return user
    return None

def GetRoleID(id, role):
    if role == "customer":
        sql="select customer_id as role_id from customers where user_id=%s"
    elif role == "store":
        sql="select store_id as role_id from stores where user_id=%s"
    elif role == "delivery":
        sql="select delivery_id as role_id from delivery_personnel where user_id=%s"
    param=(id,)
    cursor.execute(sql,param)
    role_id = cursor.fetchone()
    if role_id:
        return role_id
    return None
    
# -------------------------------------------------搜尋---------------------------------------------------------------------

# -------------------------------------------------註冊---------------------------------------------------------------------
def AddUser(user_name, account, password, role):
    # 插入用戶資料
    sql = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s);"
    param = (user_name, account, password, role)
    cursor.execute(sql, param)
    conn.commit()

    # 取得剛插入的 user_id
    user_id = cursor.lastrowid

    # 根據角色插入到相應的表格
    if role == 'store':
        # 假設 'stores' 表格有 user_id 欄位
        cursor.execute("INSERT INTO stores (user_id, store_name) VALUES (%s, %s);", (user_id, user_name,))
    elif role == 'customer':
        # 假設 'customers' 表格有 user_id 欄位
        cursor.execute("INSERT INTO customers (user_id) VALUES (%s);", (user_id,))
    elif role == 'delivery_personnel':
        # 假設 'delivery_personnel' 表格有 user_id 欄位
        cursor.execute("INSERT INTO delivery_personnel (user_id) VALUES (%s);", (user_id,))

    # 提交所有更改
    conn.commit()

# -------------------------------------------------註冊---------------------------------------------------------------------

# -------------------------------------------------搜尋---------------------------------------------------------------------
def SearchFromDB(search_input):
    sql = "SELECT * FROM items WHERE item_name LIKE %s;"
    param = (f"%{search_input}%",)
    cursor.execute(sql,param)
    items = cursor.fetchall()
    return items
# -------------------------------------------------搜尋---------------------------------------------------------------------














# -------------------------------------------------搜尋---------------------------------------------------------------------
def PGetStoreTransaction():
    sql = '''
    SELECT s.store_name, SUM(o.total_price) AS total_sum
    FROM orders o
    JOIN stores s ON o.store_id = s.store_id
    WHERE o.status = 'completed'
    GROUP BY s.store_name;
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def PGetCustomerTransaction():
    sql = '''
    SELECT 
    u.user_id, 
    u.name AS user_name, 
    SUM(o.total_price) AS total_sum, 
    COUNT(o.order_id) AS order_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN users u ON c.user_id = u.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, u.name;
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def PGetDeliveryTransaction():
    sql = '''
    SELECT 
    u.user_id, 
    u.name AS user_name, 
    SUM(o.total_price) AS total_sum, 
    COUNT(o.order_id) AS order_count
    FROM orders o
    JOIN delivery_personnel c ON o.delivery_id = c.delivery_id
    JOIN users u ON c.user_id = u.user_id
    WHERE o.status = 'completed'
    GROUP BY u.user_id, u.name;
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
# -------------------------------------------------搜尋---------------------------------------------------------------------
















# -------------------------------------------------顧客---------------------------------------------------------------------
def CGetStoreId(store_name):
    sql = "SELECT store_id FROM stores WHERE store_name = %s"
    cursor.execute(sql, (store_name,))
    result = cursor.fetchone()
    return result
    
def CLog(user_id, password):   # 登入驗證，根據 id 和 pwd 查找登入資料
    sql = "SELECT users.user_id,users.password,users.name,customers.customer_id, customers.address, customers.phone_number FROM users INNER JOIN customers ON users.user_id = customers.user_id Where users.user_id = %s AND users.password = %s"
    param = (user_id, password)
    cursor.execute(sql, param)
    user = cursor.fetchone()  # 獲取查詢結果
    return user

def CGetMenuItems(store_id):
    sql="select * from menu_items where store_id = %s"
    param=(store_id,)
    cursor.execute(sql,param)
    return cursor.fetchall()

def CGetList():# 查詢菜單主菜
	sql="select item_id,store_id,item_name,price,description from menu_items where description LIKE '%主餐%';"
	#param=('值',...)
	cursor.execute(sql)
	return cursor.fetchall()

def CGetList5():# 查詢菜單
    sql = "SELECT item_id, store_id, item_name, price, description FROM menu_items;"
    cursor.execute(sql)
    return cursor.fetchall()    
def CGetList2(): # 查詢確認訂單
	sql="select order_item_id,order_id,item_id,quantity,price from order_items;"
	#param=('值',...)
	cursor.execute(sql)
	return cursor.fetchall()     
def CGetList3(): # 查詢小點
	sql="select item_id,store_id,item_name,price,description from menu_items where description LIKE '%小點%';"
	#param=('值',...)
	cursor.execute(sql)
	return cursor.fetchall()   
def CGetList4():# 查詢飲料
	sql="select item_id,store_id,item_name,price,description from menu_items where description LIKE '%飲料%';"
	#param=('值',...)
	cursor.execute(sql)
	return cursor.fetchall() 
def CGetList6(order_id):# 查詢order_items
    sql = "SELECT order_items.quantity, order_items.price, menu_items.item_name FROM order_items JOIN menu_items ON order_items.item_id = menu_items.item_id WHERE order_items.order_id = %s;"
    cursor.execute(sql,(order_id,))
    return cursor.fetchall()
def CAddOrderItem(order_id, item_id, quantity, price):
    sql = "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (order_id, item_id, quantity, price))
    conn.commit()    
def CGetItemPrice(item_id):#根據商品 ID 獲取價格。
    sql = "SELECT price FROM menu_items WHERE item_id = %s"
    cursor.execute(sql, (item_id,))
    result = cursor.fetchone()
    return result['price']        
def CAddToList2(customer_id,created_at, store_id):#建立order
    sql = "INSERT INTO orders (customer_id,created_at, store_id) VALUES (%s, %s, %s)"
    cursor.execute(sql, (customer_id,created_at,store_id,))
    conn.commit()
    return
def CGetLatestOrderId(customer_id):
    sql = "SELECT MAX(order_id) AS order_id FROM orders WHERE customer_id = %s"
    cursor.execute(sql, (customer_id,))
    result = cursor.fetchone()  # 確保結果被完全讀取
    return result['order_id'] if result else None
    
def CCalculateTotalAmount(order_id):
    # 計算訂單的總金額
    sql_sum = "SELECT SUM(quantity * price) AS total_amount FROM order_items WHERE order_id = %s"
    cursor.execute(sql_sum, (order_id,))
    result = cursor.fetchone()
    total_amount = result['total_amount'] if result and result['total_amount'] else 0

    # 更新到 orders 表
    sql_update = "UPDATE orders SET total_price = %s WHERE order_id = %s"
    cursor.execute(sql_update, (total_amount, order_id))
    conn.commit()  # 確保更改提交到資料庫
    return total_amount

def CAddress(customer_id):
    sql = "SELECT address FROM customers WHERE customer_id = %s"
    cursor.execute(sql, (customer_id,))
    return cursor.fetchall()   
def CUpdateToList(total_amount,order_id):#更新訂單價格
	sql="update orders set total_price=%s where order_id=%s"
	cursor.execute(sql,(total_amount,order_id,))
	conn.commit()
	return
        
def CDelete(order_id): # 
	sql="delete from orders where order_id=%s"
	cursor.execute(sql,(order_id,))
	conn.commit()
	return
    
def CDelete2(order_id):
	sql="delete from order_items where order_id=%s"
	cursor.execute(sql,(order_id,))
	conn.commit()
	return 

def CCancel(order_id):
    sql="UPDATE orders SET status = 'cancelled' WHERE order_id = %s"
    cursor.execute(sql,(order_id,))
    conn.commit()
    return 
    
def DeleteUnpaidOrders(customer_id):
    # 查詢所有 total_price = 0 的未付款訂單
    sql = "SELECT order_id FROM orders WHERE customer_id = %s AND total_price = 0"
    cursor.execute(sql, (customer_id,))
    unpaid_orders = cursor.fetchall()

    # 如果存在未付款的訂單，進行刪除操作
    if unpaid_orders:
        for order in unpaid_orders:
            order_id = order['order_id']

            # 刪除 order_items 表中對應的記錄
            sql_delete_items = "DELETE FROM order_items WHERE order_id = %s"
            cursor.execute(sql_delete_items, (order_id,))

            # 刪除 orders 表中對應的記錄
            sql_delete_order = "DELETE FROM orders WHERE order_id = %s"
            cursor.execute(sql_delete_order, (order_id,))

        # 提交刪除操作
        conn.commit()   
        
        
def CGetMyOrders(customer_id):
    sql ='''
    SELECT orders.*, 
       stores.store_name, 
       feedback.review_id 
    FROM orders 
    JOIN stores ON orders.store_id = stores.store_id 
    LEFT JOIN feedback ON orders.order_id = feedback.order_id 
    WHERE orders.customer_id = %s
    GROUP BY orders.order_id;
    '''
    param = (customer_id, )
    cursor.execute(sql,param)
    data = cursor.fetchall()
    return data

def CGetOrders(order_id):
    sql = '''
    SELECT orders.*, feedback.review_id
    FROM orders
    LEFT JOIN feedback ON orders.order_id = feedback.order_id
    WHERE orders.order_id = %s;
    '''
    param = (order_id, )
    cursor.execute(sql,param)
    data = cursor.fetchone()
    return data


def CGetOrdersItems(order_id):
    sql = '''SELECT oi.*, mi.item_name 
    FROM order_items oi
    JOIN menu_items mi ON oi.item_id = mi.item_id
    WHERE oi.order_id = %s;
    '''
    param = (order_id, )
    cursor.execute(sql,param)
    data = cursor.fetchall()
    return data

from datetime import datetime

def CUpdateFeedback(order_id, customer_id, rate, comment):
    # 獲取當前時間
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # SQL 查詢：插入評價資料，並記錄當前時間
    sql = """
    INSERT INTO feedback (order_id, customer_id, rating, comment, created_at)
    VALUES (%s, %s, %s, %s, %s);
    """
    param = (order_id, customer_id, rate, comment, created_at)
    
    # 執行 SQL 查詢
    cursor.execute(sql, param)
    
    # 提交變更到資料庫
    conn.commit()
    
    return

# 備餐完成 order
def CCompleteOrder(order_id):
    sql = "UPDATE orders SET status = 'completed' WHERE order_id = %s"
    cursor.execute(sql, (order_id,))
    conn.commit()
    return

    
    
# -------------------------------------------------顧客---------------------------------------------------------------------
















# -------------------------------------------------店家---------------------------------------------------------------------
# Get store info by account and password
def GetStoreInfoByAccount(acc, pwd):
    sql = "SELECT * FROM stores WHERE account = %s AND password = %s;"
    cursor.execute(sql, (acc, pwd))
    return cursor.fetchone()

# Get store info by store ID
def GetStoreInfo(store_id):
    sql = "SELECT * FROM stores WHERE store_id = %s;"
    cursor.execute(sql, (store_id,))
    return cursor.fetchone()

# Get store menu items
def GetMenuItemsByStore(store_id):
    sql = "SELECT item_id, item_name, price, description FROM menu_items WHERE store_id = %s;"
    cursor.execute(sql, (store_id,))
    return cursor.fetchall()

# Get menu item by ID
def GetMenuItemById(item_id):
    sql = "SELECT item_id, item_name, price, description FROM menu_items WHERE item_id = %s;"
    cursor.execute(sql, (item_id,))
    return cursor.fetchone()

# Add a new menu item
def AddMenuItem(store_id, item_name, price, description):
    sql = "INSERT INTO menu_items (store_id, item_name, price, description) VALUES (%s, %s, %s, %s);"
    cursor.execute(sql, (store_id, item_name, price, description))
    conn.commit()

# Update a menu item
def UpdateMenuItem(item_id, item_name, price, description):
    sql = "UPDATE menu_items SET item_name = %s, price = %s, description = %s WHERE item_id = %s;"
    cursor.execute(sql, (item_name, price, description, item_id))
    conn.commit()

# Delete a menu item
def DeleteMenuItem(item_id):
    sql = "DELETE FROM menu_items WHERE item_id = %s;"
    cursor.execute(sql, (item_id,))
    conn.commit()

# -------------------------------------------------訂單---------------------------------------------------------------------
# Get all orders for a store
def GetOrdersByStore(store_id):
    sql = "SELECT order_id, customer_id, created_at, total_price, status FROM orders WHERE store_id = %s;"
    cursor.execute(sql, (store_id,))
    return cursor.fetchall()

# Get order items by order ID
def GetOrderItems(order_id):
    sql = "SELECT oi.order_item_id, oi.item_id, oi.quantity, oi.price, mi.item_name FROM order_items oi JOIN menu_items mi ON oi.item_id = mi.item_id WHERE oi.order_id = %s;"
    cursor.execute(sql, (order_id,))
    return cursor.fetchall()

# Calculate the total amount for an order
def CalculateOrderTotal(order_id):
    sql = "SELECT SUM(quantity * price) AS total_amount FROM order_items WHERE order_id = %s;"
    cursor.execute(sql, (order_id,))
    result = cursor.fetchone()
    return result['total_amount'] if result else 0

# Update order status
def UpdateOrderStatus(order_id, status):
    sql = "UPDATE orders SET status = %s WHERE order_id = %s;"
    cursor.execute(sql, (status, order_id))
    conn.commit()

# Delete an order
def SCancelledOrder(order_id):
    sql = "UPDATE orders SET status = 'cancelled' WHERE order_id = %s"
    cursor.execute(sql, (order_id,))
    conn.commit()
    return

# accept order
def SAcceptOrder(order_id):
    sql = "UPDATE orders SET status = 'preparing' WHERE order_id = %s"
    cursor.execute(sql, (order_id,))
    conn.commit()
    return

# 備餐完成 order
def SCompleteOrder(order_id):
    sql = "UPDATE orders SET status = 'waiting' WHERE order_id = %s"
    cursor.execute(sql, (order_id,))
    conn.commit()
    return

# -------------------------------------------------報表---------------------------------------------------------------------
# Get monthly sales report
def GetMonthlySalesReport(store_id, year, month):
    sql = """SELECT SUM(o.total_price) AS total_sales FROM orders o 
            WHERE o.store_id = %s AND YEAR(o.created_at) = %s AND MONTH(o.created_at) = %s"""
    cursor.execute(sql, (store_id, year, month))
    result = cursor.fetchone()
    return result['total_sales'] if result else 0

# -------------------------------------------------更新店家信息---------------------------------------------------------------------
def UpdateStoreInfo(store_id, store_name, store_address, store_phone):
    sql = """UPDATE stores SET store_name = %s, address = %s, phone_number = %s WHERE store_id = %s"""
    cursor.execute(sql, (store_name, store_address, store_phone, store_id))
    conn.commit()




























# -------------------------------------------------外送員---------------------------------------------------------------------


def GetDeliveryID(user_id):
    sql = "SELECT delivery_id FROM delivery_personnel WHERE user_id = %s;"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    return result['delivery_id'] if result else None

# -------------------------------------------------待接訂單---------------------------------------------------------------------
def GetPendingOrders():
    sql = """
        SELECT 
            u.name, c.customer_id, o.order_id, 
            IFNULL(SUM(oi.quantity * oi.price), 0) AS total_price
        FROM customers c
        JOIN users u ON c.user_id = u.user_id
        JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        WHERE o.status = 'waiting' 
        AND o.delivery_id IS NULL
        GROUP BY o.order_id, u.name, c.customer_id;
    """
    cursor.execute(sql)
    pending_orders = cursor.fetchall()
    if not pending_orders:
        print("No pending orders found.")
    return pending_orders

# -------------------------------------------------已接訂單---------------------------------------------------------------------

def GetAcceptedOrders(delivery_id):
    sql = """
        SELECT 
            u.name, c.customer_id, o.order_id, 
            IFNULL(SUM(oi.quantity * oi.price), 0) AS total_price
        FROM customers c
        JOIN users u ON c.user_id = u.user_id
        JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        WHERE o.status = 'waiting' 
        AND o.delivery_id = %s
        GROUP BY o.order_id, u.name, c.customer_id;
    """
    cursor.execute(sql, (delivery_id,))
    accepted_orders = cursor.fetchall()
    if not accepted_orders:
        print(f"No accepted orders found for delivery ID {delivery_id}.")
    return accepted_orders

# -------------------------------------------------完成的訂單---------------------------------------------------------------------
def GetCompletedOrders(delivery_id):
    sql = """
        SELECT 
            u.name, c.customer_id, o.order_id, 
            IFNULL(SUM(oi.quantity * oi.price), 0) AS total_price
        FROM customers c
        JOIN users u ON c.user_id = u.user_id
        JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        WHERE (o.status = 'completed' or o.status = 'arrival') 
        AND o.delivery_id = %s
        GROUP BY o.order_id, u.name, c.customer_id;
    """
    cursor.execute(sql, (delivery_id,))  # 傳遞 delivery_id 作為參數
    completed_orders = cursor.fetchall()
    if not completed_orders:
        print(f"No completed orders found for delivery ID {delivery_id}.")
    return completed_orders

# -------------------------------------------------訂單詳細資料---------------------------------------------------------------------
def GetOrderDetails(order_id):
    sql = """
        SELECT 
            oi.quantity, 
            oi.price, 
            (oi.quantity * oi.price) AS total_item_price,
            mi.item_name, 
            s.store_name AS store_name, 
            s.address AS store_address, 
            u.name AS customer_name, 
            c.address AS customer_address
        FROM order_items oi
        JOIN menu_items mi ON oi.item_id = mi.item_id
        JOIN orders o ON oi.order_id = o.order_id
        JOIN stores s ON o.store_id = s.store_id
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN users u ON c.user_id = u.user_id
        WHERE oi.order_id = %s;
    """
    cursor.execute(sql, (order_id,))
    order_items = cursor.fetchall()

    # 提取商家與顧客資訊
    if order_items:
        store_info = {
            "store_name": order_items[0].get("store_name", ""),
            "store_address": order_items[0].get("store_address", "")
        }
        customer_info = {
            "customer_name": order_items[0].get("customer_name", ""),
            "customer_address": order_items[0].get("customer_address", "")
        }
    else:
        store_info = {}
        customer_info = {}

    return order_items, store_info, customer_info


# -------------------------------------------------更新訂單狀態---------------------------------------------------------------------
def DUpdateOrderStatus(order_id, status, delivery_id):

    sql = """
        UPDATE orders
        SET status = %s, delivery_id = %s, updated_at = NOW()
        WHERE order_id = %s;
    """
    param = (status, delivery_id, order_id,)
    cursor.execute(sql, param)
    conn.commit()
    return


def GetOrderStatus(order_id):
    sql = "SELECT status FROM orders WHERE order_id = %s;"
    cursor.execute(sql, (order_id,))
    result = cursor.fetchone()
    if result:
        return result['status']
    else:
        return None
# -------------------------------------------------查看訂單評價---------------------------------------------------------------------
def GetFeedbackByOrder(order_id):
    """
    獲取指定訂單的評價
    """
    sql = """
        SELECT 
            f.review_id, f.order_id, f.customer_id, 
            f.target_id, f.target_role, 
            f.rating, f.comment, f.created_at
        FROM feedback f
        WHERE f.order_id = %s;
    """
    cursor.execute(sql, (order_id,))
    feedback = cursor.fetchall()
    
    if not feedback:
        print(f"No feedback found for order ID {order_id}.")
    
    return feedback

# -------------------------------------------------外送員---------------------------------------------------------------------
