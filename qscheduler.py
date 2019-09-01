#定时器,定时拉取基金接口中的内容,并将数据进行处理,柱状图显示,且能够将涨跌情况发送至个人邮箱
# -*- coding: UTF-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.offline as of
pyplt = py.offline.plot

class get_fund_data():
	def __init__(self,api):
		self.api=10001

	def split_list(self,datas,n):
		length = len(datas)
		size = length//n +1 if length%n else length//n
		self._datas = []
		for i in range(size):
			start = i*n
			end = (i+1)*n
			self._datas.append(datas[i*n:(i+1)*n])
		return self._datas

	def qscheduler_config(self,times):

		"""
		需要执行的调度策略
		:return:
		"""
		print('here')
		#self.sched = BlockingScheduler()
		#self.sched.add_job(self.scrapy_url, 'interval', minutes=times)

		#self.sched.start()
	def scrapy_url(self,url):
		"""
			数据的爬取
			:return:
		"""
		#天天基金网请求地址
		#self.url = 'http://fund.eastmoney.com'
		#self.url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2018-08-31&ed=2019-08-31&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.26020695171454644'

		r = requests.get(url)
		r.encoding
		r.encoding='utf-8'
		print('soup',r.text )
		return r.text

	def get_fund(self):
		max_jj='5000'
		fromstr = datetime.datetime.now().strftime('%Y-%m-%d')
		url1 = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=#custday&ed=#nowdate&qdii=&tabSubtype=,,,,,&pi=1&pn=#count&dx=1&v=0.26020695171454644'
		url = url1.replace('#count',max_jj)
		url = url.replace('#nowdate',fromstr)

		tostr = (datetime.datetime.now()-datetime.timedelta(days=5*365+1)).strftime('%Y-%m-%d')
		url = url.replace('#custday',tostr)
		print('url',url)
		s = self.scrapy_url(url)
		print('s',s)

		s = s[22:-159]
		s = s.replace('"','')
		s = s.replace('[','')
		s = s.replace(']','')
		lst = s.split(',')
		print(lst)
		lst = self.split_list(lst,25)
		frame = pd.DataFrame(lst,columns=['code','name','py','3','4','jz','day1','week1','month1','month3','month6','year1','year2','year3','year0','yearall','1','2','3','4','5','6','7','8','9'])

		self.frame = frame.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]]
		file_csv = self.frame.to_csv('fund.csv')
		file_xlsx = self.frame.to_excel('fund.xlsx',sheet_name='fund_data')
		print("frame",self.frame)
		#return self.frame
		self.data_operations(self.frame)

	def data_operations(self,frame):
		"""
		对得到的数据进行处理
		:return:
		"""
		frame = self.frame
		# 获得基金代码
		code_data = frame['code'][:10]
		#获得基金的单位净值
		jz_day_data = frame['jz'][:10]
		#获得基金的日增长率
		day1_data = frame['day1'][:10]
		#获得基金的近三月增长率
		month3 = frame['month3'][:10]
		#获得基金的近一年增长率
		year1 = frame['year1'][:10]

		#x轴为基金代码,其他内容为y轴代码(首先制作柱状图)

		data = [go.Bar(x=code_data.values.tolist(),y=jz_day_data.values.tolist())]
		print("code_data", type(code_data.values.tolist()))
		print("jz_day_data", type(jz_day_data.values.tolist()))
		print("code_data", code_data.values.tolist())
		print("jz_day_data", jz_day_data.values.tolist())
		data2 = [go.Bar(x=['1','2','3','4','5'],y=['2','4','6','8','10'])]
		pyplt(data2)
		pyplt(data)



	def send_email(self):
		"""
		将处理的内容发送邮件
		:return:
		"""
		pass

fund_data = get_fund_data("hello")
#routine_get_data = fund_data.qscheduler_config(1)
datas = fund_data.get_fund()

