from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_412_PRECONDITION_FAILED, HTTP_200_OK
from Queue import Queue, Empty
from player.constants import MAX_NO_OF_PLAYERS
from player.models import Player, GameMoves
from signal import signal

# Create your views here.

championship = Queue(maxsize=MAX_NO_OF_PLAYERS)

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


def draw_games():
    """
    Draw games for Initial Round

    the referee draws the 4 initial games and notifies the players about their game id,
    opponent and their order of play (first, second).
    All games are knock-out and supervised by the referee.
    After all 4 games have ended, the referee informs the defeated players to shut down,
    draws the second round (semi finals), informs the players about their new game id and opponents.
    In a similar fashion, the process continues to the final game and cup winner.
    """
    global championship
    player_ids = list()

    if not championship.full():
        return False

    for i in range(MAX_NO_OF_PLAYERS):
        try:
            print "collecting queued player ids"
            player_ids.append(championship.get())
        except Empty:
            pass

    i = 0
    while i < len(player_ids):
        GameMoves.objects.create(
            attacker=Player.objects.get(player_id=player_ids[i]),
            defender=Player.objects.get(player_id=player_ids[i+1])
        )
        i += 2


class JoinChampionship(APIView):
    """
    The Referee program starts and waits all 8 players to join the championship. When all players have joined
    """

    def get(self, request):
        return Response({"success": True, "response_code": HTTP_200_OK})

    def post(self, request, player_id):
        """
        :param player_id:
        :param request:
        :return:
        """
        global championship
        if not Player.objects.filter(player_id=player_id).exists():
            return Response(
                {"success": False, "response_code": HTTP_412_PRECONDITION_FAILED, "message": "Player does not exist"}
            )
        if championship.full():
            return Response(
                {"success": False, "response_code": HTTP_412_PRECONDITION_FAILED, "message": "Championship is full"}
            )
        championship.put(player_id)
        if championship.full():
            print "All players have joined the Championship"
            # draw initial round of games and inform players of their opponents and sequence of play
            draw_games()
        return Response(
            {'success': True, "response_code": HTTP_200_OK, "message": "You have successfully joined the tournament"})
