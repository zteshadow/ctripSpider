#!/user/bin/env python3
#-*- coding:utf8 -*-

from flask import Flask, render_template
import chartkick

app = Flask(__name__, static_folder = chartkick.js())
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chart")
def chart():
    data = {'2017-04-23':765, '2017-05-8':891, '2017-07-12':1513}
    return render_template('chart.html', data = data)

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

if (__name__ == '__main__'):
    app.run(debug=True,port=8764)