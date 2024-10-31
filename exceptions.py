class MatchNotFoundByUUID(Exception):
    def __init__(self, message=""):
        super().__init__()
        self.message = message


class OtherError(Exception):
    def __init__(self, message=""):
        super().__init__()
        self.message = message
