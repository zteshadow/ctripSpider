#!/usb/bin/env python3
#-*- coding:utf-8 -*-
# http://flights.ctrip.com/booking/SHA-YNJ-day-1.html?DDate1=2017-05-05

import datetime, sys, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ssdriver import ssdriver
from ssutil import ssutil

from flightdb import flightdb
from ctripflight import ctripflight
from ctripflightengine import ctripflightengine

if __name__ == '__main__':
  from_city = '上海'
  to_city = '哈尔滨'

  data = flightdb(from_city, to_city)
  flight = ctripflight(from_city, to_city, data)
  engine = ctripflightengine(from_city, to_city)
  engine.load()

  #当年年底
  current_date = datetime.date.today()
  day_end = datetime.date(current_date.year, 12, 31)

  #从明天开始
  count = (day_end - current_date).days
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
