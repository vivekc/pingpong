from __future__ import unicode_literals

import json

from django.db import models

from random import randint
from .constants import WINNING_SCORE

# Create your models here.


class Player(models.Model):
    class Meta:
        db_table = 'player'
    player_id = models.IntegerField(unique=True, default=0)
    name = models.CharField(max_length=200)
    defense_size = models.IntegerField(default=0)
    defense_numbers = models.CharField(max_length=100)
    attack_number = models.IntegerField(null=True, default=None)
    score = models.IntegerField(default=0)

    def __repr__(self):
        return "%s-%s" %(self.player_id, self.name)

    def set_defence(self):
        """set defence array"""
        self.defense_numbers = json.dumps([randint(1, 10) for _ in range(self.defense_size)])
        self.save()

    def set_offense(self):
        """generate random number"""
        self.attack_number = randint(1, 10)

    @property
    def has_won(self):
        return self.score >= WINNING_SCORE


class GameMoves(models.Model):
    """
    The game starts with the first (offensive) player picking one random number (from 1 to 10)
    and informing the referee about it. The defending player creates a
    defense array of random numbers (from 1 to 10).
    The length of the defense array is preset for each player
    (see players matrix at the end of this document) and defined in their individual configuration files.
    If the number picked by the offensive player does not exist in the defense array,
    then the player gets one point and plays again.
    If it exists, the defender gets the point and they switch roles (defender attacks).
    The first player to get 5 points wins the game.
    """
    class Meta:
        db_table = 'game_moves'

    game_id = models.AutoField(primary_key=True)
    attacker = models.ForeignKey('Player', related_name='attacker')
    defender = models.ForeignKey('Player', related_name='defender')
    attacker_move = models.IntegerField(default=0)         # random integer between 0 to Player.defense_set_size
    attacker_score = models.IntegerField(default=0)
    defender_score = models.IntegerField(default=0)

    def switch_roles(self):
        temp = self.attacker
        self.defender = self.attacker
        self.attacker = temp
        self.save()


# @Todo: operate on multiple tournaments where Queue championship is member variable of class Tournament
"""
Tournament ->* Round ->* Game



class Tournament(models.Model):
    round_id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey('GameMoves')
"""