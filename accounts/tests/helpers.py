from django.urls import reverse
from django.test import Client

from accounts.models import User

from accounts.tests.data import (
    single_user_data,
    customer_data,
    vendor_data,
)


class UserTestMixin:

    def create_user(self, user_data=None) -> User:
        user_data = user_data if user_data else single_user_data
        return User.objects.create_user(**user_data)

    def create_customer(self) -> User:
        return self.create_user(customer_data)

    def create_vendor(self) -> User:
        return self.create_user(vendor_data)

