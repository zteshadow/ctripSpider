#!/usr/bin/env python3

import pymysql

class ssdb:
  def __init__(self):
    self.connection = pymysql.connect(host='127.0.0.1', user='root', passwd='Qwertyui123456', charset='utf8')

  #上海(虹桥国际机场)(SHA) -> 上海(虹桥国际机场)
  def db(self):
    return self.connection

  def __del__(self):
    self.connection.close()
