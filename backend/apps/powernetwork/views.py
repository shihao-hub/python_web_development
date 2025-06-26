from rest_framework import viewsets, routers

from .models import Bus
from .serializers import BusSerializer


class BusModelViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer



