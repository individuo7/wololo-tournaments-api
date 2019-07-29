from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Game, Tournament
from .serializers import GameSerializer, TournamentSerializer


class TournamentViewSet(ReadOnlyModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    lookup_field = "slug"


class GameViewSet(ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
