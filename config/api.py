# from django.conf.urls import include, url
from rest_framework import routers
from api.tournaments.views import GameViewSet, TournamentViewSet

router = routers.DefaultRouter()
router.register(r"tournaments", TournamentViewSet)
router.register(r"games", GameViewSet)


urlpatterns = router.urls
