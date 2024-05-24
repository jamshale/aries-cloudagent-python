from unittest import IsolatedAsyncioTestCase

from aries_cloudagent.admin import testing_class


class TestAdminAuthentication(IsolatedAsyncioTestCase):

    def test_1(self):
        result = testing_class.testing_func(1, 2)
        assert result == 3
