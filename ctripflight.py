#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#对数据库flightdb的浅层封装
from flightdb import flightdb

class ctripflight:
  #起始地点, 到达地点, flightdb(数据库)
  def __init__(self, from_city, to_city, data):
    self.from_city = from_city
    self.to_city = to_city
    self.data = data

  def find_price(self, day):
    return self.data.find(day)
    
  def set_price(self, day, price):
    data = self.data
    if data.find(day) > 0:
      data.modify(day, price)
    else:
      data.add(day, price)

