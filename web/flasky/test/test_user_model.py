#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

import unittest
from  ..app.models import User
from ..app.models import User, AnonymousUser, Role, Permission, Follow


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u=User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u=User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u=User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u=User(password='cat')
        u2=User(password='cat')
        self.assertTrue((u.password_hash!=u2.password_hash))

    def test_role_and_permissions(self):
        Role.insert_roles()
        u=User(email='miles@example.com',password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u=AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

