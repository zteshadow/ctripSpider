#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#selenium
import time, datetime

from hoteldb import hoteldb
from ssfavorite import ssfavorite
from ctriphotel import ctriphotel
from ctriphotelengine import ctriphotelengine

#计算当前到年底的天数
current_date = datetime.date.today()
day_end = datetime.date(current_date.year, 12, 31)
count = (day_end - current_date).days

hotel_list = ssfavorite.hotels()
for name in hotel_list:
  info = ctriphotel.info(name)
  if not info:
    break

  print(name + ", start: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
  hotel = ctriphotel(name, hoteldb(name))
  engine = ctriphotelengine(info['url'])
  engine.load()

  #从明天开始
  for i in range(1, count):
    day = datetime.date.today() + datetime.timedelta(days=i)
    price = engine.get_price(day, day + datetime.timedelta(days = 1))
    hotel.set_price(day, price)

  print("end: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
