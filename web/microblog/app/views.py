#!/usr/bin/python
# _*_ encoding:utf-8_*_
import flask

from app import app
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"