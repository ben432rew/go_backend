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
    g = Sgf_game.from_string(sgf)
    # check last three moves because first move is intialized as (None, None)
    last_three_moves = [node.get_move() for node in g.get_main_sequence()][-3:]
    # game has to have at least two moves total
    if len(last_three_moves) < 3:
        return False
    elif last_three_moves[0][1] is None and last_three_moves[1][1] is None:
        return True
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
    """ If game is not over, calculate illegal moves & possible captures """
    game_is_over = is_game_over(sgf)
    if game_is_over:
        score = calculate_score(sgf)
        return score
    else:
        not_allowed = calculate_not_allowed(sgf)
        capture_moves = calculate_capture_moves(sgf)
    return {'not_allowed': not_allowed,
            'capture_moves': capture_moves}


def update_game(gam, score):
    gam.score_w = score['w']
    gam.score_b = score['b']
    gam.winner = gam.player_w if gam.score_w > gam.score_b else gam.player_b


class NewGameView(APIView):
    """ View for creating a new game """

    def post(self, request):
        serializer = NewGameSerializer(data=request.data)
        if serializer.is_valid():
            new_game = Sgf_game(size=serializer.data.get('board_size'))
            game = Game.objects.create(
                player_w_id=serializer.data.get('player_w_id'),
                player_b_id=serializer.data.get('player_b_id'),
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
