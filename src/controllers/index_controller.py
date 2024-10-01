from src.controllers.base_controller import BaseController
from View.jinja import Render


class IndexPageController(BaseController):
    def do_get(self) -> None:
        body = Render.render("index")
        self.response.body = body

    def do_post(self):
        pass
