#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
    def descorator(f):
        @wraps(f)
        def decorated_function(*argvs,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*argvs,**kwargs)
        return decorated_function
    return descorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)