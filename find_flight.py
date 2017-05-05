#!/usb/bin/env python3
#-*- coding:utf-8 -*-
# http://flights.ctrip.com/booking/SHA-YNJ-day-1.html?DDate1=2017-05-05

import datetime
from ssdata import ssdata
from ssdriver import ssdriver
from ssutil import ssutil

#'上海', '三亚', 2017-05-05
def get_price(driver, from_city, to_city, day):
  url = "http://flights.ctrip.com/booking/" + from_city + "-" + to_city + "-day-1.html?DDate1=";
  url += day.strftime('%Y-%m-%d')
  print(url)
  
  driver.get(url)
  try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "J_flightlist2")))
  except:
    
    ssutil.error('timeout to wait table')

if __name__ == '__main__':
  driver = ssdriver()
  bddata = ssdata()

  from_city = bddata.find_city('上海')
  to_city = bddata.find_city('哈尔滨')

  current_date = datetime.date.today()
  day_end = datetime.date(current_date.year, 12, 31)
  count = (day_end - current_date).days
  for i in range(0, count):
    day = datetime.date.today() + datetime.timedelta(days=i)
    price = get_price(driver.webdriver(), from_city, to_city, day)

