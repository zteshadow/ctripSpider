#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from hoteldb import hoteldb

class ctriphotel:
  def __init__(self, name, data):
    self.name = name
    self.data = data

  def __del__(self):
    pass

  def set_price(self, day, price):
    data = self.data
    if data.find(day) != None:
      data.modify(day, price)
    else:
      data.add(day, price)
  
