from rest_framework import viewsets, routers

from .models import Bus
from .serializers import BusSerializer


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


router = routers.DefaultRouter()
router.register(r'bus', BusViewSet, basename='bus')
