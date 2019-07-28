from rest_framework.serializers import ModelSerializer
from .models import Tournament


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = Tournament
        fields = "__all__"
