#!/user/bin/env python3
#-*- coding:utf8 -*-

from flask import Flask, render_template
import chartkick
import pymysql
import datetime
from flightdb import flightdb
from hoteldb import hoteldb

app = Flask(__name__, static_folder = chartkick.js())
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hotel")
def show_hotels():
    hotels = hoteldb('上海大厦').all()
    flights = flightdb('上海', '哈尔滨').all()
    #total = flight * 3(人) + hotels * 4(晚) + flight * 3(人)
    total = {}
    for key in hotels:
      hotel_price = hotels[key] * 4
      flight_price = flights[key] * 6
      hotels[key] = hotel_price
      flights[key] = flight_price
      total[key] = hotel_price + flight_price

    data = [{'data':hotels, 'name':'hotel'}, {'data':total, 'name':'total(hotel + flight)'}]
    return render_template('hotel.html', data = data)

@app.route("/flight")
def show_flights():
    data = flightdb('上海', '哈尔滨')
    flights = data.all()
    return render_template('flight.html', data = flights)

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

if (__name__ == '__main__'):
    app.run(debug=True,port=8764)

