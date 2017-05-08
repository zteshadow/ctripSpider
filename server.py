#!/user/bin/env python3
#-*- coding:utf8 -*-

from flask import Flask, render_template
import chartkick
import pymysql
import datetime
from ssdata import ssdata

def get_all_data():
  data = ssdata()
  return data.find_hotel_all_price('上海大厦', datetime.date.today())

app = Flask(__name__, static_folder = chartkick.js())
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chart")
def chart():
    data = get_all_data()
    return render_template('chart.html', data = data)

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

if (__name__ == '__main__'):
    app.run(debug=True,port=8764)

