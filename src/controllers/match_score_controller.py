from src.controllers.base_controller import BaseController
from View.jinja import Render
from urllib.parse import parse_qs
from src.db.db_service.db_service import TennisDBService
from src.score.ScoreUpdateService import ScoreUpdateService
from exceptions import MatchNotFoundByUUID


class MatchScoreController(BaseController):
    def do_get(self):
        try:
            match = TennisDBService.get_match_by_uuid(self.__get_uuid_from_query_string)
            match_param = ScoreUpdateService.show_match_params(match)
            players_names = TennisDBService.get_players_name(match.player1, match.player2)
            body = Render.render('match_score', **match_param, **players_names)
            self.response.body = body
        except MatchNotFoundByUUID as exc:
            body = Render.render('match_not_found', error_message=exc.message)
            self.response.body = body
            self.response.status = '404 Not Found'

    def __get_uuid_from_query_string(self):
        request = self.environ.get("QUERY_STRING", '')
        parsed_request = parse_qs(request)
        uuid = parsed_request['uuid'][0]
        return uuid
