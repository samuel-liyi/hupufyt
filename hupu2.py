#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import mechanize
import MySQLdb as mdb
#import re
import sys
reload(sys)
sys.setdefaultencoding("utf8")
#fyt = "http://bbs.hupu.com/fyt-1"
#d = pq(url=fyt)
#pageno=d("div.page").eq(-2).html()+0
pageno = 3                                 
pages = []
res = []
# init browser
br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
response = br.open("http://passport.hupu.com/login")
br.form = list(br.forms())[0] 
name = br.form.find_control("username")
passwd= br.form.find_control("password")
name.value="asterisk"
passwd.value=""
response=br.submit()
#init the mysqldb
con = None
con = mdb.connect('localhost', 'asterisk', 'pass', 'test1',charset="utf8")
cur = con.cursor()
cur.execute("SET NAMES utf8")
cur.execute("create table if not exists test3 (name \
varchar(50), url varchar(40),year int(4),month int(2),day \
int(2),author varchar(20)) \n default character set=utf8")
con.commit()

for i in range(1,100): 
	url="http://bbs.hupu.com/fyt-"+str(i)
	response=br.open(url)
        tmp=pq(response.read())
        for j in range(len(tmp.find('td.p_title'))):
                tmp1=[]
                title='翻译团'
                tmp2=tmp.find('td.p_title').eq(j)
                tmp3=tmp2.find('a')
                if tmp3.find('font'):
                        finished=tmp3.find('font').attr('color')
                        try:
                                
                                if(tmp2.nextAll().eq(0).text().find('-')!=-1):
                                        x=tmp2.nextAll().eq(0).text().split('-') 

                                        day=int(x[len(x)-1])
                                        month=int(x[len(x)-2])
                                        year=int(x[len(x)-3][-4:])
                                        #year,month,day=[1,1,1]
                                        if(finished and finished=='blue'):
                                                tmp1.append(tmp3.find('font').text().split(']')[-1])#strip the [] in the future comment out ,fail to handle examples like [a]b[c]
                                                #tmp1.append(re.search(r"(\[.*\])*(?P<title>.*)(\[.*\])*",tmp3.find('font').text()).group('title'))
                                                tmp4=pq(tmp3[0])
                                                if(tmp4.attr('href').find('fyt-type') != -1):
                                                        tmp4=pq(tmp3[1])
                                                else:
                                                        tmp3=pq(tmp3[0])
                                                tmp1.append("http//bbs.hupu.com"+tmp4.attr('href'))
                                                tmp1+=[year,month,day]
                                                tmp1.append(tmp2.next().find('a').text())
                                                #res.append(tmp1)
                                                #print tmp1[0]+"\t"+tmp1[1]
						cur.execute ("""
						       insert into test3 (name,url,year,month,day,author)
						       values(%s,%s,%s,%s,%s,%s)
						       """, (tmp1[0],tmp1[1],tmp1[2],tmp1[3],tmp1[4],tmp1[5]))
						con.commit()
                        except Exception:
                                pass
                else:
                        next


                        
               # x=tmp2.nextAll().eq(0).text()
                #author=tmp2.nextAll().eq(0).text().substring(0,x.length-10)
                #year=tmp2.nextAll().eq(0).text().substring(0,x.length-10)
                #month=tmp2.nextAll().eq(0).text().substring(x.length-5,2)
                #day=tmp2.nextAll().eq(0).text().substring(x.length-2,2)

#write to mysqldb
#


if con: 
	con.close()

