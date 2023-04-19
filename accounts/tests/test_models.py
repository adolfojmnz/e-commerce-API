from django.test import TestCase

from accounts.models import User

from accounts.tests.utils import create_user
from accounts.tests.data import single_user_data


class SetUp(TestCase):

    def setUp(self):
        self.user = create_user()


class TestUser(SetUp):

    def test_user(self):
        self.assertEqual(
            User.objects.filter(pk=self.user.pk).exists(),
            True,
        )
        self.assertEqual(
            User.objects.get(pk=self.user.pk).email,
            self.user.email,
        )
        self.assertEqual(
            User.objects.get(pk=self.user.pk).password,
            self.user.password,
        )

