#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ssdriver:
  def __init__(self):
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

    self.driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)

  def __del__(self):
    self.driver.quit()

  def webdriver(self):
    return self.driver
