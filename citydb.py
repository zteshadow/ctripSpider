#!/usr/bin/env python3

#该模块负责从数据库中存取城市缩写代码
#这个缩写代码是用来查询航班用的

import pymysql
import ssutil

class citydb:
  #初始化创建数据库连接, 创建数据库, 数据表
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

        #'city code table'
        cursor.execute("SET sql_notes = 0; ")
        cursor.execute("create table IF NOT EXISTS city_list (name VARCHAR(20), code VARCHAR(20), primary key(name)) charset = utf8;")
        cursor.execute("SET sql_notes = 1; ")        

      else:
        ssutil.error("cursor create error")
    else:
      ssutil.error("database connect error")

  #析构注意关闭cursor和connection
  def __del__(self):
    if self.cursor:
      self.cursor.close()

    if self.db:
      self.db.close()

  #return code of city named 'name'
  #上海->SHA, 北京->BJS
  def find_city_code(self, name):
    code = None
    if len(name) > 0:
      command = "select code from city_list where name = '" + name + "';"
      self.cursor.execute(command)
      item = self.cursor.fetchone()
      if item:
        code = item.get('code')

    return code

  #{name, code}
  #将ctrip返回的城市代码数据存入数据库
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

  #城市代码数据库是否存在
  def city_list_exist(self):
    command = "select * from city_list;"
    self.cursor.execute(command)
    city_list = self.cursor.fetchall()
    if len(city_list) > 0:
      return True
    else:
      return False;
  
  