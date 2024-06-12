
from marshmallow import Schema, fields, post_load
from src.score.game import Game, GameSchema
from src.score.set import Set, SetSchema


class Score:
    def __init__(self, current_game=None, sets=None, match_is_over=False, match_winner=None, **kwargs):
        if current_game is None:
            self.current_game = Game()
        else:
            self.current_game = current_game
        if sets is None:
            self.sets = [Set()]
        else:
            self.sets = sets
        self.match_is_over = match_is_over
        self.num_sets = len(self.sets)
        self.match_winner = match_winner

    def serialize(self):
        schema = ScoreSchema()
        return schema.dumps(self)


class ScoreSchema(Schema):
    current_game = fields.Nested(GameSchema, required=True)
    sets = fields.Nested(SetSchema, many=True, required=True)
    match_is_over = fields.Boolean(required=True)
    num_sets = fields.Integer(required=True)
    match_winner = fields.Integer(required=True, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Score(**data)
