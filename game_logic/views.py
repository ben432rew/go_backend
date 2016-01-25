from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gomill.sgf import Sgf_game

from game_logic.models import Game


class NewGameView(APIView):
    """ View for creating a new game """

    def post(self, request):
        player_w_pk = request.data.get('player_w_pk')
        player_b_pk = request.data.get('player_b_pk')
        board_size = request.data.get('board_size')

        player_w = User.objects.get(pk=player_w_pk)
        player_b = User.objects.get(pk=player_b_pk)
        new_game = Sgf_game(size=board_size)
        game = Game.objects.create(player_w=player_w,
                                   player_b=player_b,
                                   sgf_file=new_game.serialise())
        return Response(game.sgf_file, status=status.HTTP_200_OK)


class NewMoveView(APIView):
    def post(self, request):
        new_move = request.data.get('new_move')
        player_color = request.data.get('player_color')
        game_id = request.data.get('game_id')
        game = Game.objects.get(pk=game_id)
        sgf_string = str(game.sgf_file)
        game_sgf = Sgf_game.from_string(sgf_string)
        # process_move(new_move, game_sgf)
        new_node = game_sgf.extend_main_sequence()
        new_node.set_move(player_color, new_move)
        game.sgf_file = game_sgf.serialise()
        game.save()
        return Response(game.sgf_file, status=status.HTTP_200_OK)
