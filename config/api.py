# from django.conf.urls import include, url
from rest_framework import routers
from api.tournaments.views import GameViewSet, TournamentViewSet
from api.leaderboard.views import GroupViewSet, LeaderboardViewSet, PredictionViewSet

router = routers.DefaultRouter()
router.register(r"games", GameViewSet)
router.register(r"groups", GroupViewSet)
router.register("leaderboards", LeaderboardViewSet, basename="leaderboards-all")
router.register(
    "leaderboards/(?P<tournament>[^/.]+)", LeaderboardViewSet, basename="leaderboards"
)
router.register(r"predictions", PredictionViewSet)
router.register(r"tournaments", TournamentViewSet)


urlpatterns = router.urls
