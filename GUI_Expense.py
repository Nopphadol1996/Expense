#GUI Basic Expense.py

from tkinter import ttk,messagebox
from tkinter import * # ttk is them of Tk
from datetime import datetime
import csv

##################### DATABASE #########################
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
		# print('Insert Sucess...!')

def show_expense():
	with conn:
		c.execute("SELECT *FROM expenselist")
		expense = c.fetchall() # คำสั่งให้ดึงข้อมูลมา
		# print(expense)
	return expense # มี return  เพราะดึงข้อมูลมาทั้งหมด แล้วนำไปใช้งานต่อ


def update_expense(transectionid,title,expense,quantity,total):
	with conn:
		########################## ต้องเหมิอนกับในdatabase ###############
		c.execute("""UPDATE expenselist SET title=?, expense=?, quantity=?, total=? WHERE transectionid=?""",
			([title,expense,quantity,total,transectionid]))
		conn.commit()
		# print('Data update')

def delete_expense(transectionid):
	with conn:
		c.execute("DELETE FROM expenselist WHERE transectionid=?",([transectionid])) #ใส่เป็น list
	conn.commit()
	# print('Data Deleted')


##################### DATABASE #########################




GUI = Tk()

GUI.title('โปรแกรมบันทึกค่าใช้จ่าย By Nopphadol')
#GUI.geometry('700x670+500+4')

w = 720 # กว้าง
h = 670 # สูง

ws = GUI.winfo_screenwidth() #screen width เช็คความกว้างของหน้า
hs = GUI.winfo_screenheight() #screen height


x = (ws/2) - (w/2) # ws คือความกว้างของหน้าจอทั้งหมด /2 คือครึ่งหนึ่งคือ CENTER
y = (hs/2) - (h/2) - 45

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

# B1 = Button(GUI,text='Hello1')
# B1.pack(ipadx=50,ipady=100) # ติดปุ่มเข้ากับ GUI หลัก ipadx=50 ตามแนวแกนx , ipady=100 ตามแนวแกน y

############################## MENU ###########################
menuber = Menu(GUI)
GUI.config(menu=menuber)

# File menu
filemenu = Menu(menuber,tearoff=0) # tearoff=0 ปิดฟังก์ชั่นย่อย
menuber.add_cascade(label='File',menu=filemenu) # add label file menuber
filemenu.add_command(label='import CSV')
filemenu.add_command(label='Export to googlesheet')

def About():
	messagebox.showinfo('About','นี่คือโปรแกรมสำหรับการเรียนรู้จากลุงวิศวะกร	')
# Help
helpemenu = Menu(menuber,tearoff=0)
menuber.add_cascade(label='Help',menu=helpemenu) # add label file menuber
helpemenu.add_command(label='About',command=About) # เทื่อกดปุ่มให้ไปเรียกฟังก์ชั่น About



# Donate
#donatemenu = Menu(menuber,tearoff=0)
#menuber.add_cascade(label='Donate',menu=donatemenu) # add label file menuber


############################## MENU ###########################

########## สร้าง TAb ###############

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)#,width=400,height=400
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1) # BOTH ขยายทั้งหมด แกนX,Y

########## สร้าง TAb ###############

########## ดึงข้อมูลรูปภาพ .png ##############

icon_t1 = PhotoImage(file='T1_expens.png') # .subsample(2) ย่อขนาดลง2เท่าใช้ได้กับรูป png เท่านั้น
icon_t2 = PhotoImage(file='T2_expens.png')
icon_b1 = PhotoImage(file='button_save.png')

########## ดึงข้อมูลรูปภาพ .png ##############

