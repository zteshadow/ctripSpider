#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, json
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
      if not os.path.isfile(file_path):
        chrome_path = ssdriver.get_chrome_driver_path()
        driver = webdriver.Chrome(chrome_path)
        driver.get('http://hotels.ctrip.com/')
        cookies = driver.get_cookies()
        #print(cookies)
        with open(file_path, 'w', encoding = 'utf-8') as f:
          json.dump(cookies, f)
      else:
        with open(file_path, 'r') as f:
          cookies = json.load(f)
    return cookies

  @staticmethod
  def add_cookies(driver, url):
    cookies = ssdriver.get_cookies(url)
    for item in cookies:
      driver.add_cookie(item)

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
    phantomjs_path = ssdriver.get_phantomjs_path()
    self.driver = webdriver.PhantomJS(executable_path = phantomjs_path, desired_capabilities = dcap)

  def __del__(self):
    if self.driver:
      #self.driver.quit()
      pass

  def webdriver(self):
    return self.driver
