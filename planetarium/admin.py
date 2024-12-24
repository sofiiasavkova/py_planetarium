from django.contrib import admin
from .models import AstronomyShow, PlanetariumDome, ShowTheme, ShowSession, Ticket, Reservation

admin.site.register(AstronomyShow)
admin.site.register(PlanetariumDome)
admin.site.register(ShowTheme)
admin.site.register(ShowSession)
admin.site.register(Ticket)
admin.site.register(Reservation)