#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid=StringField('openid',validators=[DataRequired()])
    remember_me=BooleanField('remember_me',default=False)
