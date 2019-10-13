# -*- coding: UTF-8 -*-
import requests
import os
import re
import pandas as pd
import numpy as np
import json
import re
from datetime import datetime
import plotly.graph_objs as go
import plotly as py
pyplt = py.offline.plot

def get_url_content(url):
        url = url
        r = requests.get(url)
        r.encoding
        r.encoding='utf-8'
        return r.text

def get_fund_data(url,file_name):
        #需要进行行转列输出
        data = get_url_content(url)  
        p2 = re.compile(r'[[](.*)[]]', re.S)  #贪婪匹配
        fund_datas_list = re.findall(p2, data)#匹配得到一个包含所有信息内容的list
        fund_datas_string = fund_datas_list[0]#将list中的内容string输出
        fund_datas_lists = fund_datas_string.split('\"')#将string中每一个基金的内容变成list
        columns=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']
        columns={'0':['基金代码','基金名称','基金编号','查询日期','单位净值','日增长率','近一周','近一月','近三月','近六月','近一年','近两年','近三年','今年来','成立来','自定义','手续费','','','','','','','','']}
        datas_dict={}
        datas_dict.update(b=columns["0"])
        datas_list=[]
        for datas in fund_datas_lists[1:-1]:
                if datas == "" or datas =="\"" or datas == ",":
                        continue
                else:
                        datas_string = re.sub(',','\",\"',datas).split(',')
                        datas_list.append(datas_string)

        for data_key in range(len(datas_list)):
                datas_dict[data_key]=datas_list[data_key]

        #将得到的每个基金数据中相同位置的内容取出，拼成全新的datas_dict
        fund_data_item_dict = {}
        fund_data_item_jz = [] #基金净值
        fund_data_item_code =[] #基金代码
        fund_data_item_pg = [] #基金日增长
        fund_data_item_name = [] #基金名称
        fund_data_item_date = [] #时间
        for fund_data_item in datas_list:
                fund_data_item_jz.append(fund_data_item[4])  #得到所有基金净值的数据，组成datas_list
                fund_data_item_code.append(fund_data_item[0])  #得到所有基金代码
                fund_data_item_pg.append(fund_data_item[5])
                fund_data_item_name.append(fund_data_item[1])
                fund_data_item_date.append(fund_data_item[3])
        fund_data_item_dict['基金代码'] = fund_data_item_code
        fund_data_item_dict['基金名称'] = fund_data_item_name
        fund_data_item_dict['单位净值'] = fund_data_item_jz
        fund_data_item_dict['基金日增长'] = fund_data_item_pg
        fund_data_item_dict['日期'] = fund_data_item_date
                
                
        ft = pd.DataFrame(datas_dict)
        ft.to_excel('my.xls',index=0)
        dt = pd.DataFrame(fund_data_item_dict)
        dt.to_excel(file_name,index=0)
        return dt  #返回表格内容
   
def get_data_config(endday,startday):
#配置查询基金的方式，时间等，配置的方式通过url中的传参设置请求  
        ed=endday
        sd=startday
        url='http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2019-09-03&ed=2019-09-03&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.9656184483914523'
        url_new_1 = re.sub('sd=2019-09-03','sd='+sd,url)
        url_new_2 = re.sub('ed=2019-09-03','ed='+ed,url_new_1)
        return url_new_2
#将得到的数据进行分析处理

def  plot_figure(frame):
        # 获得基金代码
        code_data = frame['基金名称'][:10]
        #获得基金的单位净值
        jz_day_data = frame['单位净值'][:10]
        #获得基金的日增长率
        day_data = frame['基金日增长'][:10]
        data = [go.Bar(x=code_data.values.tolist(),y=jz_day_data.values.tolist())]
        #print(data)
        pyplt(data)
        return data


time = datetime.now()
hms = time.strftime('%Y%m%d%S%f')
endtime = time.strftime('%Y-%m-%d')
data_config = get_data_config(endtime,endtime)
t = get_fund_data(data_config,hms+'.xls')
print(t)
figure = plot_figure(t)
