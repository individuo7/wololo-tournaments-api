from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Group, Prediction
from .serializers import GroupSerializer, PredictionSerializer


client = Elasticsearch()


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = "slug"


class PredictionViewSet(ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer


class LeaderboardViewSet(GenericViewSet):
    def list(self, request, tournament=None):
        if tournament:
            qs = (
                Search(using=client, index="player")
                .query("match", tournament=tournament)
                .execute()
            )

            return Response([{"username": x.username, "gold": x.gold} for x in qs])

        # sum the gold of all the tournaments participations
        qs = Search(using=client, index="player").execute()
        users = list(set([x.username for x in qs]))
        table = {users[i]: 0 for i in range(0, len(users))}

        for hit in qs:
            table[hit.username] += hit.gold

        return Response([{"username": key, "gold": table[key]} for key in table])
