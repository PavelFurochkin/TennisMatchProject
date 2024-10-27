from src.controllers.base_controller import BaseController
from urllib.parse import parse_qs
from src.db.db_service.db_service import TennisDBService
from src.score.score import ScoreSchema
from View.jinja import Render


class FinishedMatchesController(BaseController):
    def do_get(self):
        player_names_list = TennisDBService.get_all_players()
        filter_by_player_name = self.get_player_name()
        matches_count = TennisDBService.get_matches_count(filter_by_player_name=filter_by_player_name)
        page_size = self.get_num_rows()
        page_number = self.get_page_number()
        records = TennisDBService.paginate(filter_by_player_name=filter_by_player_name,
                                           page_size=page_size,
                                           page=page_number)
        output = MatchRecordsService.process(records)
        body = Render.render('matches', output=output, player_names_list=player_names_list)
        self.response.body = body

    def do_post(self):
        pass

    def get_player_name(self):
        request = self.environ.get("QUERY_STRING", None)
        if request:
            parsed_request = parse_qs(request)
            name = parsed_request.get('filter_by_player_name', None)
            if name[0] == "all" or not name:
                return None
            else:
                return name[0]
        return None

    def get_num_rows(self):
        query_string = self.environ.get("QUERY_STRING", None)
        if query_string:
            parsed_query_string = parse_qs(query_string)
            num_rows = int(parsed_query_string["num_rows"][0])
        else:
            num_rows = 10
        return num_rows

    def get_page_number(self):
        query_string = self.environ.get("QUERY_STRING", None)
        if query_string:
            parsed_query_string = parse_qs(query_string)
            page_number_str = parsed_query_string.get('page', None)
            if page_number_str:
                page_number = int(page_number_str[0])
                return page_number

        page_number = 1
        return page_number


class MatchRecordsService:
    @classmethod
    def process(cls, records):
        output = []
        for record in records:
            match = record[0]
            score = ScoreSchema().loads(match.score)
            player_names = TennisDBService.get_players_name(match.player1, match.player2)
            player1, player2 = player_names['player1_name'], player_names['player2_name']
            num_sets = len(score.sets)
            if match.winner is not None:
                winner = player_names[f'player{match.winner}_name']
            else:
                continue
            set1_result, set2_result, set3_result = [
                f'{score.sets[n].p1_points}:{score.sets[n].p2_points}' if n < num_sets else "---" for n in range(3)
            ]
            output.append(dict(player1=player1, player2=player2, winner=winner,
                          set1_results=set1_result, set2_results=set2_result, set3_results=set3_result))

        return output
