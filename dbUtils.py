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