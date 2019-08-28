# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
class transform_file_type:
	def __init__(self,root,file_path,file_type,file_path_trans):
		self.root = root.geometry("500x300")
		#设置默认保存路径
		self.file_path = r'C:\Users\jiang_ss\Desktop'
		#设置转换后的文件类型
		self.file_type = 'xlxs'
		#设置转换后的文件保存路径
		self.file_path_trans = r'C:\Users\jiang_ss\Desktop\report.xlxs'
	#页面布局
	def show_windows(self):

		self.ft = tkfont.Font(family='Fixdsys',size=10,weight=tkfont.BOLD,slant=tkfont.ITALIC)
		self.label = Label(self.root,text="Transform tool",font=self.ft)
		self.label.pack()
		self.e = StringVar()
		#带转换的文件输入
		self.show_message = Message(self.root,text="请输入要转换的文件路径").pack()
		self.entry_file_path = Entry(self.root)
		self.show_message_trans = Message(self.root,text='请输入转换后的文件路径').pack()
		self.entry_file_path.pack()
		#转换后的路径输入
		self.entry_file_path_trans = Entry(self.root)
		self.entry_file_path_trans.pack()
		#转换的类型下拉选择

		self.Combox_type = ttk.Combobox(self.root)
		self.Combox_type['values'] = (self.file_type)
		self.Combox_type.current(0)
		self.Combox_type.pack()
		self.button_trans = Button(self.root,text='转换',command=self.transform_file).pack()

		#刷新按钮
		self.button_ref = Button(self.root,text='刷新',command=self.delete_windows).pack()


	def transform_file(self):
		print("执行了转换功能")
		pass

	def delete_windows(self):
		print("执行了刷新功能")
		#root.delete()


root=Tk()
transform = transform_file_type(root,"name","path","var")
transform.show_windows()
root.mainloop()


