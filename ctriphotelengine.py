#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, datetime

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

class ctriphotelengine:
  def __init__(self, url):
    self.url = url
    self.driver = ssdriver()

  def __del__(self):
    pass

  def load(self):
    hotelurl = self.url
    driver = self.driver.webdriver()
    #print(hotelurl)
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
      ssutil.error("no flag row")

  def get_price(self, from_date, to_date):
    driver = self.driver.webdriver()
    lowest_price = sys.maxsize
    lowest_bed = 'no'
    lowest_breakfirst = 'no'

    flag_row = self.get_flag_row()

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

    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'J_RoomListTbl'))
    )
  
    table = driver.find_element_by_id('J_RoomListTbl')
    row_list = table.find_elements_by_tag_name('tr')
    count = len(row_list)
    if count > 0:
      print("get row ok: %d" % count)
    else:
      ssutil.error("no row")

    for row in row_list:
      try:
        bed = row.find_element_by_class_name('col3')
      except:
        #logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
        continue

      try:
        breakfirst = row.find_element_by_class_name('col4')
      except:
        #logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
        continue

      try:
        price = row.find_element_by_class_name('base_price')
      except:
        #logging.info("\n/////////////////////////" + row.get_attribute('outerHTML'))
        continue

      bed = bed.text
      breakfirst = breakfirst.text
      price = price.text
    
      #条件是: 双床, 双早, 找最低价格
      if bed.find('双') != -1 and breakfirst.find('双') != -1:
        #print('bed: ' + bed + " breakfirst: " + breakfirst + " price: " + price)
        real_price = ssutil.price(price)
        if real_price > 0 and real_price < lowest_price:
          lowest_price = real_price
          lowest_bed = bed
          lowest_breakfirst = breakfirst

    print("from: " + str(from_date) + " to: " + str(to_date) + " bed: " + lowest_bed + " breakfirst: " + lowest_breakfirst + " lowest_price: %d" % lowest_price)
    return lowest_price
    
