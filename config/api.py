# from django.conf.urls import include, url
from rest_framework import routers
from api.tournaments.views import TournamentViewSet

router = routers.DefaultRouter()
router.register(r"tournaments", TournamentViewSet)


urlpatterns = router.urls
