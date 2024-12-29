from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .permissions import IsAdminOrIfAuthenticatedReadOnly
from .models import AstronomyShow, PlanetariumDome, ShowTheme, ShowSession, Reservation, Ticket
from .serializers import (
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowThemeSerializer,
    ShowSessionSerializer,
    ReservationSerializer,
    TicketSerializer,
)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        show_time = self.request.query_params.get("show_time")
        if show_time:
            date = datetime.strptime(show_time, "%Y-%m-%d").date()
            return self.queryset.filter(show_time__date=date)
        return self.queryset

    @action(detail=True, methods=["GET"])
    def tickets_available(self, request, pk=None):
        session = self.get_object()
        dome = session.planetarium_dome
        total_seats = dome.rows * dome.seats_in_row
        tickets_sold = Ticket.objects.filter(show_session=session).count()
        available_seats = total_seats - tickets_sold
        return Response({"tickets_available": available_seats}, status=status.HTTP_200_OK)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related("tickets__show_session")
    serializer_class = ReservationSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("show_session", "reservation")
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
