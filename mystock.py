from tkinter import *
from tkinter import filedialog
from tkinter import ttk, messagebox
import mysql.connector

##################### UX-UI ######################################################
# Color
bg='#323333' #ตั้งค่า default สีพื้นหลังได้
fg='#f2f2f2' #ตั้งสีเพิ่มได้

# Font
f1 = ('Browalia New',30)
f2 = (None,12)
f3 = ('Angsana New', 14)


GUI = Tk()
GUI.geometry('1000x600+300+100') #กว้างxยาว+ตำแหน่งที่เดสท็อบแนวนอน+ตำแหน่งที่เดสท็อบแนวตั้ง
# GUI.configure(background=bg) #นำ default สีพื้นหลังมาใช้
# GUI.state('zoomed')
GUI.title('My Stock')


itemCode = StringVar()
itemName = StringVar()
itemQuantity = StringVar()
itemUnitPrice = StringVar()
itemLocation = StringVar()
status = StringVar()


Label(GUI,text='item_code: ').grid(row=0,column=0)
Label(GUI,text='item_name: ').grid(row=1,column=0)
Label(GUI,text='item_quantity: ').grid(row=2,column=0)
Label(GUI,text='item_unitprice: ').grid(row=3,column=0)
Label(GUI,text='item_location: ').grid(row=4,column=0)


Entry(GUI,textvariable=itemCode).grid(row=0,column=1)
Entry(GUI,textvariable=itemName).grid(row=1,column=1)
Entry(GUI,textvariable=itemQuantity).grid(row=2,column=1)
Entry(GUI,textvariable=itemUnitPrice).grid(row=3,column=1)
Entry(GUI,textvariable=itemLocation).grid(row=4,column=1)


##################### DATABASE ###################################################
import sqlite3 as db

conn = db.connect('mystock.db')
c = conn.cursor()

#create table ตรงตัวแปรสุดท้ายประเภทฟิลด์ของ honor หลัง TEXT จุลภาค ถ้าใส่หลังสุด error
c.execute("""CREATE TABLE IF NOT EXISTS mystock (
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		item_code TEXT,
		item_name TEXT,
		item_quantity INTEGER,
		item_unitprice DECIMAL,
		item_location TEXT
		)""")
c.close()

def insert_mystock():
	conn = db.connect('mystock.db')
	c = conn.cursor()
	c.execute("INSERT into mystock (item_code, item_name, item_quantity, item_unitprice, item_location) VALUES (?,?,?,?,?)",(itemCode.get(),itemName.get(),itemQuantity.get(),itemUnitPrice.get(),itemLocation.get()))
	c.close()
	conn.commit()
	conn.close()
	status.set('Data add successfully')

	view_mystock()


def view_mystock():
	global table
	header = ['ID','รหัสไอเทม','ชื่อไอเทม','จำนวน','ราคาต่อหน่วย','สถานที่จัดเก็บ']
	hwidth = [100,100,200,100,100,100]
	table = ttk.Treeview(GUI, columns=header, show='headings',height=20)
	table.place(x=50,y=150)

	for hd,w in zip(header,hwidth):
		table.column(hd,width=w)
		table.heading(hd,text=hd)

	conn = db.connect('mystock.db')
	c = conn.cursor()
	c.execute("SELECT * from mystock")
	list0 = c.fetchall()
	c.close()
	conn.close()

	for row in list0:
		table.insert('',0,value=row)

	itemCode.set('')
	itemName.set('')
	itemQuantity.set('')
	itemUnitPrice.set('')
	itemLocation.set('')


def edit(event):
	select = table.selection()[0]
	data = table.item(select)['values']

	update_data = Toplevel()
	update_data.title('edit data')
	update_data.geometry('300x200+500+300')

	ID=['values'][0]
	newitemCode = StringVar()
	newitemName = StringVar()
	newitemQuantity = StringVar()
	newitemUnitPrice = StringVar()
	newitemLocation = StringVar()
	

	Label(update_data,text='item_code: ').grid(row=1,column=0)
	Label(update_data,text='item_name: ').grid(row=2,column=0)
	Label(update_data,text='item_quantity: ').grid(row=3,column=0)
	Label(update_data,text='item_unitprice: ').grid(row=4,column=0)
	Label(update_data,text='item_location: ').grid(row=5,column=0)


	Entry(update_data,textvariable=newitemCode).grid(row=1,column=1)
	Entry(update_data,textvariable=newitemName).grid(row=2,column=1)
	Entry(update_data,textvariable=newitemQuantity).grid(row=3,column=1)
	Entry(update_data,textvariable=newitemUnitPrice).grid(row=4,column=1)
	Entry(update_data,textvariable=newitemLocation).grid(row=5,column=1)


	newitemCode.set(data[1])
	newitemName.set(data[2])
	newitemQuantity.set(data[3])
	newitemUnitPrice.set(data[4])
	newitemLocation.set(data[5])

    # ฟังก์ชันสำหรับอัพเดทข้อมูลในฐานข้อมูล
	def edi_data():
	    new_values = [newitemCode.get(),
	    			  newitemName.get(),
	    			  newitemQuantity.get(),
	    			  newitemUnitPrice.get(),
	    			  newitemLocation.get()
	    			 ]
	    print(new_values)
	    conn = db.connect('mystock.db')
	    c = conn.cursor()
	    c.execute("UPDATE mystock SET item_code=?, item_name=?, item_quantity=?, item_unitprice=?, item_location=? WHERE ID=?", (newitemCode.get(), newitemName.get(), newitemQuantity.get(), newitemUnitPrice.get(), newitemLocation.get(), data[0]))
	    conn.commit()
	    conn.close()
	    view_mystock()


    # ปุ่มสำหรับบันทึกการแก้ไข
	Button(update_data, text="Update",command=edi_data).grid(row=6, columnspan=2)

GUI.bind('<Double-1>', edit)
# GUI.bind('<Double-1>', update_mystock)

# สร้างฟังก์ชันลบข้อมูล
def delete_mystock(event):
	global table

	select = table.selection()[0]
	data = table.item(select)['values']

	conn = db.connect('mystock.db')
	c = conn.cursor()
	c.execute("DELETE from mystock WHERE ID=?",(data[0],))
	conn.commit()
	conn.close()
	status.set('Delete data successfully')
	view_mystock()

###################################################################################
view_mystock()
Label(GUI,text='',textvariable=status).grid(row=6,column=2)
Button(GUI,text='Submit',command=insert_mystock).grid(row=5,columnspan=2)
GUI.bind('<Delete>',delete_mystock)

GUI.mainloop()