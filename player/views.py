from django.shortcuts import render
# Create your views here.
from django.views.generic import View

from player.models import Player


class PlayerDashboard(View):
    """ Display Players configuration and allow join tournament """
    template_name = 'player/dashboard.html'

    def get(self, request):
        players = Player.objects.all()
        return render(request, self.template_name, context={'players': players})