#### เอารูปภาพมาใส่ในช่อง TAB, compound = 'left' ,top บน ,right = ขวา
Tab.add(T1,text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top') #ใช้ f-string มากำลังหนดระยะข้อความให้เท่ากัน ^ คือเริ่มจาก CENtor <คือ ซ้าย > ขวาสุด
Tab.add(T2,text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')	

F1 = Frame(T1)     # สร้าง Frame เปรียบเสมือนฟิวเจอร์บอร์ด  เอา TABมาใส่ใน Fram
#F1.place(x=100,y=50) # control ระยะ
F1.pack() # ขยายตามหน้าจอวางจากบนจากบนลงล่าง

days = {'Mon':'จันทร์',
		'Tue':'อังคาร์',
		'Wed':'พุธ',
		'Thu':'พฤหัสบดี',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(even=None):

	expense = v_expense.get() # .get ดึงค่ามาจาก v_expense = StringVarผป
	price = v_price.get() # .get ดึงค่ามาจาก v_expense = StringVar
	quantity = v_quantity.get() # .get ดึงค่ามาจาก v_expense = StringVar
	if expense == '':
		messagebox.showwarning('ERROR','กรุณากรอกรายการค่าใช้จ่าย')
		
		return

	elif price =='':

		messagebox.showwarning('ERROR','กรุณากรอกราคา')
		return

	elif quantity =='':

		quantity = 1 #กำหนดค่า Default = 1 ถ้าหาก User ไม่ใส่ 
		#messagebox.showwarning('ERROR','กรุณากรอกจำนวน')
		#return

	try:
		total = float(price)	* float(quantity)
		# print('รายการ: {} ราคา: {} บาท' .format(expense,price))
		# print('จำนวน:{} ชิ้น รวมทั้งหมด {} บาท '.format(quantity,total))

		########## แสดงผลออกทาง GUI ################
		text = 'รายการ: {} ราคา: {} บาท\n'.format(expense,price)
		text = text + 'จำนวน:{} ชิ้น รวมทั้งหมด {} บาท '.format(quantity,total)
		v_result.set(text)

		########## แสดงผลออกทาง GUI ################

		# Clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')


		# บันทึกข้อมูลลง csv
		today = datetime.now().strftime('%a') # เรียก %a คือวันที่ เป็น format สามารถดูได้ใน google https://strftime.org/
		# print(today)
		stamp = datetime.now()
		dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
		transectionid = stamp.strftime('%Y%m%d%H%M%f') # สร้าง transection ID
		dt = days[today] + '-' + dt # แล้วเอา dictionaryมาบวกกับ days[today] ที่ get จาก datetime มา กับ - บวก dt
		
		insert_expense(transectionid,dt,expense,float(price),int(quantity),total)
		'''
		################## อย่าลืมแปลงข้อมูลให้เหมือนกับในdatabase float(price)ในdatabase เป็นจุดทศนิยม แต่ตอนแรก
		price เป็น str
		'''
		with open('savedata.csv','a',encoding='utf-8',newline='') as f:

			# with คือ คำสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' คือ การบันทึกไปเรื่อยๆ เพิ่มข้อมูลจากข้อมูลเก่า แต่ถ้า w  เคลียค่าเก่าแล้วบันทึกใหม่
			# newline='' คือการทำให้ข้อมูลไม่มีบรรทัดว่าง

			fw = csv.writer(f) # สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
			data = [transectionid,dt,expense,price,quantity,total] # เอา Transection ID มาใส่ ใน treeview
			fw.writerow(data)

		# ทำให้เคอร์เซอร์กลับไปตำแหน่งช่องกรอก E1

		E1.focus()
		update_table() # function update_table อยู่ด้านล่าง แต่นำมาใส่ด้านบนได้เพราะ ยังไม่มีการ run


	except:
		print('ERROR')
		#messagebox.showerror('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		messagebox.showwarning('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showinfo('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')

		# Clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')
		E1.focus()


######## ทำให้สามารถกด Enter ได้ ###############


GUI.bind('<Return>',Save) # ต้องเพิ่มใน def Save(event=None)

#############################################

#-------text1--------------
FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New'

############## image ############
Main_icon = PhotoImage(file='icon_money.png')


Mainicon = Label(F1,image=Main_icon)
Mainicon.pack()



############## image ############

L1 = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar() # String() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()

#-------text1--------------


#-------text2--------------

L2 = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar() # String() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1) # Entry คือ ช่องกรอกรับข้อมูลจาก User
E2.pack()

#-------text2-------------

#-------text3--------------

L3 = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar() # String() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1) # Entry คือ ช่องกรอกรับข้อมูลจาก User
E3.pack()

#-------text3--------------


B2 = ttk.Button(F1,text=f'{"Save":>{10}}',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20) # ติดปุ่มเข้ากับ GUI หลัก


################# แสดงผลลัพธฺ์ออกทางหน้าจอ ##################
v_result = StringVar()
v_result.set('--------ผลลัพธ์--------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='green')
# result = Label(F1,textvariable=v_result,font=FONT1,fg='green') ของ Mac os จะใช้รูปแบบนี้
result.pack(pady=20)

################# แสดงผลลัพธฺ์ออกทางหน้าจอ ##################
         
######################### TAB2 #############################

def read_csv():

	with open('savedata.csv',newline='',encoding='utf-8') as f:# function read csv ไม่ต้องใส่ w,a
		fr = csv.reader(f) #  fr = firerader
		data = list(fr)    #  แปลง fr ให้เป็น list เพื่อจะให้เราอ่านออก	
		return data # นำค่าไปใช้งานต่อ หรือทำอีกแบบประกาศตัวแปรเป็น global
		# print(data)
		# print('-------')
		# print(data[0][0])
		# for a,b,c,d,e in data:
		#	print(a,b,c,d,e)

############## Table #############

L2 = ttk.Label(T2,text='รายการค่าใช้จ่าย',font=FONT1,foreground='green')
L2.pack(pady=20)

header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม'] # สร้างHeader
headerwidth = [120,150,170,80,80,80]

resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20) # สร้างTreeview height = 10 คือ จำนวนบรรทัดใน Treeview
resulttable.pack()

for h in header:
	resulttable.heading(h,text=h) # นำ ข้อมูลใน list header ไปใส่ใน Treeview

for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w) # กำหนดระยะ headerwidth เข้ากับ header โดยการ zip
'''
resulttable.insert('','0',value=['จันทร์','น้ำดื่ม',150,2,300])  # ถ้าเป็น 0 อังคาร์จะขึ้นก่อนในตาราง
resulttable.insert('','0',value=['อังคาร์','น้ำดื่ม',150,2,300])  # ถ้าเป็น 0 อังคาร์จะขึ้นก่อนในตาราง

resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',150,2,300])  # ถ้าเป็น end จันทร์จะขึ้นก่อนในตาราง
resulttable.insert('','end',value=['อังคาร์','น้ำดื่ม',150,2,300])  # ถ้าเป็น end อังคาร์จะขึ้นก่อนในตาราง
'''

alltransection = {} # สร้าง Dic เพื่อเก็บข้อมูลที่มาการอ่่านจาก csv เพื่อนำไปลบข้อมูล

def updateCSV():

	with open('savedata.csv','w',newline='',encoding='utf-8') as f:# function read csv ไม่ต้องใส่ w,a
		fw = csv.writer(f) #  fw = filewriter

		# เพื่อนำไปลบข้อมูลตรียมข้อจาก transection ให้กลายเป็น list
		data = list(alltransection.values())
		fw.writerows(data) # multiple line from nested list [[],[],[]] list ซ้อน list
		print('Table was update ')

def UpdateSQL():
	data = list(alltransection.values())
	#print('UPDATE SQL:',data[0]) # โชว์แค่ 1 record
	for d in data:

		# transectionid,title,expense,quantity,total
		# d[0] = 202108300144088343,d[1]= จันทร์-2021-08-30 01:44:52,d[2]มะม่วง,d[3]=30,d[4]=2,d[5]60.0
		####### เราต้องการเปลี่ยนแค่ d0,2,3,4,5
		update_expense(d[0],d[2],d[3],d[4],d[5]) #ไปเรียก function update_expense มีจำนวน 6 ฟิว ใน database 


def DeleteRecord(event=None): # สร้าง Function สำหรับ Delete ข้อมูล

	check = messagebox.askyesno('Confirm','คุณต้องการลบข้อมูลหรือไม่ ?') # สร้าง pop up yes No เพื่อที่จะลบ แล้วใช้ if else กำหนดเงื่อนไข
	# print('Yes/No: ',check)
	try:

		if check == True:

			select = resulttable.selection() # ไปเรียกฟังก์ชั่น พิเศษที่ คลิกใน Treeview
			# print(select)
			data = resulttable.item(select) # ดึง Item ที่เราเลือกมา จากตาราง (((ถ้าอยากได้มากว่า 1 รายการให้ Run for lop)))
			data = data['values'] # ไปดึง values ออกมา ((dic))
			transectionid = data[0] # ให้ transectionid = รหัสรายการคือ data[0]
			# print(transectionid)
			# print(type(transectionid))
			del alltransection[str(transectionid)] # ลบข้อมูลที่อยู่ใน Dic Delete data ที่อยู่ใน dic ต้องแปลจาก Int > str
			# print(alltransection)

			######### ของ CSV #############

			# updateCSV() # หลังจากการ ลบ ให้ Update CSV

			######### ของ CSV #############

			delete_expense(str(transectionid)) ### Delete in DB

			update_table() # Update data ใหม่่ทั้งหมดอัพโนมัติ

		else:

			pass
			# print('Cancel')
	except:

		#print('กรุณาเลือกข้อมูลที่จะลบ')
		messagebox.showerror('ERROR','กรุณาเลือกข้อมูลที่จะลบ')

BDelete = ttk.Button(T2,text='Delete',command=DeleteRecord) # สร้างปุ่มสำหรับ Delete ข้อมูล
BDelete.place(x=50,y=550)

resulttable.bind('<Delete>',DeleteRecord) # กดปุ่ม Delete เพื่อลบข้อมูล


def update_table():
	resulttable.delete(*resulttable.get_children()) # clear ข้อมูลเก่าแล้ว update ข้อมูลใหม่

	# for c in resulttable.get_children(): เหมือนกันกับ *
	#	resulttable.delete(c)
	try:

		data = show_expense()  # read_csv() เปลี่ยนไปใช้ database แทน csvs
		#print('DATA',data)

		for d in data:
			################ csv ################
			#resulttable.insert('',0,value=d) # บันทึกล่าสุดจะอยู่ด้านบน
			#resulttable.insert('','end',value=d) # บันทึกล่าสุดจะอยู่ด้านล่าง เมื่อไปใช้ database แทน มันจะดึง indexมาด้วย เราต้องช้ามโดยการ[1:]
			#alltransection[d[0]] = d # d[0] =  เก็บ transectionid เป็น Dic, เมื่อไปใช้ database แทน มันจะดึง indexมาด้วย เราต้องช้ามโดยการ[1:]
			
			################ csv ################
			
			####### ใช้ databasec แทน #########
			alltransection[d[1]] = d[1:] # d[0] =  เก็บ transectionid เป็น Dic, เมื่อไปใช้ database แทน มันจะดึง indexมาด้วย เราต้องช้ามโดยการ[1:]
			resulttable.insert('','end',value=d[1:]) # บันทึกล่าสุดจะอยู่ด้านล่าง เมื่อไปใช้ database แทน มันจะดึง indexมาด้วย เราต้องช้ามโดยการ[1:]
			
			####### ใช้ databasec แทน #########
		#print(alltransection)
	except Exception as e:
		print('No File: ',e)

##################### Right Click Menu ###########################
def EditRecord():
################## ควรจะเเปลี่ยนชื่อ ########### ในตารางแก้ไขเดี๋ยวมาทำ#############
	POPUP = Toplevel()
	#POPUP.geometry('500x300')
	POPUP.title('Edit Record')
	w = 500 # กว้าง
	h = 300 # สูง

	ws = POPUP.winfo_screenwidth() #screen width เช็คความกว้างของหน้า
	hs = POPUP.winfo_screenheight() #screen height


	x = (ws/2) - (w/2) # ws คือความกว้างของหน้าจอทั้งหมด /2 คือครึ่งหนึ่งคือ CENTER
	y = (hs/2) - (h/2) - 45

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

	L1 = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
	v_expense = StringVar() # String() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
	E1.pack()

	#-------text1--------------


	#-------text2--------------

	L2 = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
	v_price = StringVar() # String() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1) # Entry คือ ช่องกรอกรับข้อมูลจาก User
	E2.pack()

	#-------text2-------------

	#-------text3--------------

	L3 = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
	v_quantity = StringVar() # String() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1) # Entry คือ ช่องกรอกรับข้อมูลจาก User
	E3.pack()

	#-------text3--------------
	def Edit():

		# print(transectionid)
		# print(alltransection)
		olddata = alltransection[str(transectionid)] ########## อย่าลืมแปลงเป็น str เพราะเวลา get ออกมาเป็นตัวเลข###########
		# print('OLD',olddata)
		v1 = v_expense.get() #### กำหนดตัวแปร v1 เพื่อที่จะนำไปคำนวนใหม่
		v2 = float(v_price.get()) #### กำหนดตัวแปร v2 เพื่อที่จะนำไปคำนวนใหม่
		v3 = float(v_quantity.get()) #### กำหนดตัวแปร v3 เพื่อที่จะนำไปคำนวนใหม่
		total = v2 * v3
		newdata = [olddata[0],olddata[1],v1,v2,v3,total] # ตำแหน่งที่ 0,1 เราไม่ต้องแก้ไข
		########## อย่าลืมแปลงเป็น str เพราะเวลา get ออกมาเป็นตัวเลข###########
		alltransection[str(transectionid)] = newdata # ให้ alltransection[transectionid] ให้มีค่า = newdata ใหม่ที่ทำการแก้ไขแล้ว
		
		#### ของ csv ####
		#updateCSV()
		#### ของ csv ####
		UpdateSQL()
		update_table()
		POPUP.destroy() ########### สั่งปิด POPUP ###################	

	B2 = ttk.Button(POPUP,text=f'{"Save":>{10}}',image=icon_b1,compound='left',command=Edit) #### ให้ไปเรียก function Edit
	B2.pack(ipadx=50,ipady=20,pady=20)

	############# Get data in selected record ########### เพื่อที่จะแก้ไข
	try:

		select = resulttable.selection() # ไปเรียกฟังก์ชั่น พิเศษที่ คลิกใน Treeview
		# print(select)
		data = resulttable.item(select) # ดึง Item ที่เราเลือกมา จากตาราง (((ถ้าอยากได้มากว่า 1 รายการให้ Run for lop)))
		data = data['values'] # ไปดึง values ออกมา ((dic))
		# print(data)
		transectionid = data[0] # ให้ transectionid = รหัสรายการคือ data[0]

		############## ดึงข้อมูลเก่ามาใส่ใน ช่องกรอกที่เราจะแก้ไข ######################
		v_expense.set(data[2])
		v_price.set(data[3])
		v_quantity.set(data[4])
	except:

		POPUP.destroy()
		messagebox.showerror('ERROR','กรุณาเลือกรายการ')
	POPUP.mainloop()

rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord) # ไปเรียก function Delete

def menupopup(event): # ใส่ Event ด้วยจ๊ะ
	#if left_click == True: ######### เดี๋ยวมาทำทีหลัง ทำเอง คลิก ซ้ายเลือกก่อนที่จะแสดง POP UP

	# print(event.x_root,event.y_root) # บอกตำแหน่งของแนวแกน x y 
	rightclick.post(event.x_root,event.y_root) # บอกตำแหน่งของแนวแกน x y  ที่คลิกใน resulttable

resulttable.bind('<Button-3>',menupopup) # มีการคลิกขวาที่ตาราง resulttable ให้แสดงข้อมูลในfunction menupopup , Button-3 คือคลิก ขวา

##################### Right Click Menu ###########################

''''
left_click = False

def leftclick(event): 
	global left_click
	left_click = True   ######### เดี๋ยวมาทำทีหลัง ทำเอง คลิก ซ้ายเลือกก่อนที่จะแสดง POP UP
	print(left_click)

resulttable.bind('<Button-1>',leftclick)
'''

update_table()
#UpdateSQL()
GUI.bind('<Tab>',lambda x:E2.focus())
GUI.mainloop()
