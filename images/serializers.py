from rest_framework import serializers
from .models import Image, ConvertedImage


class ResizedImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    class Meta:
        model = ConvertedImage
        serializer_class = serializers.ListSerializer
        fields = ['image']



class ImageSerializer(serializers.ModelSerializer):
    child = ResizedImageSerializer(many=True, read_only=True)
    class Meta:
        model = Image
        fields = ['name', 'url', 'picture', 'width', 'height', 'child']

