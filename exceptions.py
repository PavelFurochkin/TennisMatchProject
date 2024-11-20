class TennisScoreboardError(Exception):
    def __init__(self, message='Base exception', *args):
        self.message = message

    def __str__(self):
        return self.message


class MatchNotFoundByUUIDError(TennisScoreboardError):
    def __init__(self, *args):
        self.message = f"Матч не найден."


class PlayerNameError(TennisScoreboardError):
    def __init__(self, name: str, *args):
        self.message = f'Игрок {name} не может играть сам с собой.'


class TooShortNameError(TennisScoreboardError):
    def __init__(self, name: str, *args):
        self.message = f'Имя игрока {name} должно быть от 3 до 20 символов.'


class InvalidUserNameError(TennisScoreboardError):
    def __init__(self, *args):
        self.message = f"Имя не может состоять только из пробелов."