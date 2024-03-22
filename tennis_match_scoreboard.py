from src.router.router import Router
from waitress import serve
from whitenoise import WhiteNoise


class WSGIapp(object):
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        controller_class = Router.choose_controller(self.environ.get('PATH_INFO', ''))
        controller = controller_class(self.environ)
        controller.get_method()
        response = controller.response
        self.start(response.status, response.headers)
        yield response.body


if __name__ == '__main__':
    app = WhiteNoise(WSGIapp)
    serve(app, host='0.0.0.0', port=8000)
