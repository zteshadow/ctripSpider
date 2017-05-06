#!/usb/bin/env python3
#-*- coding:utf-8 -*-
# http://flights.ctrip.com/booking/SHA-YNJ-day-1.html?DDate1=2017-05-05

import datetime, sys, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ssdata import ssdata
from ssdriver import ssdriver
from ssutil import ssutil

#td[0-8], [0]: 航空公司, 航班和机型, [1]:出发时间和机场, [3]:到达时间和机场, [6]:价格
#返回元组(航班, 价格)
def parse_data(table):
  lowest_price = sys.maxsize
  airline = None
  lowest_table = None

  table_list = table.find_elements_by_tag_name('table')
  for table in table_list:
    element = table.find_element_by_class_name('base_price02')
    price = ssutil.price(element.text)
    if price < lowest_price:
      lowest_price = price
      lowest_table = table

  if lowest_table:
    element = lowest_table.find_element_by_class_name('flight_logo')
    airline = element.text

  return (airline, lowest_price)

#'上海', '三亚', 2017-05-05
def get_price(from_city, to_city, day):
  driver_util = ssdriver()
  driver = driver_util.webdriver()
  url = "http://flights.ctrip.com/booking/" + from_city + "-" + to_city + "-day-1.html?DDate1=";
  url += day.strftime('%Y-%m-%d')
  print(url)
  
  driver.get(url)
  try:
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "J_flightlist2")))
  except:
    ssutil.error('timeout to wait table')

  item = parse_data(table)
  if item[0]:
    print("name: " + item[0] + " price: %d" % item[1])
    return item[1]
  else:
    return None

if __name__ == '__main__':
  bddata = ssdata()

  from_city = bddata.find_city('上海')
  to_city = bddata.find_city('哈尔滨')

  current_date = datetime.date.today()
  day_end = datetime.date(current_date.year, 12, 31)
  count = (day_end - current_date).days
  for i in range(0, count):
    day = datetime.date.today() + datetime.timedelta(days=i)
    price = get_price(from_city, to_city, day)
    while not price:
      print('wait 3 secs...')
      time.sleep(3)
      price = get_price(from_city, to_city, day)

