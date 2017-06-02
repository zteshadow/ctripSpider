#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, datetime, time, threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#自定义package
from ssutil import ssutil
from ssdriver import ssdriver
from ctriphotel import ctriphotel

lock = threading.Lock()

def thread_process(start, stop, row_list, price_list):
  #print(range(start, stop))
  #print(threading.current_thread().name)
  lowest_price = sys.maxsize

  for i in range(start, stop):
    row = row_list[i]
    #print('start find bed ' + ssutil.time())
    try:
      bed = row.find_element_by_class_name('col3')
    except:
      #print('no col3')
      #logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
      continue

    try:
      breakfirst = row.find_element_by_class_name('col4')
    except:
      #print('no col4')
      #logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
      continue

    try:
      price = row.find_element_by_class_name('base_price')
    except:
      #print('no base_price')
      #logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
      continue

    #print('end find bed ' + ssutil.time())

    bed = bed.text
    breakfirst = breakfirst.text
    price = price.text

    #条件是: 双床, 双早, 找最低价格
    #if bed.find('双') != -1 and breakfirst.find('双') != -1:
    if bed.find('双') != -1:
      real_price = ssutil.price(price)
      if real_price > 0:
        if real_price < lowest_price:
          lowest_price = real_price

  #for循环结束, 查看是否有min最小值, 否则插入0
  lock.acquire()
  price_list.append(lowest_price)
  lock.release()

class ctriphotelengine:
  def __init__(self, url):
    self.url = url
    self.driver = ssdriver()

  def load(self):
    hotelurl = self.url
    driver = self.driver.webdriver()

    driver.get(hotelurl)
    ssdriver.add_cookies(driver, hotelurl)
    try:
      table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "J_RoomListTbl")))
    except:
      ssutil.save_web(driver)
      ssutil.error('timeout to wait table')

  def get_flag_row(self):
    driver = self.driver.webdriver()
    table = driver.find_element_by_id('J_RoomListTbl')
    row_list = table.find_elements_by_tag_name('tr')
    count = len(row_list)
    if count > 2:
      return row_list[1] #取第二条作为table更新的标志行
    else:
      #ssutil.error("no flag row")
      return None

  #返回日期对应的符合要求(双床, 双早)的最低价格, 否则返回0
  def get_price(self, from_date, to_date):
    driver = self.driver.webdriver()
    flag_row = self.get_flag_row()
    if not flag_row:
      return 0

    from_string = from_date.strftime('%Y-%m-%d')
    to_string = to_date.strftime('%Y-%m-%d')
  
    toBox = driver.find_element_by_name('cc_txtCheckOut')
    if toBox != None:
      toBox.clear()
      toBox.send_keys(to_string)
    else:
      ssutil.error('no to box')

    fromBox = driver.find_element_by_name('cc_txtCheckIn')
    if fromBox != None:
      fromBox.clear()
      fromBox.send_keys(from_string)
    else:
      ssutil.error('no from box')

    search_button = driver.find_element_by_id('changeBtn')
    if search_button != None:
      search_button.click()
    else:
      ssutil.error('no search button')
  
    #如果存在, 则等待dom刷新
    if flag_row:
      try:
        WebDriverWait(driver, 20).until(staleness_of(flag_row))
      except:
        print(flag_row.get_attribute('outerHTML'))
        ssutil.error('timeout to refresh table')

    try:
      WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'J_RoomListTbl'))
      )
    except:
      ssutil.save_web(driver)
      ssutil.error('timeout to wait J_RoomListTbl');
  
    table = driver.find_element_by_id('J_RoomListTbl')
    row_list = table.find_elements_by_tag_name('tr')
    count = len(row_list)
    if count > 0:
      pass
    else:
      ssutil.error("no row")

    #print('start loop ' + ssutil.time())
    start = 0
    end = count
    thread_list = []
    price_list = []
    while start < end:
      step = min(5, end - start)
      thread_list.append(threading.Thread(target = thread_process, args = (start, start + step, row_list, price_list, )))
      start += step

    for thread in thread_list:
      thread.start()

    for thread in thread_list:
      thread.join()

    exist = False
    lowest_price = sys.maxsize
    for price in price_list:
      if price < lowest_price:
        exist = True
        lowest_price = price

    if exist:
      print(str(from_date) + ': %d' % lowest_price)
      return lowest_price
    else:
      print(str(from_date) + ' no available room')
      return 0
