#!/usr/bin/env python3
#-*- coding:utf-8 -*-

class Hotel:
  def __init__(self, bed, breakfirst, price):
    self.bed = bed
    self.breakfirst = breakfirst
    self.price = price

  def get_bed(self):
    return self.bed

  def get_breakfirst(self):
    return self.breakfirst

  def get_price(self):
    return self.price

  def say_hi(self):
    print("bed: " + str(self.bed) + " breakfirst: " + str(self.breakfirst) + " price: %d" % self.price)

