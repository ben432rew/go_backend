from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gomill.sgf import Sgf_game

from game_logic.models import Game
from game_logic.serializers import NewGameSerializer, NewMoveSerializer


def process_move(move, sgf):
    """ return prohibited moves and moves that will capture """
    return 'TODO-not_allowed', 'TODO-capture_moves'


class NewGameView(APIView):
    """ View for creating a new game """

    def post(self, request):
        serializer = NewGameSerializer(data=request.data)
        if serializer.is_valid():
            player_w = User.objects.get(pk=serializer.data.get('player_w_pk'))
            player_b = User.objects.get(pk=serializer.data.get('player_b_pk'))
            new_game = Sgf_game(size=serializer.data.get('board_size'))
            game = Game.objects.create(player_w=player_w,
                                       player_b=player_b,
                                       sgf_file=new_game.serialise())
            return Response({'game_id': game.pk}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewMoveView(APIView):
    def post(self, request):
        serializer = NewMoveSerializer(data=request.data)
        if serializer.is_valid():
            new_move = serializer.data.get('new_move')
            game = Game.objects.get(pk=serializer.data.get('game_id'))
            sgf_string = str(game.sgf_file)
            game_sgf = Sgf_game.from_string(sgf_string)
            not_allowed, capture_moves = process_move(new_move, game_sgf)
            new_node = game_sgf.extend_main_sequence()
            new_node.set_move(serializer.data.get('player_color'), new_move)
            game.sgf_file = game_sgf.serialise()
            game.save()
            response = {
                'game': game.sgf_file,
                'not_allowed': not_allowed,
                'capture_moves': capture_moves,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
