#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from hoteldb import hoteldb
from urllib.request import urlopen
from urllib.parse import quote
import json
from ssutil import ssutil

class ctriphotel:
  def __init__(self, name, data):
    self.name = name
    self.data = data

  def find_price(self, day):
    return self.data.find(day)

  def set_price(self, day, price):
    data = self.data
    if data:
      if data.find(day) != None:
        data.modify(day, price)
      else:
        data.add(day, price)
  
  #根据hotel名称, 返回信息
  #['url'] = url
  #['city'] = city
  @staticmethod
  def info(name):
    info = {}
    url = "http://m.ctrip.com/restapi/h5api/searchapp/search?action=autocomplete&source=globalonline&keyword=%s" % quote(name)
    #print(url)
    content = urlopen(url).read()
    if content == None:
      ssutil.error('content not found')

    json_data = json.loads(content.decode("utf-8"))
    #print(json_data)

    hotel_list = None;
    try:
      hotel_list = json_data['data']
    except:
      ssutil.error("--no 'data' for url: " + url)

    for hotel in hotel_list:
      try:
        if hotel['word'] == name and hotel['type'] == 'hotel':
          #print(hotel)
          try:
            info['url'] = hotel['url']
            info['city'] = hotel['districtname']
          except:
            ssutil.error("--no 'url/districtname' for json: " + hotel)
          break
      except:
        ssutil.error("--no 'word' for json: " + hotel)

    return info
