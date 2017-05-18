#!/usr/bin/env python3

import pymysql
import ssutil

class hoteldb:
  def __init__(self, name):
    self.name = name
    self.cursor = None
    self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='Qwertyui123456', charset='utf8')
    if self.db:
      cursor = self.db.cursor(pymysql.cursors.DictCursor)
      if cursor:
        self.cursor = cursor

        #'ctrip' data base
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create database IF NOT EXISTS travel;")
        cursor.execute("USE travel;")

        #'hotel table'
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create table IF NOT EXISTS hotel (name VARCHAR(20), day DATE, price INT, primary key(name, day)) charset = utf8;")
        cursor.execute("SET sql_notes = 1; ")
      else:
        ssutil.error("cursor create error")
    else:
      ssutil.error("database connect error")

  def __del__(self):
    if self.cursor:
      self.cursor.close()

    if self.db:
      self.db.close()
  
  def find(self, day):
    name = self.name
    command = "select price from hotel where name = '"
    command += name + "'"
    command += " and day = '" + str(day) + "';"
    #print(command)
    try:
      self.cursor.execute(command)
      item = self.cursor.fetchone()
      if item:
        return item['price']
      else:
        return None
    except:
      print(command + "--> command error")
      return None

  def add(self, day, price):
    name = self.name
    data = "insert into hotel (name, day, price) values("
    data += "'" + name + "'"
    data += ", '" + str(day) + "'"
    data += ", %d);" % price
    #print(data)
    try:
      self.cursor.execute(data)
      self.db.commit()
    except:
      print(data + "--> command error")

  def modify(self, day, price):
    name = self.name
    command = "update hotel set price = %d " % price
    command += " where name = '"
    command += name + "'"
    command += " and day = '" + str(day) + "';"
    #print(command)
    try:
      self.cursor.execute(command)
      self.db.commit()
    except:
      print(command + "--> command error")

  def all(self):
    name = self.name
    all_data = {}
    command = "select name, day, price from hotel where name = '" + name + "' order by day;"
    self.cursor.execute(command)
    all_items = self.cursor.fetchall()
    for item in all_items:
      all_data[str(item["day"])] = item["price"]
      #item_string = "'" + str(item["id"]) + "':" + str(item["price"])
      #print(item_string)
      #print(item["id"])
      #print(item["price"])
      #all_data.append(item_string)

    return all_data
