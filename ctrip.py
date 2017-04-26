#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#selenium
import os
import time
import datetime
import sys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
#
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from bs4 import BeautifulSoup

import json
import pymysql

#user defined
from ssroom import *
import logging

db = None
cursor = None

def ss_db_init():
  global db
  db = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                             user='root', passwd='Qwertyui123456', db='mysql')
  global cursor
  cursor = db.cursor()
  cursor.execute("SET sql_notes = 0; ")
  cursor.execute("create database IF NOT EXISTS ctrip")
  cursor.execute("USE ctrip")

  cursor.execute("SET sql_notes = 0; ")
  cursor.execute("create table IF NOT EXISTS lowest_price_eachday (id DATE, search_date DATE, price INT, primary key(id, search_date));")
  cursor.execute("SET sql_notes = 1; ")

def ss_db_add_new_item(start, end, price):
  data = "insert into lowest_price_eachday (id, search_date, price) values('"
  data += str(start)
  data += "', '"
  data += str(end)
  data += "', %d)" % price
  #print(data)
  cursor.execute(data)
  db.commit()

def ss_db_deinit():
  cursor.close()
  db.close()

def ss_show_error(msg):
  print(msg)
  exit(1)

def ss_get_content(url):
  try:
    html = urlopen(url)
  except HTTPError as e:
    print(e)
    return None

  return html.read()

def ss_get_title(url):
  try:
    html = urlopen(url)
  except HTTPError as e:
    print(e)
    return None

  try:
    bsObj = BeautifulSoup(html.read(), "html.parser")
    title = bsObj.title
    nameList = bsObj.findAll("input", {"id":"_allSearchKeyword"})
    for name in nameList:
      print(name)
      print(name.get_text())

  except AttributeError as e:
    return None
  return title

def ss_get_url_for_hotel(keyword):
  #keyword = '上海大厦';
  #keyword = urllib.parse.quote(keyword)
  keyword = quote(keyword)
  url = "http://m.ctrip.com/restapi/h5api/searchapp/search?action=autocomplete&source=globalonline&keyword=%s"%keyword
  #print(url)
  #print("http://m.ctrip.com/restapi/h5api/searchapp/search?action=autocomplete&source=globalonline&keyword=%s"%keyword)

  content = ss_get_content(url)
  if content == None:
    print("content not found")
    exit(0)

  jsonData = json.loads(content.decode("utf-8"))
  #print(s)
  hotelList = None;
  try:
    hotelList = jsonData['data']
    #print(jsonData['data'])
  except:
    ss_show_error("--------json struction is changed-----")

  hotelURL = None;
  for hotel in hotelList:
    try:
      name = hotel['word']
      if (name == '上海大厦'):
        print(hotel)
        try:
          hotelURL = hotel['url']
        except:
          ss_show_error("--------json struction is changed-----")
    except:
      ss_show_error("--------json struction is changed-----")

  return hotelURL

def ss_get_element_text_by_class(element, class_name):
  try:
    item = element.find_element_by_class_name(class_name)
    if item:
      return item.text
    else:
      return None
  except:
    print("no class ".class_name)
  finally:
    return None

def ss_get_flag_row(driver):
  table = driver.find_element_by_id('J_RoomListTbl')
  row_list = table.find_elements_by_tag_name('tr')
  count = len(row_list)
  if count > 2:
    return row_list[1] #取第二条作为table更新的标志行
  else:
    ss_show_error("no flag row")

