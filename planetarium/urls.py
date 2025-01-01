from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    TicketViewSet,
)

app_name = "planetarium"

router = DefaultRouter()
router.register(
    r"astronomy-shows",
    AstronomyShowViewSet,
    basename="astronomyshow"
)
router.register(
    r"planetarium-domes",
    PlanetariumDomeViewSet,
    basename="planetariumdome"
)
router.register(r"show-sessions", ShowSessionViewSet, basename="showsession")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]
