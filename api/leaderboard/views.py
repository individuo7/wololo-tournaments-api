from rest_framework.viewsets import ModelViewSet
from .models import Group, Prediction
from .serializers import GroupSerializer, PredictionSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = "slug"


class PredictionViewSet(ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
