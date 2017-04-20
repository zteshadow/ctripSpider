#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#selenium
import os
import time
import datetime
from selenium import webdriver

#
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
from bs4 import BeautifulSoup

import json

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

def ss_get_price_for_date(driver, from_date, to_date):
  from_string = from_date.strftime('%Y-%m-%d')
  to_string = to_date.strftime('%Y-%m-%d')
  driver.find_element_by_name('cc_txtCheckIn').clear()
  driver.find_element_by_name('cc_txtCheckIn').send_keys(from_string)
  driver.find_element_by_name('cc_txtCheckOut').clear()
  driver.find_element_by_name('cc_txtCheckOut').send_keys(to_string)
  driver.find_element_by_id('changeBtn').click()
  time.sleep(5) # 控制间隔时间，等待浏览器反映

def ss_retrieve_all_price_for_hotel(hotelurl):
    #driver = webdriver.Firefox()
    chromedriver = '/usr/local/bin/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get(hotelurl)
    driver.maximize_window() # 将浏览器最大化显示
    time.sleep(5) # 控制间隔时间，等待浏览器反映

    for i in range(0, 100): #当前开始100天
      start = datetime.date.today() + datetime.timedelta(days=i)
      end = start + datetime.timedelta(days=1)
      print("start: "+start.strftime('%Y-%m-%d')+" end: "+end.strftime('%Y-%m-%d'))
      #tomorrow_string = tomorrow.strftime('%Y-%m-%d')
      ss_get_price_for_date(driver, start, end)

url = ss_get_url_for_hotel('上海大厦')
print(url)
chromedriver = '/usr/local/bin/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(url)
driver.maximize_window() # 将浏览器最大化显示
time.sleep(5) # 控制间隔时间，等待浏览器反映
start = datetime.date.today() + datetime.timedelta(days=5)
end = start + datetime.timedelta(days=1)
ss_get_price_for_date(driver, start, end)




