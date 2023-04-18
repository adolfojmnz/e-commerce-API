from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'about',
            'avatar',
            'birthdate',
            'password',
            'is_active',
            'last_login',
            'date_joined',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
        }

    def save(self, **kwargs):
        try:
            self.validated_data['password'] = make_password(
                self.validated_data['password']
            )
        except KeyError:
            pass
        finally:
            return super().save(**kwargs)
