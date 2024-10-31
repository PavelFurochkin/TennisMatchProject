from abc import ABC, abstractmethod

from src.controllers.response import Response
from src.db.db_service.db_service import TennisDBService


class BaseController(ABC):
    def __init__(self, environ):
        self.environ = environ
        self.response = Response()
        self.db_service = TennisDBService()

    def get_method(self):
        request_method = self.environ.get('REQUEST_METHOD')
        if request_method == 'GET':
            self.do_get()
        elif request_method == 'POST':
            self.do_post()
        else:
            pass

    @abstractmethod
    def do_get(self):
        pass

    @abstractmethod
    def do_post(self):
        pass

