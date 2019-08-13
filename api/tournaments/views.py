from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from .models import Game, Tournament
from .serializers import GameSerializer, TournamentSerializer
from rest_framework import mixins


class TournamentViewSet(ReadOnlyModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    lookup_field = "slug"


class GameViewMixin(GenericViewSet):
    serializer_class = GameSerializer
    lookup_field = "slug"

    def get_queryset(self):
        tournament = self.kwargs.get("tournament", None)
        if tournament is None:
            return Game.objects.all()
        if tournament == "upcoming":
            return Game.objects.order_by("-date")[:5]

        return Game.objects.filter(tournament__slug=tournament)

    class Meta:
        abstract = True


class GameListViewSet(mixins.ListModelMixin, GameViewMixin):
    pass


class GameDetailsViewSet(mixins.RetrieveModelMixin, GameViewMixin):
    pass
