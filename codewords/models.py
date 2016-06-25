from __future__ import unicode_literals

import base64
import enum
import json
from datetime import datetime

from ._app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class FromIndexMixin(object):
    @classmethod
    def from_index(cls, i):
        for idx, elt in enumerate(cls):
            if idx == i:
                return elt


class GameStatus(FromIndexMixin, enum.Enum):
    __order__ = 'BLUE_TEAM_GIVE RED_TEAM_GIVE BLUE_TEAM_GUESS RED_TEAM_GUESS DONE'

    BLUE_TEAM_GIVE = 0
    RED_TEAM_GIVE = 1
    BLUE_TEAM_GUESS = 2
    RED_TEAM_GUESS = 3
    DONE = 4


class GameWinner(FromIndexMixin, enum.Enum):
    __order__ = 'BLUE_TEAM RED_TEAM NOT_DONE'

    BLUE_TEAM = 0
    RED_TEAM = 1
    NOT_DONE = 2


class TeamWord(FromIndexMixin, enum.Enum):
    __order__ = 'BLUE RED WHITE BLACK'

    BLUE = 0
    RED = 1
    WHITE = 2
    BLACK = 3


class Game(db.Model):
    
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    words_encoded = db.Column(db.Unicode)
    teams_encoded = db.Column(db.BigInteger)
    status_encoded = db.Column(db.SmallInteger)

    moves = db.relationship("GameMoves", backref="game")
    hints = db.relationship("GameHint", backref="game")

    _words = None
    _teams = None

    def __init__(self, words, teams):
        words_encoded = json.dumps(words)
        teams_encoded = 0
        for idx, team in enumerate(teams):
            teams_encoded |= team.value << (2 * idx)
        status_encoded = GameStatus.BLUE_TEAM_GIVE.value
        super(Game, self).__init__(words_encoded=words_encoded,
                                   teams_encoded=teams_encoded,
                                   status_encoded=status_encoded)

    @property
    def words(self):
        if self._words:
            return self._words
        self._words = json.loads(self.words_encoded)
        return self._words

    @property
    def teams(self):
        if self._teams:
            return self._teams
        teams_decoded = [(self.teams_encoded & (0b11 << (2 * i))) >> (2 * i)
                         for i in range(len(self.words))]
        self._teams = [TeamWord.from_index(team) for team in teams_decoded]
        return self._teams

    @property
    def status(self):
        return GameStatus.from_index(self.status_encoded)

    @status.setter
    def status(self, stat):
        self.status_encoded = stat.value


class GameMoves(db.Model):

    __tablename__ = 'game_moves'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    team_encoded = db.Column(db.Integer)
    word = db.Column(db.Unicode)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if team in kwargs:
            kwargs[team_encoded] = team.value
        super(GameMoves, self).__init__(*args, **kwargs)


class GameHint(db.Model):

    __tablename__ = 'game_hints'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    word = db.Column(db.Unicode)
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
