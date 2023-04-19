from accounts.models import User

from accounts.tests.data import single_user_data


def create_user():
    user = User.objects.create(**single_user_data)
    user.save()
    return user