def ss_get_price_for_date(driver, from_date, to_date):
  lowest_price = sys.maxsize
  lowest_bed = 'no'
  lowest_breakfirst = 'no'

  flag_row = ss_get_flag_row(driver)

  from_string = from_date.strftime('%Y-%m-%d')
  to_string = to_date.strftime('%Y-%m-%d')
  
  toBox = driver.find_element_by_name('cc_txtCheckOut')
  if toBox != None:
    toBox.clear()
    toBox.send_keys(to_string)
  else:
    ss_show_error('no to box')

  fromBox = driver.find_element_by_name('cc_txtCheckIn')
  if fromBox != None:
    fromBox.clear()
    fromBox.send_keys(from_string)
  else:
    ss_show_error('no from box')

  search_button = driver.find_element_by_id('changeBtn')
  if search_button != None:
    search_button.click()
  else:
    ss_show_error('no search button')
  
  #如果存在, 则等待dom刷新
  if flag_row:
    try:
      WebDriverWait(driver, 20).until(staleness_of(flag_row))
    except:
      print(flag_row.get_attribute('outerHTML'))
      ss_show_error('timeout to refresh table')

  WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'J_RoomListTbl'))
  )
  
  table = driver.find_element_by_id('J_RoomListTbl')
  row_list = table.find_elements_by_tag_name('tr')
  count = len(row_list)
  if count > 0:
    print("get row ok: %d" % count)
  else:
    ss_show_error("no row")

  for row in row_list:
    try:
      bed = row.find_element_by_class_name('col3')
    except:
      logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
      continue

    try:
      breakfirst = row.find_element_by_class_name('col4')
    except:
      logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
      continue

    try:
      price = row.find_element_by_class_name('base_price')
    except:
      logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
      continue

    bed = bed.text
    breakfirst = breakfirst.text
    price = price.text
    #条件是: 双床, 双早, 找最低价格
    if bed.find('双') != -1 and breakfirst.find('双') != -1:
      #print('bed: ' + bed + " breakfirst: " + breakfirst + " price: " + price)
      price = price.strip()
      while price.isalnum() == False and len(price) >= 2:
        price = price[1:]

    if price.isalnum():
      try:
        real_price = int(price)
        if real_price > 0 and real_price < lowest_price:
          lowest_price = real_price
          lowest_bed = bed
          lowest_breakfirst = breakfirst
      except:
        #print("invalide price: " + price)
        pass

  print("from: " + str(from_date) + " to: " + str(to_date) + " bed: " + lowest_bed + " breakfirst: " + lowest_breakfirst + " lowest_price: %d" % lowest_price)
  return lowest_price

def ss_retrieve_all_price_for_hotel(hotelurl):
  ss_db_init()
  dcap = dict(DesiredCapabilities.PHANTOMJS)
  dcap["phantomjs.page.settings.userAgent"] = (
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
  )
  dcap["phantomjs.page.settings.loadImages"] = False
  phantomjs_path = os.environ.get('PHANTOMJSPATH')
  if phantomjs_path:
    pass
  else:
    print("phantomjs needed, set environment for 'PHANTOMJSPATH'")
    exit(1)

  driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)
  print(hotelurl)
  driver.get(hotelurl)
  try:
    table = EC.presence_of_element_located((By.ID, 'J_RoomListTbl'))
    WebDriverWait(driver, 30).until(table)
  except:
    if os.path.isfile('./test.png'):
      os.remove('./test.png')
    driver.save_screenshot("test.png")
    ss_show_error('timeout to wait table')
    driver.quit()

  #当前到年底
  current_date = datetime.date.today()
  day_end = datetime.date(current_date.year, 12, 31)
  count = (day_end - current_date).days
  for i in range(0, count):
    start = datetime.date.today() + datetime.timedelta(days=i)
    end = start + datetime.timedelta(days=1)
    #print("start: "+start.strftime('%Y-%m-%d')+" end: "+end.strftime('%Y-%m-%d'))
    #tomorrow_string = tomorrow.strftime('%Y-%m-%d')
    price = ss_get_price_for_date(driver, start, end)
    ss_db_add_new_item(start, current_date, price)
  driver.quit()
  ss_db_deinit()

# 通过下面的方式进行简单配置输出方式与日志级别
if os.path.isfile('./logger.log'):
  os.remove('./logger.log')
logging.basicConfig(filename='logger.log', level=logging.INFO)

print("start: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
url = ss_get_url_for_hotel('上海大厦')
ss_retrieve_all_price_for_hotel(url)
print("end: " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

