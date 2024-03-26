from src.controllers.base_controller import BaseController
from View.jinja import Render
from urllib.parse import parse_qs


class NewMatchController(BaseController):

    def do_get(self):
        body = Render.render('new_match')
        self.response.body = body

    def do_post(self):
        player1, player2 = self.__parse_data_from_request()
        redy_for_the_match = self.db_service.checking_available_players(player1, player2)
        if redy_for_the_match is False:
            body = Render.render('busy_player')
            self.response.body = body
            self.response.status = "400"
            return
        self.db_service.add_match(player1, player2)
        self.response.status = '303 See Other'
        self.response.headers = [('Location', '/match-score?uuid=$match_id')]

    def __parse_data_from_request(self):
        request_data = self.environ['wsgi.input'].read().decode('utf-8')
        service_data = parse_qs(request_data)
        player1_name = service_data['player1'][0]
        player2_name = service_data['player2'][0]
        return player1_name, player2_name


