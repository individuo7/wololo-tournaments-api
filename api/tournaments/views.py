from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from .models import Game, Tournament
from .serializers import GameSerializer, TournamentSerializer
from rest_framework import mixins


class TournamentViewSet(ReadOnlyModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    lookup_field = "slug"


class GameViewSixin(GenericViewSet):
    serializer_class = GameSerializer
    lookup_field = "slug"

    def get_queryset(self):
        tournament = self.kwargs["tournament"]
        if tournament == "upcoming":
            return Game.objects.order_by("-date")[:5]

        return Game.objects.filter(tournament__slug=tournament)

    class Meta:
        abstract = True


class GameListViewSet(mixins.ListModelMixin, GameViewSixin):
    pass


class GameDetailsViewSet(mixins.RetrieveModelMixin, GameViewSixin):
    pass
