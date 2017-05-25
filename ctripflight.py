#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flightdb import flightdb

class ctripflight:
  def __init__(self, from_city, to_city, data):
    self.from_city = from_city
    self.to_city = to_city
    self.data = data

  def set_price(self, day, price):
    data = self.data
    if data.find(day) != None:
      data.modify(day, price)
    else:
      data.add(day, price)

