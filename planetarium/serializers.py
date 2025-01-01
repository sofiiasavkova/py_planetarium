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
        fields = ["id", "title", "description", "theme"]


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

    def validate(self, data):
        show_session = data.get("show_session")

        if not show_session:
            raise serializers.ValidationError(
                {"show_session": "Show session is required."}
            )

        dome = show_session.planetarium_dome

        row = data.get("row")
        if row < 1 or row > dome.rows:
            raise serializers.ValidationError(
                {"row": f"Row {row} is out of range."}
            )

        seat = data.get("seat")
        if seat < 1 or seat > dome.seats_in_row:
            raise serializers.ValidationError(
                {"seat": f"Seat {seat} is out of range."}
            )

        if Ticket.objects.filter(
                row=row,
                seat=seat,
                show_session=show_session
        ).exists():
            raise serializers.ValidationError(
                {"seat": f"Seat {seat} in row {row} is already occupied."}
            )

        return data


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]
