from rest_framework.viewsets import ModelViewSet
from .models import Tournament
from .serializers import TournamentSerializer


class TournamentViewSet(ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
