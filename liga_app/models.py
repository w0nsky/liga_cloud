from django.db import models


class League(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class Schedule(models.Model):
    league = models.OneToOneField(
        League,
        on_delete=models.CASCADE,
        related_name='terminarz'
    )
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.league.nazwa} - {self.nazwa}"


class Team(models.Model):
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='zespoly'
    )
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class Player(models.Model):
    nazwa = models.CharField(max_length=255)
    zespoly = models.ManyToManyField(
        Team,
        related_name='gracze'
    )

    def __str__(self):
        return self.nazwa


class Location(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa


class Game(models.Model):
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='mecze'
    )
    nazwa = models.CharField(max_length=255)
    date_and_time = models.DateTimeField()

    gospodarz = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='mecze_gospodarz'
    )
    gosc = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='mecze_gosc'
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='mecze'
    )

    def __str__(self):
        return f"{self.nazwa} ({self.date_and_time})"


class Wynik(models.Model):
    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
        related_name='wynik'
    )
    gole_gospodarz = models.IntegerField(default=0)
    gole_gosc = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.game.gospodarz} {self.gole_gospodarz}:{self.gole_gosc} {self.game.gosc}"


class Gol(models.Model):
    strzelec = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='gole'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='gole'
    )
    minuta = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Gol: {self.strzelec} w meczu {self.game}"