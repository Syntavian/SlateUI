from python.utils.string_utils import *

class TestRedactSpacing:
    def test_redact_spacing_whitespace(self):
        assert redact_spacing("  ") == " "
    def test_redact_spacing_text_endings(self):
        assert redact_spacing("  text  ") == " text "
    def test_redact_spacing_between_text(self):
        assert redact_spacing("  text  text  ") == " text text "

class TestRedactOverflow:
    def test_redact_overflow_shorten(self):
        assert redact_overflow("abcdefghijklmnopqrstuvwxyz", 5) == "abcde..."
    def test_redact_overflow_same(self):
        assert redact_overflow("abcdefghijklmnopqrstuvwxyz", 100) == "abcdefghijklmnopqrstuvwxyz"
