# views.py
from django.shortcuts import render
from django.db.models import Count, F, Q
from .models import Team, Player, Game, Gol


def najlepsza_druzyna(request):
    teams = Team.objects.annotate(
        wygrane=Count(
            'mecze_gospodarz',
            filter=Q(mecze_gospodarz__wynik__gole_gospodarz__gt=F('mecze_gospodarz__wynik__gole_gosc'))
        ) + Count(
            'mecze_gosc',
            filter=Q(mecze_gosc__wynik__gole_gosc__gt=F('mecze_gosc__wynik__gole_gospodarz'))
        )
    ).order_by('-wygrane').first()

    return render(request, 'najlepsza_druzyna.html', {'team': teams})


def najlepszy_zawodnik(request):
    najlepszy = (
        Player.objects.annotate(liczba_goli=Count('gole'))
        .order_by('-liczba_goli')
        .first()
    )
    return render(request, 'najlepszy_zawodnik.html', {'player': najlepszy})


def najlepszy_na_druzyne(request):
    teams = Team.objects.all()
    selected_team = None
    najlepszy = None

    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        selected_team = Team.objects.get(id=team_id)

        zawodnicy = Player.objects.annotate(
            gole_na_druzyne=Count(
                'gole',
                filter=(
                    Q(gole__game__gosc__id=team_id) | Q(gole__game__gospodarz__id=team_id)
                ) & (
                    ~Q(zespoly__id=team_id)
                )
            )
        ).order_by('-gole_na_druzyne')

        # Wybieramy tylko jeśli ktoś naprawdę strzelił
        if zawodnicy and zawodnicy[0].gole_na_druzyne > 0:
            najlepszy = zawodnicy[0]

    return render(request, 'najlepszy_na_druzyne.html', {
        'teams': teams,
        'selected_team': selected_team,
        'player': najlepszy
    })
