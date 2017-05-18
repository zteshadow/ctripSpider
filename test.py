#!/user/bin/env python3
#-*- coding:utf8 -*-

import datetime, time

from ssdata import ssdata
from ssfavorite import ssfavorite
from ssdriver import ssdriver
from ctriphotelengine import ctriphotelengine


flight_list = ssfavorite.flights()
for from_city, to_city in flight_list:
  print(from_city + " -> " + to_city)
