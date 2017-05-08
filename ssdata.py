#!/usr/bin/env python3
#{
# display: "上海(浦东国际机场)",
# data: "Shanghai(PU DONG)|上海(浦东国际机场)(PVG)|2|SHA,PVG"
#}, 
#{
# display: "上海(虹桥国际机场)",
# data: "Shanghai(HONGQIAO)|上海(虹桥国际机场)(SHA)|2|SHA,SHA"
#}, 
#{
# display: "广州",
# data: "Guangzhou|广州(CAN)|32|CAN"
#}
#第一步从以下结构中提取出""中间的数据, 得到:
#上海(浦东国际机场)
#Shanghai(PU DONG)|上海(浦东国际机场)(PVG)|2|SHA,PVG
#Shanghai(HONGQIAO)|上海(虹桥国际机场)(SHA)|2|SHA,SHA
#Guangzhou|广州(CAN)|32|CAN

#第二步, 对于每一条目, 用|分隔, 然后把()去掉, 再取,分隔的第一项, 这样就不区分上海的浦东和虹桥机场了(上海<->SHA)

from ssdb import ssdb
from urllib.request import urlopen
import datetime
import json
import re

class ssdata:
  def __init__(self):
    self.db = ssdb()

  #上海(虹桥国际机场)(SHA) -> 上海(虹桥国际机场)
  def remove_code(self, name):
    try:
      pos = name.rindex('(')
      return name[0:pos]
    except:
      return name

  def get_city_list(self):
    city_list = {}
    today = datetime.date.today().strftime('%Y_%m_%d_%H_%M_%S')
    url = "http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?releaseno=?CR_" + today
    response = urlopen(url).read().decode('gb2312')
    
    #以下解析参考文件头的说明
    pattern = re.compile('\"(.*?)\"')
    data_list = pattern.findall(response)
    for row in data_list:
      item_list = row.split('|')
      if len(item_list) >= 4:
        name = self.remove_code(item_list[1])
        code = item_list[3]
        if len(name) > 0 and len(code) > 0:
          city_list[name] = code

    return city_list

  def find_city(self, name):
    if self.db.city_list_exist():
      code = self.db.find_city(name)
      return code
    else:
      city_list = self.get_city_list()
      self.db.add_city_list(city_list)
      return city_list[name]
  
  def add_hotel(self, name, day, search_day, price):
    self.db.add_hotel(name, day, search_day, price)

  def find_hotel(self, name, day, search_day):
    return self.db.find_hotel(name, day, search_day)

  def find_hotel_all_price(self, name, search_day):
    return self.db.find_hotel_all_price(name, search_day)

  def add_flight(self, from_city, to_city, day, search_day, price):
    self.db.add_flight(from_city, to_city, day, search_day, price)
  
  def find_flight(self, from_city, to_city, day, search_day):
    return self.db.find_flight(from_city, to_city, day, search_day)

