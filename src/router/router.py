from src.controllers.start_new_match_controller import NewMatchController


class Router:
    routes = {
        # '/': index_page_controller,
        '/new-match': NewMatchController
        # '/match-score': match_score_controller
        # '/matches': matches_controller
    }

    @classmethod
    def choose_controller(cls, path):
        final_controller = cls.routes.get(path, NewMatchController)
        return final_controller
