from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from planetarium.models import ShowSession, Reservation, Ticket
from datetime import datetime, timedelta
from planetarium.serializers import TicketSerializer

User = get_user_model()

class PlanetariumTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.admin_user = User.objects.create_user(
            email="user_admin@example.com",
            password="password123",
            is_staff=True
        )

    def create_show_session(self, rows, seats_in_row, show_time=None):
        return ShowSession.objects.create(
            rows=rows,
            seats_in_row=seats_in_row,
            show_time=show_time or datetime.now() + timedelta(days=1)
        )

    def create_reservation(self, show_session, user):
        return Reservation.objects.create(
            show_session=show_session,
            user=user
        )

    def create_ticket(self, show_session, row, seat):
        return Ticket.objects.create(
            show_session=show_session,
            row=row,
            seat=seat
        )

    def test_tickets_available_correct_calculation(self):
        session = self.create_show_session(rows=5, seats_in_row=5)
        self.create_ticket(show_session=session, row=1, seat=1)
        self.create_ticket(show_session=session, row=2, seat=2)

        self.assertEqual(session.tickets_available(), 23)  # Total seats = 25, Sold = 2

    def test_tickets_available_no_tickets_left(self):
        session = self.create_show_session(rows=2, seats_in_row=2)
        self.create_ticket(show_session=session, row=1, seat=1)
        self.create_ticket(show_session=session, row=1, seat=2)
        self.create_ticket(show_session=session, row=2, seat=1)
        self.create_ticket(show_session=session, row=2, seat=2)

        self.assertEqual(session.tickets_available(), 0)

    def test_tickets_available_all_tickets_available(self):
        session = self.create_show_session(rows=3, seats_in_row=3)

        self.assertEqual(session.tickets_available(), 9)

    def test_get_queryset_with_show_time(self):
        session1 = self.create_show_session(rows=3, seats_in_row=3, show_time=datetime.now() + timedelta(days=1))
        session2 = self.create_show_session(rows=3, seats_in_row=3, show_time=datetime.now() + timedelta(days=2))

        response = self.client.get("/api/showsessions/", {"show_time": session1.show_time.date()})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], session1.id)

    def test_get_queryset_without_show_time(self):
        self.create_show_session(rows=3, seats_in_row=3)
        self.create_show_session(rows=3, seats_in_row=3)

        response = self.client.get("/api/showsessions/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_perform_create_reservation_authenticated(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        session = self.create_show_session(rows=3, seats_in_row=3)
        response = self.client.post("/api/reservations/", {"show_session": session.id})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Reservation.objects.filter(user=self.user, show_session=session).exists())

    def test_perform_create_reservation_unauthenticated(self):
        session = self.create_show_session(rows=3, seats_in_row=3)
        response = self.client.post("/api/reservations/", {"show_session": session.id})

        self.assertEqual(response.status_code, 401)

    def test_get_queryset_admin_user(self):
        token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        session = self.create_show_session(rows=3, seats_in_row=3)
        self.create_reservation(show_session=session, user=self.admin_user)

        response = self.client.get("/api/reservations/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Reservation.objects.count())

    def test_get_queryset_normal_user(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        session = self.create_show_session(rows=3, seats_in_row=3)
        self.create_reservation(show_session=session, user=self.user)

        response = self.client.get("/api/reservations/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(reservation["user"] == self.user.id for reservation in response.data))

    def test_ticket_validation_seat_taken(self):
        session = self.create_show_session(rows=3, seats_in_row=3)
        self.create_ticket(show_session=session, row=1, seat=1)

        ticket_data = {"show_session": session.id, "row": 1, "seat": 1}
        serializer = TicketSerializer(data=ticket_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("seat", serializer.errors)

    def test_ticket_validation_out_of_bounds(self):
        session = self.create_show_session(rows=3, seats_in_row=3)

        ticket_data = {"show_session": session.id, "row": 4, "seat": 1}
        serializer = TicketSerializer(data=ticket_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("row", serializer.errors)

    def test_ticket_creation_valid(self):
        session = self.create_show_session(rows=3, seats_in_row=3)

        ticket_data = {"show_session": session.id, "row": 1, "seat": 1}
        serializer = TicketSerializer(data=ticket_data)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(Ticket.objects.filter(row=1, seat=1, show_session=session).exists())
