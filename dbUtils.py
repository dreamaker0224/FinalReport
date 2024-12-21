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

def GetAllItems():
    sql=""  
    cursor.execute(sql)
    return cursor.fetchall()

# -------------------------------------------------登入---------------------------------------------------------------------
def GetLoginInfo(id,pwd):
	sql="select * from users where user_account=%s and user_password=%s"
	param=(id,pwd,)
	cursor.execute(sql,param)
	user = cursor.fetchone()
	if user:
		return user
	return None
# -------------------------------------------------搜尋---------------------------------------------------------------------

# -------------------------------------------------註冊---------------------------------------------------------------------
def AddUser(user_name,account,password):
    sql = "INSERT INTO users (user_name,user_account,user_password) VALUES (%s,%s,%s);"
    param = (user_name,account,password,)
    cursor.execute(sql,param)
    conn.commit()
    return
# -------------------------------------------------註冊---------------------------------------------------------------------

# -------------------------------------------------搜尋---------------------------------------------------------------------
def SearchFromDB(search_input):
    sql = "SELECT * FROM items WHERE item_name LIKE %s;"
    param = (f"%{search_input}%",)
    cursor.execute(sql,param)
    items = cursor.fetchall()
    return items
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
    sql = "SELECT order_item_id,order_id,item_id,quantity,price from order_items where order_id=%s;"
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
    return result['price'] if result else 0        
def CAddToList2(customer_id,created_at, store_id):#建立order
    sql = "INSERT INTO orders (customer_id,created_at, store_id) VALUES (%s, %s, %s)"
    cursor.execute(sql, (customer_id,created_at,store_id,))
    conn.commit()
    return
def CGetLatestOrderId(customer_id):#獲取最新建立的訂單 ID。
    sql = "SELECT MAX(order_id) AS order_id FROM orders where customer_id=%s"
    cursor.execute(sql, (customer_id,))
    result = cursor.fetchone()
    return result['order_id'] if result else None  
    
def CCalculateTotalAmount(order_id):
    sql = "SELECT SUM(quantity * price) AS total_amount FROM order_items WHERE order_id = %s"
    cursor.execute(sql, (order_id,))
    result = cursor.fetchone()  # 獲取單一記錄
    return result['total_amount'] if result and result['total_amount'] else 0
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
	sql="delete from orders where total_price=0 or order_id=%s"
	cursor.execute(sql,(order_id,))
	conn.commit()
	return
    
def CDelete2(order_id):
	sql="delete from order_items where order_id=%s"
	cursor.execute(sql,(order_id,))
	conn.commit()
	return 
# -------------------------------------------------顧客---------------------------------------------------------------------
    