# from django.conf.urls import include, url
from rest_framework import routers
from api.tournaments.views import GameListViewSet, GameDetailsViewSet, TournamentViewSet
from api.leaderboard.views import GroupViewSet, LeaderboardViewSet, PredictionViewSet

router = routers.DefaultRouter()
router.register(r"games/(?P<tournament>[^/.]+)", GameListViewSet, basename="games")
router.register(r"games", GameDetailsViewSet, basename="games")
router.register(r"groups", GroupViewSet)
router.register(r"leaderboards", LeaderboardViewSet, basename="leaderboards-all")
router.register(
    r"leaderboards/(?P<tournament>[^/.]+)", LeaderboardViewSet, basename="leaderboards"
)
router.register(r"predictions", PredictionViewSet)
router.register(r"tournaments", TournamentViewSet)


urlpatterns = router.urls
