#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from ssdata import ssdata

class ctripflight:
  def __init__(self, from_city, to_city):
    self.from_city = from_city
    self.to_city = to_city
    self.data = ssdata()

  def __del__(self):
    pass

  def set_price(self, day, price):
    #self.data.add_hotel(self.name, start, end, price)
    pass
