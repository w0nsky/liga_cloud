from django import forms
from .models import Team, Player, Game, Gol

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['league', 'nazwa']
        widgets = {
            'league': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'nazwa': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nazwa', 'zespoly']
        widgets = {
            'nazwa': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'zespoly': forms.CheckboxSelectMultiple(attrs={
                'class': 'mt-2 space-y-2'
            }),
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['schedule', 'nazwa', 'date_and_time', 'gospodarz', 'gosc', 'location']
        widgets = {
            'schedule': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'nazwa': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'date_and_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'gospodarz': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'gosc': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
            'location': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm p-2 mt-1'
            }),
        }
