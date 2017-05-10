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
        cursor.execute("create database IF NOT EXISTS travel")
        cursor.execute("USE travel;")

        #'hotel table'
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create table IF NOT EXISTS hotel (name VARCHAR(20), day DATE, price INT, primary key(name, day)) charset = utf8;")
        cursor.execute("SET sql_notes = 1; ")

        #'find_flights table'
        cursor.execute("SET sql_notes = 0; ")
        command = "create table IF NOT EXISTS flight (from_city VARCHAR(20), to_city VARCHAR(20), day DATE, price INT, primary key(from_city, to_city, day)) charset = utf8;"
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
  
  