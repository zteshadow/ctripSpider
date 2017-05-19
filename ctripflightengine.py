#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, datetime, logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#自定义package
from ssutil import ssutil
from ssdriver import ssdriver
from ssdata import ssdata

class ctripflightengine:
  def __init__(self, from_city, to_city):
    bddata = ssdata()
    from_code = bddata.find_city_code(from_city)
    to_code = bddata.find_city_code(to_city)
    self.url = "http://flights.ctrip.com/booking/" + from_code + "-" + to_code + "-day-1.html";

    self.bddata = bddata
    self.driver = ssdriver()

  def __del__(self):
    pass

  def load(self):
    flighturl = self.url
    driver = self.driver.webdriver()
    print(flighturl)
    driver.get(flighturl)
    ssdriver.add_cookies(driver, flighturl)

    #等待搜索按钮ok, 算加载成功
    try:
      table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "btnReSearch")))
    except:
      ssutil.save_web(driver)
      ssutil.error('timeout to wait search button')

#td[0-8], [0]: 航空公司, 航班和机型, [1]:出发时间和机场, [3]:到达时间和机场, [6]:价格
#返回元组(航班, 价格)

#'上海', '三亚', 2017-05-05
# return: 765
  def get_lowest_price(self, table):
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
    else:
      print("----empty table------")
      ssutil.log(table.get_attribute('outerHTML'))

    return (airline, lowest_price)

  #作为页面已经被刷新的标志
  def get_flag_element(self):
    driver = self.driver.webdriver()
    #return driver.find_elements_by_tag_name('html')
    return driver.find_element_by_id('btnReSearch')

  def click_button(self, day):
    driver = self.driver.webdriver()

    day_string = day.strftime('%Y-%m-%d')

    day_box = driver.find_element_by_id('DDate1')
    if day_box != None:
      day_box.clear()
      day_box.send_keys(day_string)
    else:
      ssutil.error('no day box')
    
    search_button = driver.find_element_by_id('btnReSearch')
    if search_button != None:
      search_button.click()
    else:
      ssutil.error('no search button')

  def get_price(self, day):
    driver = self.driver.webdriver()

    refresh_flag = self.get_flag_element()
    self.click_button(day)
    
    #如果存在, 则等待dom刷新
    if refresh_flag:
      try:
        WebDriverWait(driver, 20).until(staleness_of(refresh_flag))
      except:
        print(refresh_flag.get_attribute('outerHTML'))
        ssutil.error('timeout to refresh page')
      #print("html refresh ok")

      table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'J_flightlist2'))
      )
      
      #等待都加载完
      WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'flight_pagefooter'))
        )
  
    data = self.get_lowest_price(table)
    if data[0]:
      print(str(day) + ", " + data[0] + ": %d" % data[1])
    else:
      ssutil.save_web(driver)
      return 0

    return data[1]
    