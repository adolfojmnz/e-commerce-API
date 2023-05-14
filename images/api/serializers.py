from rest_framework import serializers

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image.url

    class Meta:
        model = Image
        fields = ['id', 'image', 'image_url']

