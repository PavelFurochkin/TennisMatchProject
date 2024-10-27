from jinja2 import Environment, PackageLoader, select_autoescape
from View.templates.game_score_convector import GameScoreConvector


class Render:
    templates = {
        'index': 'index.html',
        'new_match': 'new_match.html',
        'match_score': 'match_score.html',
        'match_not_found': 'match_not_found.html',
        'busy_player': 'busy_is_player.html',
        'matches': 'matches.html',
    }

    env = Environment(
        loader=PackageLoader('View', 'templates'),
        autoescape=select_autoescape()
    )

    @classmethod
    def __get_template_by_name(cls, template):
        template = cls.env.get_template(cls.templates.get(template))
        return template

    @classmethod
    def render(cls, template_name, *args, **kwargs):
        template = cls.__get_template_by_name(template_name)
        if kwargs.get('current_game'):
            kwargs['current_game'] = GameScoreConvector.converter(kwargs['current_game'])
        return template.render(*args, **kwargs)

