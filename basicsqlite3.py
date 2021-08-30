# basicsqlite3.py

import sqlite3

#สร้าง database
conn = sqlite3.connect('expanse.sqlite3')
# สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้ได้เลย)
c = conn.cursor()

'''
 ['รหัสรายการ(transectionid) TEXT',
 'วัน-เวลา(Datetime)'TEXT,
 'รายการ(title)'TEXT,
 'ค่าใช้จ่าย(expense)'REAL (float),
 'จำนวน(quantity) INTERGER',
 'รวม(total)'REAL]
 '''
 ############### สร้าง Table ด้วยภาษา SQL ###############
# expenselist คือชื่อ TABLE
c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				transectionid TEXT,
				datetime TEXT,
				title TEXT,
				expense REAL,
				quantity INTEGER,
				total REAL
			)""")
def insert_expense(transectionid,datetime,title,expense,quantity,total): # เอาที่เราสร้างมาใส่
	ID = None
	with conn:
		c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""", # ? ต้องรวม ID = None
			(ID,transectionid,datetime,title,expense,quantity,total)) #ใส่ ID ไปด้วย
		conn.commit() # คือ การบันทึกข้อมูลลงในฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก
		print('Insert Sucess...!')

def show_expense():
	with conn:
		c.execute("SELECT *FROM expenselist")
		expense = c.fetchall() # คำสั่งให้ดึงข้อมูลมา
		print(expense)
	return expense


#transectionid,title,expense,quantity,total
def update_expense(transectionid,title,expense,quantity,total):
	with conn:
		########################## ต้องเหมิอนกับในdatabase ###############
		c.execute("""UPDATE expenselist SET title=?, expense=?, quantity=?, total=? WHERE transectionid=?""",
			([title,expense,quantity,total,transectionid]))
		conn.commit()
		print('Data update')

def delete_expense(transectionid):
	with conn:
		c.execute("DELETE FROM expenselist WHERE transectionid=?",([transectionid])) #ใส่เป็น list
	conn.commit()
	print('Data Deleted')



#########   CRUD #########

#insert_expense('113','วันเสาร์ 2021-08-30','ข้าวสาร',45,2,90) C = creat
#show_expense() # R  = Read
#update_expense('113','GG',20,2,40) U = update
#delete_expense('114') # D = DELETE


######### CRUD #########


#print('sucess')

############### สร้าง Table ด้วยภาษา SQL ###############