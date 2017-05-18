#!/usb/bin/env python3
#-*- coding:utf-8 -*-
# http://flights.ctrip.com/booking/SHA-YNJ-day-1.html?DDate1=2017-05-05

import datetime, time

from ssfavorite import ssfavorite
from flightdb import flightdb
from ctripflight import ctripflight
from ctripflightengine import ctripflightengine

if __name__ == '__main__':
  
  #当年到年底的天数
  current_date = datetime.date.today()
  day_end = datetime.date(current_date.year, 12, 31)
  count = (day_end - current_date).days

  flight_list = ssfavorite.flights()
  for from_city, to_city in flight_list:
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
