#!/user/bin/env python3
#-*- coding:utf8 -*-

from flask import Flask, render_template
import chartkick
import pymysql
import datetime
from ssdata import ssdata

app = Flask(__name__, static_folder = chartkick.js())
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hotel")
def show_hotels():
    data = ssdata()
    hotels = data.find_hotel_all_price('上海大厦', datetime.date.today())
    return render_template('hotel.html', data = hotels)

@app.route("/flight")
def show_flights():
    data = ssdata()
    flights = data.find_flight_all_price('上海', '哈尔滨', datetime.date.today())
    return render_template('flight.html', data = flights)

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

if (__name__ == '__main__'):
    app.run(debug=True,port=8764)

