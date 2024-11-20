from exceptions import  TennisScoreboardError
from src.controllers.base_controller import BaseController
from src.render.renderer import Render
from urllib.parse import parse_qs
from src.db.DAO.DAO import TennisDAO


class NewMatchController(BaseController):

    def do_get(self):
        body = Render.render('new_match')
        self.response.body = body

    def do_post(self):
        try:
            player1, player2 = self.__parse_data_from_request()
            redy_for_the_match = TennisDAO.checking_available_players(player1, player2)
            if redy_for_the_match is False:
                body = Render.render('busy_player')
                self.response.body = body
                self.response.status = "400"
                return
            match = self.db_service.add_match(player1, player2)
            self.response.status = '303 See Other'
            self.response.headers = [('Location', f'/match-score?uuid={match.uuid}')]
        except TennisScoreboardError as e:
            body = Render.render('error_page', exception=e.message)
            self.response.body = body
            self.response.status = '400 Bad Request'

    def __parse_data_from_request(self):
        request_data = self.environ['wsgi.input'].read().decode('utf-8')
        service_data = parse_qs(request_data)
        player1_name = service_data['player1'][0]
        player2_name = service_data['player2'][0]
        return player1_name, player2_name

