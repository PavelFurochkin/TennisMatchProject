from src.controllers.base_controller import BaseController
from src.render.renderer import Render
from urllib.parse import parse_qs
from src.db.db_service.db_service import TennisDBService
from src.score.ScoreUpdateService import ScoreUpdateService
from exceptions import MatchNotFoundByUUIDError
from src.db.DAO.DAO import TennisDAO


class MatchScoreController(BaseController):
    def do_get(self):
        try:
            match = TennisDAO.get_match_by_uuid(self.get_uuid_from_query_string())
            match_param = ScoreUpdateService.show_match_params(match)
            players_names = TennisDAO.get_players_name(match.player1, match.player2)
            body = Render.render('match_score', **match_param, **players_names)
            self.response.body = body
        except MatchNotFoundByUUIDError as e:
            body = Render.render('error_page', exception=e.message)
            self.response.body = body
            self.response.status = '404 Not Found'

    def do_post(self):
        try:
            match = TennisDAO.get_match_by_uuid(self.get_uuid_from_query_string())
        except MatchNotFoundByUUIDError as e:
            body = Render.render('error_page', exception=e.message)
            self.response.body = body
            self.response.status = '404 Not Found'
        point_winner = self.__get_point_winner()
        updated_match = TennisDBService.update_match(match, point_winner)
        players_names = TennisDAO.get_players_name(updated_match.player1, updated_match.player2)
        match_param = ScoreUpdateService.show_match_params(updated_match)
        body = Render.render('match_score', **match_param, **players_names)
        self.response.body = body

    def get_uuid_from_query_string(self):
        request = self.environ.get("QUERY_STRING", '')
        parsed_request = parse_qs(request)
        uuid = parsed_request['uuid'][0]
        return uuid

    def __get_point_winner(self):
        request_body = self.environ.get('wsgi.input').read().decode()
        parsed_body = parse_qs(request_body)
        if parsed_body.get('player1', None):
            return 1
        else:
            return 2
