"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import liga_app.views as views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('register/', views.register_view, name='register'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('najlepsza-druzyna/', views.najlepsza_druzyna, name='najlepsza_druzyna'),
    path('najlepszy-zawodnik/', views.najlepszy_zawodnik, name='najlepszy_zawodnik'),
    path('najlepszy-na-druzyne/', views.najlepszy_na_druzyne, name='najlepszy_na_druzyne'),
    path('dodaj-druzyne/', views.dodaj_druzyne, name='dodaj_druzyne'),
    path('dodaj-zawodnika/', views.dodaj_zawodnika, name='dodaj_zawodnika'),
    path('dodaj-mecz/', views.dodaj_mecz, name='dodaj_mecz'),
    path('dodaj-gol/', views.dodaj_gol, name='dodaj_gol'),
    path('dodaj-wynik/', views.dodaj_wynik, name='dodaj_wynik'),
    path('manage/', views.manage, name='manage'),
    path('', views.home, name='home'),
]

