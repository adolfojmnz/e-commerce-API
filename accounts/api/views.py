from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from accounts.models import User
from accounts.api.serializers import UserSerializer

from carts.models import Cart


class UserViewMixin:
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        # Assign a Cart to the user
        cart = Cart.objects.create(user=serializer.instance)
        cart.save()

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

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class CurrentUserView(UserDetailView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user.last_login = timezone.now()
            user.save()
        return response

