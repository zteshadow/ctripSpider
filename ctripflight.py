#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flightdb import flightdb

class ctripflight:
  def __init__(self, from_city, to_city, data):
    self.from_city = from_city
    self.to_city = to_city
    self.data = data

  def __del__(self):
    pass

  def set_price(self, day, price):
    data = self.data
    if data.find(day):
      data.modify(day, price)
    else:
      data.add(day, price)

