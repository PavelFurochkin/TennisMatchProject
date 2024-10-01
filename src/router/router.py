from src.controllers.start_new_match_controller import NewMatchController
from src.controllers.match_score_controller import MatchScoreController
from src.controllers.index_controller import IndexPageController


class Router:
    routes = {
        '/': IndexPageController,
        '/new-match': NewMatchController,
        '/match-score': MatchScoreController,
        # '/matches': matches_controller
    }

    @classmethod
    def choose_controller(cls, path):
        final_controller = cls.routes.get(path, IndexPageController)
        return final_controller
