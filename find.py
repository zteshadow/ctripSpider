#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#selenium
import time, datetime

from hoteldb import hoteldb
from ssfavorite import ssfavorite
from ctriphotel import ctriphotel
from ctriphotelengine import ctriphotelengine
from ctripflight import ctripflight
from ctripflightengine import ctripflightengine
from flightdb import flightdb
from ssdb import ssdb

#计算当前到年底的天数
current_date = datetime.date.today()
day_end = datetime.date(current_date.year, 12, 31)
count = (day_end - current_date).days

connectioin = ssdb()
database = connectioin.db()
hotel_list = ssfavorite.hotels()
home = ssfavorite.home()

for name in hotel_list:
  info = ctriphotel.info(name)
  if not info:
    break

  city = info['city']
  url = info['url']
  print(name + ':\n' + city + ', ' + url)
  #print("start: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

  #hotel
  hotel = ctriphotel(name, hoteldb(name, database))
  hotel_engine = ctriphotelengine(url)
  hotel_engine.load()

  go_flight = None
  back_flight = None

  if home != city:
    go_flight = ctripflight(home, city, flightdb(home, city, database))
    go_engine = ctripflightengine(home, city)
    back_flight = ctripflight(city, home, flightdb(city, home, database))
    back_engine = ctripflightengine(city, home)
    go_engine.load()
    back_engine.load()

  #从明天开始
  for i in range(1, count):
    day = datetime.date.today() + datetime.timedelta(days=i)
    if not hotel.find_price(day):
      price = hotel_engine.get_price(day, day + datetime.timedelta(days = 1))
      hotel.set_price(day, price)

    if go_flight:
      if not go_flight.find_price(day):
        price = go_engine.get_price(day)
        if price:
          go_flight.set_price(day, price)

    if back_flight:
      if not back_flight.find_price(day):
        price = back_engine.get_price(day)
        if price:
          back_flight.set_price(day, price)

  #print("end: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
