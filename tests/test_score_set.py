import unittest

from src.score.set import Set


class TestSet(unittest.TestCase):
    """ Метод тестирует подсчет очков в сете"""

    def test_set_without_tie(self):
        set_score = [
            (1, 1, 1, 1, 1, 1),
            (1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2)
        ]
        for set_ in set_score:
            new_set = Set()
            with self.subTest(set=set_):
                for point in set_:
                    new_set.add_point(point)
                self.assertEqual(new_set.is_over, True)

    def test_set_need_tie(self):
        set_score = [
            (1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1),
        ]
        for set_ in set_score:
            new_set = Set()
            with self.subTest(set=set_):
                for point in set_:
                    new_set.add_point(point)
                self.assertEqual(new_set.need_tie, True)

    def test_set_with_tie(self):
        set_score = [
            (1, 2, 1, 1, 1, 1),
            (1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2)
        ]
        for set_ in set_score:
            new_set = Set(need_tie=True)
            with self.subTest(set=set_):
                for point in set_:
                    new_set.add_point(point)
                self.assertEqual(new_set.is_over, True)


if __name__ == "__main__":
    unittest.main(verbosity=2)

