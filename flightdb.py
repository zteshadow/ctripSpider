#!/usr/bin/env python3

import pymysql

class flightdb:
  def show_error(self, msg):
    print(msg)
    exit(1)

  def __init__(self, from_city, to_city):
    self.from_city = from_city
    self.to_city = to_city
    self.cursor = None
    self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='Qwertyui123456', charset='utf8')
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
        command = "create table IF NOT EXISTS flight (from_city VARCHAR(20), to_city VARCHAR(20), day DATE, price INT, primary key(from_city, to_city, day)) charset = utf8;"
        cursor.execute(command)
        cursor.execute("SET sql_notes = 1; ")

      else:
        show_error("cursor create error")
    else:
      show_error("database connect error")

  def __del__(self):
    if self.cursor:
      self.cursor.close()

    if self.db:
      self.db.close()

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
    except:
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
    from_city = self.from_city
    to_city = self.to_city    
    all_data = {}
    command = "select day, price from flight where "
    command += "from_city = '" + from_city + "'" 
    command += " and to_city = '" + to_city + "' order by day;"
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

