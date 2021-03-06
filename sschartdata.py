#!/user/bin/env python3
#-*- coding:utf8 -*-

from flightdb import flightdb
from hoteldb import hoteldb
from ctriphotel import ctriphotel
from ssfavorite import ssfavorite
from ssdb import ssdb

class sschartdata:
  def __init__(self):
    pass

  @staticmethod
  def hotel_price(name):
    connection = ssdb()
    price_list = hoteldb(name, connection.db()).all()
    return {'data' : price_list, 'name' : name}

  #查找根据酒店名称, 查找city, 然后查找往返飞机
  @staticmethod
  def flight_price(name):
    connection = ssdb()
    city = ctriphotel.info(name)['city']
    home = ssfavorite.home()
    price_list_go = {}
    price_list_back = {}
    if city != home:
      price_list_go = flightdb(home, city, connection.db()).all()
      price_list_back = flightdb(city, home, connection.db()).all()
    return [{'data' : price_list_go, 'name' : home + '->' + city}, {'data' : price_list_back, 'name' : city + '->' + home}]

  #去程机票
  #4晚住宿
  #回程机票
  #返回(最低价, 日期, list)
  @staticmethod
  def travel_price(name, city, peoples):
    connection = ssdb()
    home = ssfavorite.home()

    #最低价格和日期
    lowest = 0
    day = ''

    price_list_go = {}
    price_list_back = {}

    if city != home:
      price_list_go = flightdb(home, city, connection.db()).all()
      price_list_back = flightdb(city, home, connection.db()).all()

    hotel_price_list = hoteldb(name, connection.db()).all()
    #total = flight * (人) + hotels * 4(晚) + flight * (人)
    total = {}
    hotels = {}

    if len(price_list_go) > 0:
      for key in hotel_price_list:
        hotel_price = hotel_price_list[key] * 4
        go_price = price_list_go.get(key)
        back_price = price_list_back.get(key)
        if go_price and back_price:
          flight_price = go_price * peoples + back_price * peoples
          hotels[key] = hotel_price
          total_price = hotel_price + flight_price
          total[key] = total_price
          if lowest == 0:
            lowest = total_price
            day = key
          elif total_price < lowest:
            lowest = total_price
            day = key

      return (lowest, day, [{'data':total, 'name':'机票+酒店'}, {'data':hotels, 'name':name}])
    else:
      for key in hotel_price_list:
        total_price = hotel_price_list[key] * 4
        hotels[key] = total_price
        if lowest == 0:
          lowest = total_price
          day = key
        elif total_price < lowest:
          lowest = total_price
          day = key

      return (lowest, day, [{'data' : hotels, 'name' : name + '(only)'}])




    