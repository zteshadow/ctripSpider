#!/usr/bin/env python3
#-*- coding=utf8 -*-

import sys, os
from selenium import webdriver

class ssutil:
  def __init__(self):
    pass

  @staticmethod
  def error(msg):
    #print(msg)
    #os._exit(1)
    sys.exit(msg)

  @staticmethod
  def save_web(driver):
    if os.path.isfile('./web.png'):
      os.remove('./web.png')
    driver.save_screenshot("web.png")
