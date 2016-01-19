from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gomill.sgf import Sgf_game

from game_logic.models import Game


class NewGameView(APIView):
    """ View for creating a new game """

    def post(self, request):
        # TODO-Benny: serialize POST information first
        player_w_pk = request.POST.get('player_w_pk')
        player_b_pk = request.POST.get('player_b_pk')
        board_size = request.POST.get('board_size')
        new_game = Sgf_game(size=board_size)
        game = Game.objects.creat(player_w=player_w_pk,
                                  player_b=player_b_pk,
                                  sgf_file=new_game.serialise())
        return Response(game.sgf_file, status=status.HTTP_200_OK)
