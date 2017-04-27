#!/user/bin/env python3
#-*- coding:utf8 -*-

from flask import Flask, render_template
import chartkick
import pymysql

def get_all_data():
  all_data = {}
  db = pymysql.connect(host='127.0.0.1', user='root', passwd='Qwertyui123456')
  cursor = db.cursor(pymysql.cursors.DictCursor)
  cursor.execute("SET sql_notes = 0;")
  cursor.execute("USE ctrip;")

  cursor.execute("SET sql_notes = 0; ")
  cursor.execute("SET sql_notes = 1; ")

  command = "select id, price from lowest_price_eachday where search_date = '2017-04-27' order by id limit 0, 45;"
  cursor.execute(command)
  all_items = cursor.fetchall()
  for item in all_items:
    all_data[str(item["id"])] = item["price"]
    #item_string = "'" + str(item["id"]) + "':" + str(item["price"])
    #print(item_string)
    #print(item["id"])
    #print(item["price"])
    #all_data.append(item_string)

  return all_data

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

