#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
from flask import Flask
app=Flask(__name__)
app.config.from_object('config')
from app import views