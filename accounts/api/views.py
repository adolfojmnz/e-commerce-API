from rest_framework.generics import ListCreateAPIView

from accounts.models import User

from .serializers import UserSerializer


class UserListView(ListCreateAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer