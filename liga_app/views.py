# views.py
from django.shortcuts import render, redirect
from django.db.models import Count, F, Q
from .models import Team, Player, Game, Gol, Wynik
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TeamForm, PlayerForm, GameForm
from django.contrib.auth.decorators import login_required


def home(request):
    teams = Team.objects.all()
    tabela = []

    for team in teams:
        mecze = Game.objects.filter(Q(gospodarz=team) | Q(gosc=team)).select_related('wynik')

        wins = draws = losses = goals_for = goals_against = 0

        for mecz in mecze:
            if not hasattr(mecz, 'wynik'):
                continue

            if mecz.gospodarz == team:
                gf = mecz.wynik.gole_gospodarz
                ga = mecz.wynik.gole_gosc
            else:
                gf = mecz.wynik.gole_gosc
                ga = mecz.wynik.gole_gospodarz

            goals_for += gf
            goals_against += ga

            if gf > ga:
                wins += 1
            elif gf == ga:
                draws += 1
            else:
                losses += 1

        games_played = wins + draws + losses
        points = wins * 3 + draws
        goal_difference = goals_for - goals_against
        win_rate = round((wins / games_played) * 100, 2) if games_played > 0 else 0

        tabela.append({
            'team': team,
            'games_played': games_played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goal_difference,
            'points': points,
            'win_rate': win_rate,
        })

    tabela.sort(key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_for']))

    return render(request, 'home.html', {
        'teams_table': tabela
    })

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # zmień na swój widok startowy
        else:
            messages.error(request, 'Nieprawidłowe dane logowania.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dodaj_druzyne(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TeamForm()
    return render(request, 'dodaj_druzyne.html', {'form': form})
@login_required
def dodaj_zawodnika(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PlayerForm()
    return render(request, 'dodaj_zawodnika.html', {'form': form})
@login_required
def dodaj_mecz(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'dodaj_mecz.html', {'form': form})
@login_required
def dodaj_gol(request):
    players = Player.objects.all()
    games = Game.objects.all()

    if request.method == 'POST':
        player_id = request.POST.get('strzelec')
        game_id = request.POST.get('game')
        minuta = request.POST.get('minuta')

        if player_id and game_id:
            Gol.objects.create(
                strzelec_id=player_id,
                game_id=game_id,
                minuta=minuta if minuta else None
            )
            return redirect('home')  # albo inna strona

    return render(request, 'dodaj_gol.html', {
        'players': players,
        'games': games
    })
@login_required
def dodaj_wynik(request):
    games = Game.objects.all()

    if request.method == 'POST':
        game_id = request.POST.get('game')
        gole_gospodarz = request.POST.get('gole_gospodarz')
        gole_gosc = request.POST.get('gole_gosc')

        if game_id and gole_gospodarz is not None and gole_gosc is not None:
            # Jeśli wynik już istnieje, edytuj, jeśli nie – stwórz
            wynik, created = Wynik.objects.update_or_create(
                game_id=game_id,
                defaults={
                    'gole_gospodarz': gole_gospodarz,
                    'gole_gosc': gole_gosc
                }
            )
            return redirect('home')

    return render(request, 'dodaj_wynik.html', {'games': games})
@login_required
def manage(request):
    return render(request, 'manage.html')

# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         password_confirm = request.POST['password_confirm']
#         if password != password_confirm:
#             messages.error(request, 'Hasła nie są zgodne.')
#             return render(request, 'register.html')
#         if len(username) < 3 or len(password) < 6:
#             messages.error(request, 'Nazwa użytkownika musi mieć co najmniej 3 znaki, a hasło co najmniej 6 znaków.')
#             return render(request, 'register.html')
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Użytkownik już istnieje.')
#         else:
#             User.objects.create_user(username=username, password=password)
#             messages.success(request, 'Zarejestrowano pomyślnie. Możesz się zalogować.')
#             return redirect('login')
#     return render(request, 'register.html')