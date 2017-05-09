#!/usr/bin/env python3

import pymysql

class ssdb:
  def show_error(self, msg):
    print(msg)
    exit(1)

  def __init__(self):
    self.cursor = None
    self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='Qwertyui123456', charset='utf8')
    if self.db:
      cursor = self.db.cursor(pymysql.cursors.DictCursor)
      if cursor:
        self.cursor = cursor

        #'ctrip' data base
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create database IF NOT EXISTS ctrip")
        cursor.execute("USE ctrip")

        #'hotel table'
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create table IF NOT EXISTS find_hotel (name VARCHAR(20), day DATE, search_date DATE, price INT, primary key(name, day, search_date)) charset = utf8;")
        cursor.execute("SET sql_notes = 1; ")

        #'find_flights table'
        cursor.execute("SET sql_notes = 0; ")
        command = "create table IF NOT EXISTS find_flight (from_city VARCHAR(20), to_city VARCHAR(20), day DATE, search_date DATE, price INT, primary key(from_city, to_city, day, search_date)) charset = utf8;"
        cursor.execute(command)
        cursor.execute("SET sql_notes = 1; ")

        #'city code table'
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create table IF NOT EXISTS city_list (name VARCHAR(20), code VARCHAR(20), primary key(name)) charset = utf8;")
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

  #return code of city named 'name'
  def find_city_code(self, name):
    code = None
    if len(name) > 0:
      command = "select code from city_list where name = '" + name + "';"
      self.cursor.execute(command)
      item = self.cursor.fetchone()
      code = item['code']

    return code

  #{name, code}
  def add_city_list(self, map):
    for name in map:
      code = map[name]
      data = "insert into city_list (name, code) values('"
      data += name
      data += "', '"
      data += code
      data += "');"
      #print(data)
      self.cursor.execute(data)
      self.db.commit()

  def city_list_exist(self):
    command = "select * from city_list;"
    self.cursor.execute(command)
    city_list = self.cursor.fetchall()
    if len(city_list) > 0:
      return True
    else:
      return False;
  
  def add_hotel(self, name, day, search_date, price):
    data = "insert into find_hotel (name, day, search_date, price) values("
    data += "'" + name + "'"
    data += ", '" + str(day) + "'"
    data += ", '" + str(search_date) + "'"
    data += ", %d);" % price
    #print(data)
    try:
      self.cursor.execute(data)
      self.db.commit()
    except:
      print(data + "--> command error")

  def find_hotel(self, name, day, search_day):
    command = "select price from find_hotel where name = '"
    command += name + "'"
    command += " and day = '" + str(day) + "'"
    command += " and search_date = '" + str(search_day) + "';"
    #print(command)
    try:
      self.cursor.execute(command)
      item = self.cursor.fetchone()
      #print(item)
      if item:
        return item['price']
      else:
        return 0
    except:
      print(command + "--> command error")
      return 0

  def find_hotel_all_price(self, name, search_day):
    all_data = {}
    command = "select name, day, price from find_hotel where search_date = '" + search_day.strftime('%Y-%m-%d') + "' order by day;"
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

  def add_flight(self, from_city, to_city, day, search_day, price):
    command = "insert into find_flight (from_city, to_city, day, search_date, price) values("
    command += "'" + from_city + "'"
    command += ", '" + to_city + "'"
    command += ", '" + str(day) + "'"
    command += ", '" + str(search_day) + "'"
    command += ", %d);" % price
    #print(command)
    try:
      self.cursor.execute(command)
      self.db.commit()
    except:
      print(command + "--> command error")

  def find_flight(self, from_city, to_city, day, search_day):
    command = "select price from find_flight where from_city = '"
    command += from_city + "'"
    command += " and to_city = '" + to_city + "'"
    command += " and day = '" + str(day) + "'"
    command += " and search_date = '" + str(search_day) + "'"
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

  def find_flight_all_price(self, from_city, to_city, search_day):
    all_data = {}
    command = "select day, price from find_flight where "
    command += "from_city = '" + from_city + "'" 
    command += " and to_city = '" + to_city + "'"
    command += " and search_date = '" + search_day.strftime('%Y-%m-%d') + "' order by day;"
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

