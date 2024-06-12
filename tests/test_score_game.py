import unittest

from src.score.game import Game


class TestGame(unittest.TestCase):
    """ Метод тестирует подсчет очков в гейме"""

    def test_win_without_tie(self):
        game_score = [
            (2, 2, 1, 1, 2, 1, 2, 1, 1, 1),
            (1, 1, 1, 1),
            (2, 2, 2, 2),
        ]
        for test_game in game_score:
            game = Game()
            with self.subTest(test_game=test_game):
                for point in test_game:
                    game.add_point(point)
                self.assertEqual(game.is_over, True)

    def test_win_with_tie(self):
        game_score = [
            (2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2),
        ]
        for test_game in game_score:
            game = Game(is_tie=True)
            with self.subTest(test_game=test_game):
                for point in test_game:
                    game.add_point(point)
                self.assertEqual(game.is_over, True)

    def test_score_less7_with_tie(self):
        game_score = [
            (2, 2, 2, 2, 2, 1, 1, 2,),
        ]
        for test_game in game_score:
            game = Game(is_tie=True)
            with self.subTest(test_game=test_game):
                for point in test_game:
                    game.add_point(point)
                self.assertEqual(game.is_over, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)


