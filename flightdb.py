#!/usr/bin/env python3

import pymysql
import ssutil

class flightdb:
  def __init__(self, from_city, to_city, db):
    self.from_city = from_city
    self.to_city = to_city
    self.cursor = None
    self.db = db
    if self.db:
      cursor = self.db.cursor(pymysql.cursors.DictCursor)
      if cursor:
        self.cursor = cursor

        #'ctrip' data base
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create database IF NOT EXISTS travel;")
        cursor.execute("use travel;")

        #'find_flights table'
        cursor.execute("SET sql_notes = 0; ")
        command = "create table IF NOT EXISTS flight (from_city VARCHAR(50), to_city VARCHAR(50), day DATE, price INT, primary key(from_city, to_city, day)) charset = utf8;"
        cursor.execute(command)
        cursor.execute("SET sql_notes = 1; ")

      else:
        ssutil.error("cursor create error")
    else:
      ssutil.error("database connect error")

  def __del__(self):
    if self.cursor:
      self.cursor.close()

  def find(self, day):
    from_city = self.from_city
    to_city = self.to_city
    command = "select price from flight where from_city = '"
    command += from_city + "'"
    command += " and to_city = '" + to_city + "'"
    command += " and day = '" + str(day) + "';"
    #print(command)
    try:
      self.cursor.execute(command)
      item = self.cursor.fetchone()
      if item:
        return item['price']
      else:
        return 0
    except Exception as e:
      print(e)
      print(command + "--> command error")
      return 0

  def add(self, day, price):
    from_city = self.from_city
    to_city = self.to_city    
    command = "insert into flight (from_city, to_city, day, price) values("
    command += "'" + from_city + "'"
    command += ", '" + to_city + "'"
    command += ", '" + str(day) + "'"
    command += ", %d);" % price
    #print(command)
    try:
      self.cursor.execute(command)
      self.db.commit()
    except:
      print(command + "--> command error")

  def modify(self, day, price):
    from_city = self.from_city
    to_city = self.to_city    
    command = "update flight set price = %d " % price
    command += " where from_city = '"
    command += from_city + "'"
    command += " and to_city = '" + to_city + "'"
    command += " and day = '" + str(day) + "';"
    #print(command)
    try:
      self.cursor.execute(command)
      self.db.commit()
    except:
      print(command + "--> command error")

  def all(self):
    all_data = {}
    from_city = self.from_city
    to_city = self.to_city
    if from_city and to_city:
      command = "select day, price from flight where "
      command += "from_city = '" + from_city + "'" 
      command += " and to_city = '" + to_city + "' order by day;"
      self.cursor.execute(command)
      all_items = self.cursor.fetchall()
      for item in all_items:
        all_data[str(item["day"])] = item["price"]

    return all_data

