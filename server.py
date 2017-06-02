#!/user/bin/env python3
#-*- coding:utf8 -*-

import datetime
import chartkick, pymysql

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from flightdb import flightdb
from hoteldb import hoteldb
from ssfavorite import ssfavorite
from sschartdata import sschartdata

app = Flask(__name__, static_folder = chartkick.js())
app.jinja_env.add_extension("chartkick.ext.charts")
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    return render_template('index.html')

#type标识有没有机票
@app.route("/hotel")
def show_hotels():
  name = request.values.get("name")
  if name == None :
    name = ""

  hotel_list = []
  travel_peoples = 0
  city = None
  travel_list = ssfavorite.travels()
  for hotel_name, city, peoples in travel_list:
    if name == hotel_name:
      travel_peoples = peoples
      city = city
    hotel_list.append(hotel_name)

  (low, day, data) = sschartdata.travel_price(name, city, travel_peoples)
  if len(data) > 1:
    type = 1
  else:
    type = 0

  return render_template('hotel.html', data = data, hotel_list = hotel_list, type = type, label = '最低价: '+ str(low) + '(' + str(day) + ')')

@app.route("/flight")
def show_flights():
    data = flightdb('上海', '哈尔滨')
    flights = data.all()
    return render_template('flight.html', data = flights)

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

@app.route("/base")
def base():
    return render_template('base.html')

if (__name__ == '__main__'):
    app.run(debug=True,port=8764)

