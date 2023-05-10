from rest_framework.generics import CreateAPIView

from images.models import Image
from images.api.serializers import ImageSerializer


class Images(CreateAPIView):
    model = Image
    queryset = model.objects.all()
    serializer_class = ImageSerializer
