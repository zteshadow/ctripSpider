#!/usr/bin/env python3

from ssdb import ssdb
from urllib.request import urlopen
import datetime

class ssdata:
  def __init__(self):
    self.db = ssdb()

  def create_city_list(self):
    today = datetime.date.today().strftime('%Y_%m_%d_%H_%M_%S')
    url = "http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?releaseno=?CR_" + today
    data = urlopen(url)
    print(data.read())

  def find_city(self, name):
    if self.db.city_list_exist():
      code = self.db.find_city(name)
    else:
      self.create_city_list()

