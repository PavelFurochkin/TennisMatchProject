from jinja2 import Environment, PackageLoader, select_autoescape


class Render:
    templates = {
        # 'index': 'index.html',
        'new_match': 'new_match.html',
        # 'match_score': 'match_score.html',
        # 'busy_player': 'busy_is_player.html',
        # 'matches': 'matches.html',
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
    def render(cls, template):
        return cls.__get_template_by_name(template).render()
