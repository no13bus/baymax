# -*- coding: utf-8 -*-

from baymax.user import User, UserDetail

from tests import TestCase


class TestUser(TestCase):

    def test_get_current_time(self):

        assert User.query.count() == 2
