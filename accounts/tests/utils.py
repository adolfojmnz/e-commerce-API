from accounts.models import User

from accounts.tests.data import (
    single_user_data,
    customer_data,
    vendor_data,
)


def create_user(user_data_dict=single_user_data):
    user = User.objects.create(**user_data_dict)
    user.save()
    return user

def create_customer():
    return create_user(customer_data)

def create_vendor():
    return create_user(vendor_data)
