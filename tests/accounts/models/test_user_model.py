from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.hashers import check_password

from datetime import datetime

from accounts.models import User

from tests.helpers import AccountsTestHelpers
from tests.data import user_single as user_data


class SetUp(TestCase):

    def setUp(self):
        accounts_helpers = AccountsTestHelpers()
        self.user = accounts_helpers.create_user()
        return super().setUp()


class TestUser(SetUp):

    def test_user_model(self):
        self.assertEqual(User.objects.filter(pk=self.user.pk).exists(), True)
        db_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(db_user.avatar_url, user_data['avatar_url'])
        self.assertEqual(db_user.username, user_data['username'])
        self.assertTrue(
            check_password(user_data['password'], db_user.password)
        )
        self.assertEqual(db_user.first_name, user_data['first_name'])
        self.assertEqual(db_user.last_name, user_data['last_name'])
        self.assertEqual(db_user.email, user_data['email'])
        self.assertEqual(db_user.about, user_data['about'])
        self.assertEqual(db_user.birthdate.__str__(), user_data['birthdate'])
        self.assertEqual(db_user.is_active, user_data['is_active'])
        self.assertEqual(
            db_user.date_joined,
            timezone.make_aware(
                datetime.strptime(user_data['date_joined'], '%Y-%m-%dT%H:%M:%SZ')
            )
        )
        self.assertEqual(
            db_user.last_login,
            timezone.make_aware(
                datetime.strptime(user_data['last_login'], '%Y-%m-%dT%H:%M:%SZ')
            )
        )
