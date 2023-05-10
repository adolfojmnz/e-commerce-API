from rest_framework import serializers

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'image']
        read_only_fields = ['created_at']
