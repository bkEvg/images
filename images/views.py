from .serializers import ImageSerializer
from .models import Image
from rest_framework import viewsets


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


