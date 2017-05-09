#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#selenium
import os, time, datetime, sys

import pymysql, logging

from ssdata import ssdata
from ssdriver import ssdriver
from ssutil import ssutil
from ctriphotel import ctriphotel
from ctriphotelengine import ctriphotelengine

name = '上海大厦'
print(name + ", start: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

hotel = ctriphotel(name)
  
engine = ctriphotelengine(name)
engine.load()

#当前到年底
current_date = datetime.date.today()
day_end = datetime.date(current_date.year, 12, 31)
count = (day_end - current_date).days
for i in range(1, count):
  start = datetime.date.today() + datetime.timedelta(days=i)
  end = start + datetime.timedelta(days = 1)
  price = engine.get_price(start, end)
  hotel.set_price(start, end, price)

print("end: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
