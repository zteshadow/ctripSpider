#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from ssdata import ssdata

class ctriphotel:
  def __init__(self, name):
    self.name = name
    self.data = ssdata()

  def __del__(self):
    pass

  def set_price(self, start, end, price):
    self.data.add_hotel(self.name, start, end, price)
