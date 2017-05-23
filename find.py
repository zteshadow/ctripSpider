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

def find_flight(from_city, to_city, count):
  flight = ctripflight(from_city, to_city, flightdb(from_city, to_city))
  engine = ctripflightengine(from_city, to_city)
  engine.load()

  #从明天开始
  for i in range(1, count):
    day = datetime.date.today() + datetime.timedelta(days = i)
    price = engine.get_price(day)
    if price:
      flight.set_price(day, price)

    while not price:
      print('wait 10 secs...')
      time.sleep(10)
      price = get_price(driver, from_city, to_city, day)
      if price:
        flight.set_price(day, price)

#计算当前到年底的天数
current_date = datetime.date.today()
day_end = datetime.date(current_date.year, 12, 31)
count = (day_end - current_date).days
count = 5

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

  #hotel price
  hotel = ctriphotel(name, hoteldb(name))
  hotel_engine = ctriphotelengine(url)
  hotel_engine.load()

  #从明天开始
  for i in range(1, count):
    #day = datetime.date.today() + datetime.timedelta(days=i)
    #price = hotel_engine.get_price(day, day + datetime.timedelta(days = 1))
    #hotel.set_price(day, price)
    pass

  #flight price
  if home != city:
    find_flight(home, city, count)
    find_flight(city, home, count)

  #print("end: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
