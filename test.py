#!/user/bin/env python3
#-*- coding:utf8 -*-

import datetime, time

from ssdata import ssdata
from ssdriver import ssdriver

today = datetime.date.today()
cookies = ssdriver.get_cookies("http://hotels.ctrip.com/hotel/375470.html")
print(len(cookies))

index = 0
for item in cookies:
  if item['hostOnly'] == True:
    print(("[%d]: " % index) + str(item))
  index += 1
