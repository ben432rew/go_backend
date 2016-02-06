from rest_framework import serializers


class NewGameSerializer(serializers.Serializer):
    player_w_pk = serializers.IntegerField(min_value=0)
    player_b_pk = serializers.IntegerField(min_value=0)
    board_size = serializers.IntegerField(max_value=26, min_value=1)


class NewMoveSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(min_value=0)
    new_move = serializers.CharField(max_length=10)
    player_color = serializers.ChoiceField(choices=['b', 'w'])
