from python.utils.function_utils import *


class TestRepeatFunction:
    def test_repeat_function(self):
        assert repeat_function(lambda a, b: a * b, 2, [(1, 2), (3, 4)]) == [2, 12]
