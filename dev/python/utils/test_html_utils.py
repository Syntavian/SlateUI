from python.utils.html_utils import *

class TestContaining:
    def test_containing(self):
        assert containing("abc") == r"((?:.|\s)*(?:abc)(?:.|\s)*)"

class TestFindStringValues:
    def test_find_string_values(self):
        assert find_string_values("Lorem 'ipsum' dolor 'sit' amet;") == ["'ipsum'", "'sit'"]

class TestSlateTag:
    def test_slate_tag(self):
        assert slate_tag() == r"((?:<#(?:.|\s)*?\/>)|(?:<!--#(?:.|\s)*?\/-->))"
