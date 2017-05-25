#!/user/bin/env python3
#-*- coding:utf8 -*-

from flightdb import flightdb
from hoteldb import hoteldb
from ctriphotel import ctriphotel
from ssfavorite import ssfavorite

class sschartdata:
  def __init__(self):
    pass

  @staticmethod
  def hotel_price(name):
    price_list = hoteldb(name).all()
    return {'data' : price_list, 'name' : name}

  #查找根据酒店名称, 查找city, 然后查找往返飞机
  @staticmethod
  def flight_price(name):
    city = ctriphotel.info(name)['city']
    home = ssfavorite.home()
    price_list_go = {}
    price_list_back = {}
    if city != home:
      price_list_go = flightdb(home, city).all()
      price_list_back = flightdb(city, home).all()
    return [{'data' : price_list_go, 'name' : home + '->' + city}, {'data' : price_list_back, 'name' : city + '->' + home}]

  #3人去程机票
  #4晚住宿
  #3人回程机票
  @staticmethod
  def travel_price(name):
    city = ctriphotel.info(name).get('city')
    home = ssfavorite.home()

    price_list_go = {}
    price_list_back = {}

    if city != home:
      price_list_go = flightdb(home, city).all()
      price_list_back = flightdb(city, home).all()

    hotel_price_list = hoteldb(name).all()
    #total = flight * 3(人) + hotels * 4(晚) + flight * 3(人)
    total = {}
    hotels = {}

    if len(price_list_go) > 0:
      for key in hotel_price_list:
        hotel_price = hotel_price_list[key] * 4
        go_price = price_list_go.get(key)
        back_price = price_list_back.get(key)
        if go_price and back_price:
          flight_price = go_price * 3 + back_price * 3
          hotels[key] = hotel_price
          total[key] = hotel_price + flight_price
      return [{'data':total, 'name':'机票+酒店'}, {'data':hotels, 'name':name}]      
    else:
      for key in hotel_price_list:
        hotels[key] = hotel_price_list[key] * 4
      return [{'data' : hotels, 'name' : name + '(only)'}]

    