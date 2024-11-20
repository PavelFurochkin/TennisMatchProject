from src.router.router import Router
from waitress import serve
from whitenoise import WhiteNoise
from src.db.DAO.DAO import TennisDAO
from src.db.db_service.db_service import TennisDBService


class WSGIapp(object):
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        TennisDAO.create_tables()

    def __iter__(self):
        controller_class = Router.choose_controller(self.environ.get('PATH_INFO', ''))
        controller = controller_class(TennisDBService, self.environ)
        controller.get_method()
        response = controller.response
        self.start(response.status, response.headers)
        yield response.body


if __name__ == '__main__':
    app = WhiteNoise(WSGIapp, f'View/static/')
    serve(app, host='0.0.0.0', port=8000)
