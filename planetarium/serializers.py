from rest_framework import serializers
from .models import (
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    ShowTheme,
    Ticket,
    Reservation,
)


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ["id", "title", "description"]


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.StringRelatedField()
    planetarium_dome = serializers.StringRelatedField()

    class Meta:
        model = ShowSession
        fields = ["id", "astronomy_show", "planetarium_dome", "show_time"]


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ["id", "name", "rows", "seats_in_row"]


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ["id", "name"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "show_session", "reservation"]


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]
