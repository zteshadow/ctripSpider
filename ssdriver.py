#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, json, time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ssutil import ssutil

class ssdriver:
  @staticmethod
  def create_cookies(url):
    cookies = None
    domain_list = urlparse(url).hostname.split('.')
    name = None
    if len(domain_list) >= 3:
      name = domain_list[1] + '.' + domain_list[2]
    else:
      ssutil.error(domain_list)

    if name:
      file_path = "./data/" + name + '.cookies'

      if os.path.isfile(file_path):
        os.remove(file_path)

      chrome_path = ssdriver.get_chrome_driver_path()
      driver = webdriver.Chrome(chrome_path)
      driver.get(url)

      #20秒等待输入密码
      time.sleep(20)

      cookies = driver.get_cookies()
      #print(cookies)
      with open(file_path, 'w', encoding = 'utf-8') as f:
        json.dump(cookies, f, sort_keys=True)
    return cookies

  @staticmethod
  def get_cookies(url):
    cookies = None
    domain_list = urlparse(url).hostname.split('.')
    name = None
    if len(domain_list) >= 3:
      name = domain_list[1] + '.' + domain_list[2]
    else:
      ssutil.error(domain_list)

    if name:
      file_path = "./data/" + name + '.cookies'
      with open(file_path, 'r') as f:
        cookies = json.load(f)
    return cookies

  @staticmethod
  def add_cookies(driver, url):
    driver.delete_all_cookies()
    cookies = ssdriver.get_cookies(url)
    index = 0
    for item in cookies:
      if item['hostOnly'] != True:
        #print(("[%d]: " % index) + str(item))
        driver.add_cookie(item)
      index += 1

  @staticmethod
  def get_phantomjs_path():
    phantomjs_path = os.environ.get('PHANTOMJSPATH')
    if phantomjs_path:
      return phantomjs_path
    else:
      ssutil.quit("phantomjs needed, set environment for 'PHANTOMJSPATH'")

  @staticmethod
  def get_chrome_driver_path():
    path = os.environ.get('CHROMEDRIVERPATH')
    if path:
      return path
    else:
      ssutil.quit("chrome driver needed, set environment for 'CHROMEDRIVERPATH'")

  def __init__(self):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
      )
    dcap["phantomjs.page.settings.loadImages"] = False
    #dcap["Host"] = 'hotels.ctrip.com'
    phantomjs_path = ssdriver.get_phantomjs_path()
    self.driver = webdriver.PhantomJS(executable_path = phantomjs_path, desired_capabilities = dcap)

  def __del__(self):
    if self.driver:
      self.driver.quit()
      pass

  def webdriver(self):
    return self.driver
