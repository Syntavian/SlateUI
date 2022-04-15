from python.utils.html_utils import *


class TestContaining:
    def test_containing(self):
        assert containing("abc") == r"((?:.|\s)*(?:abc)(?:.|\s)*)"


class TestFindStringValues:
    def test_find_string_values(self):
        assert find_string_values("Lorem 'ipsum' dolor 'sit' amet;") == [
            "'ipsum'",
            "'sit'",
        ]

    def test_find_string_values_ends(self):
        assert find_string_values("'Lorem' 'ipsum' dolor 'sit' 'amet;'") == [
            "'Lorem'",
            "'ipsum'",
            "'sit'",
            "'amet;'",
        ]

    def test_find_string_values_whole(self):
        assert find_string_values("'Lorem ipsum dolor sit amet;'") == [
            "'Lorem ipsum dolor sit amet;'"
        ]

    def test_find_string_values_string_within(self):
        assert find_string_values("'Lorem ipsum \"dolor\" sit amet;'") == [
            "'Lorem ipsum \"dolor\" sit amet;'"
        ]


class TestSlateTag:
    def test_slate_tag(self):
        assert slate_tag() == r"((?:<#(?:.|\s)*?\/>)|(?:<!--#(?:.|\s)*?\/-->))"


class TestStripSlateTag:
    def test_strip_slate_tag_short(self):
        assert strip_slate_tag("<#abc/>") == r"abc"

    def test_strip_slate_tag_long(self):
        assert strip_slate_tag("<!--#abc/-->") == r"abc"
