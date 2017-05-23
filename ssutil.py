#!/usr/bin/env python3
#-*- coding=utf8 -*-

import sys, os
from selenium import webdriver

class ssutil:
  def __init__(self):
    pass

  @staticmethod
  def log(msg):
    with open('error.log', 'w') as outfile:
      outfile.write(msg)

  #quit without exception
  @staticmethod
  def quit(msg):
    print(msg)
    os._exit(1)

  #exception will rail
  @staticmethod
  def error(msg):
    print(msg)
    #os._exit(1)
    sys.exit(msg)

  @staticmethod
  def save_web(driver):
    if os.path.isfile('./web.png'):
      os.remove('./web.png')
    driver.save_screenshot("web.png")

  #￥113 -> 113
  @staticmethod
  def price(price):
    pricenumber = 0
    price = price.strip()
    while price.isalnum() == False and len(price) >= 2:
      price = price[1:]

    if price.isalnum():
      try:
        pricenumber = int(price)
      except:
        #print('--error price: ' + price)
        pass

    return pricenumber
