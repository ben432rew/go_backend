from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gomill.sgf import Sgf_game

from game_logic.models import Game
from game_logic.serializers import NewGameSerializer, NewMoveSerializer


def set_game_sgf(new_move, game, player_color):
    sgf_string = str(game.sgf_file)
    game_sgf = Sgf_game.from_string(sgf_string)
    new_node = game_sgf.extend_main_sequence()
    new_node.set_move(player_color, new_move)
    game.sgf_file = game_sgf.serialise()
    return game_sgf


def is_game_over(sgf):
    """ If two pass moves in a row, then game is over """
    return False


def calculate_score(sgf):
    # TODO-Benny: Add territories, subtract captures, add komi here
    score = {'score': {'b': 'TDOO', 'w': 'TODO'}}
    return score


def calculate_not_allowed(sgf):
    return 'TODO-not_allowed'


def calculate_capture_moves(sgf):
    return 'TODO-capture_moves'


def process_move(sgf):
    """ Calculate illegal moves & possilbe captures """
    game_is_over = is_game_over(sgf)
    if game_is_over:
        score = calculate_score(sgf)
        return score
    else:
        not_allowed = calculate_not_allowed(sgf)
        capture_moves = calculate_capture_moves(sgf)
    return {'not_allowed': not_allowed,
            'capture_moves': capture_moves}


def update_game(game, score):
    game.score_w = score['w']
    game.score_b = score['b']
    if game.score_w > game.score_b:
        game.winner = game.player_w
    else:
        game.winner = game.player_b


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
            game = Game.objects.get(pk=serializer.data.get('game_id'))
            game_sgf = set_game_sgf(serializer.data.get('new_move'),
                                    game,
                                    serializer.data.get('player_color'))
            processed = process_move(game_sgf)
            # If game is over, save score and winner
            if 'score' in processed:
                update_game(game, processed['score'])
            game.save()
            processed['game'] = str(game.sgf_file)
            return Response(processed, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
