from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS,
)
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from accounts.models import User
from utils.permissions import IsSuperUser
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


class UserListViewMixin(UserViewMixin, ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        return self.handle_request_on_valid_password(
            self.handle_post_request,
            request,
            *args,
            **kwargs,
        )


class UserDetailViewMixin(UserViewMixin, RetrieveUpdateDestroyAPIView):

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
            {'message': 'The user has been set as inactive.'},
            status=status.HTTP_200_OK,
        )


class CustomerListView(UserListViewMixin):

    def perform_create(self, serializer):
        serializer.save()
        cart = Cart.objects.create(user=serializer.instance)
        cart.save()

    def get_queryset(self):
        return super().get_queryset().filter(
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )


class CustomerDetailView(UserDetailViewMixin):

    def get_permissions(self):
        if self.request.user == User.objects.get(pk=self.kwargs['pk']):
            self.permission_classes = [IsAuthenticated]
        elif not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().filter(
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )


class AdminListView(UserListViewMixin):
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.validated_data['is_staff'] = True
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(
            is_staff=True,
            is_superuser=False,
        )


class AdminDetailView(UserDetailViewMixin):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user == User.objects.get(pk=self.kwargs['pk']):
            self.permission_classes = [IsAdminUser]
        elif not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()

    def get_queryset(self):
        return self.queryset.filter(is_staff=True)


class CurrentUserView(UserDetailViewMixin):
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
