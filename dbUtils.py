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
		database="auction"
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
    sql='''
    SELECT I.*, 
       COALESCE(MAX(B.bid_price), 0) AS max_price,
       (SELECT COUNT(*) FROM bids WHERE item_id = I.item_id) AS bid_count
    FROM items I 
    LEFT JOIN bids B ON I.item_id = B.item_id
    GROUP BY I.item_id;
    '''
    cursor.execute(sql)
    return cursor.fetchall()

#login to check account and password
def GetLoginInfo(id,pwd):
	sql="select * from users where user_account=%s and user_password=%s"
	param=(id,pwd,)
	cursor.execute(sql,param)
	user = cursor.fetchone()
	if user:
		return user
	return None

#get individual item and render to it's page
def GetItem(id):
    sql='''
    SELECT I.*, U.user_name, 
       (SELECT COALESCE(MAX(B.bid_price)) FROM bids B WHERE B.item_id = I.item_id) AS max_price
	FROM items I 
	JOIN users U ON I.user_id = U.user_id 
	WHERE I.item_id = %s;
    '''
    param = (id,)
    cursor.execute(sql,param)
    item = cursor.fetchone()
    if item:
        return item
    return None

# 註冊
def AddUser(user_name,account,password):
    sql = "INSERT INTO users (user_name,user_account,user_password) VALUES (%s,%s,%s);"
    param = (user_name,account,password,)
    cursor.execute(sql,param)
    conn.commit()
    return


# 搜尋
def SearchFromDB(search_input):
    sql = "SELECT * FROM items WHERE item_name LIKE %s;"
    param = (f"%{search_input}%",)
    cursor.execute(sql,param)
    items = cursor.fetchall()
    return items
