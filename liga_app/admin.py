from django.contrib import admin
from .models import League, Schedule, Team, Player, Location, Game, Wynik, Gol

admin.site.register(League)
admin.site.register(Schedule)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Location)
admin.site.register(Game)
admin.site.register(Wynik)
admin.site.register(Gol)