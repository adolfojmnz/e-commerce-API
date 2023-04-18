from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User

from .serializers import UserSerializer


class UserViewMixin:
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer

    def handle_post_request(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def handle_put_request(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def handle_patch_request(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def handle_request_on_valid_password(self,
                                     handler_func,
                                     request,
                                    *args,
                                    **kwargs):
        password = request.data.get('password')
        try:
            validate_password(password)
            return handler_func(request, *args, **kwargs)
        except ValidationError as error:
            return Response(
                {'Validation Error': f'{error}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TypeError as error:
            if request.method in ['PATCH']:
                return handler_func(request, *args, **kwargs)
            return Response(
                {'password': ['This field is required.']},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserListView(UserViewMixin, ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_post_request,
            request,
            *args,
            **kwargs,
        )


class UserDetailView(UserViewMixin, RetrieveUpdateDestroyAPIView):

    def put(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_put_request,
            request,
            *args,
            **kwargs,
        )

    def patch(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_patch_request,
            request,
            *args,
            **kwargs,
        )
